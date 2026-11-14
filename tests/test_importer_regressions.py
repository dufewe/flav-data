import importlib.util
import gzip
import io
import json
import os
import tarfile
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
IMPORTER_ROOT = PROJECT_ROOT / 'flav-data-importer'


def load_script(name, filename):
    path = IMPORTER_ROOT / 'scripts' / filename
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    source = path.read_text(encoding='utf-8')
    exec(compile('from __future__ import annotations\n' + source, str(path), 'exec'), module.__dict__)
    return module


json_valid = load_script('json_valid', 'json-valid.py')
hepdata_ext = load_script('hepdata_ext', 'hepdata-ext.py')
inspirehep_ext = load_script('inspirehep_ext', 'inspirehep-ext.py')
arxiv_ext = load_script('arxiv_ext', 'arxiv-ext.py')
common = load_script('common', 'common.py')


class JsonValidatorTests(unittest.TestCase):
    def test_existing_example_has_required_top_level_order(self):
        source = PROJECT_ROOT / 'expe-data/CERN-LHCb/2015/12/LHCb:2015svh.json'
        with source.open(encoding='utf-8') as f:
            data = json.load(f)
        keys = list(data)
        self.assertEqual(keys[-2:], ['transition-mode', 'data'])
        self.assertEqual(json_valid.validate_json(str(source)), [])

    def test_non_object_root_returns_validation_error(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as f:
            json.dump([1, 2], f)
            f.flush()
            issues = json_valid.validate_json(f.name)

        self.assertTrue(any('Top-level JSON must be an object' in issue for issue in issues))

    def test_observable_name_rejects_embedded_transition(self):
        for name in ('FL', 'R', 'RBr[pi/K]', 'DeltaACP[mu-e]', 'Vcb(CLN)', 'f+.Vcs'):
            self.assertEqual(json_valid.validate_observable_name(name), [], name)

        for name in (
            'FL(dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0)',
        ):
            self.assertTrue(json_valid.validate_observable_name(name), name)

    def test_kinematic_condition_is_rejected(self):
        for name in (
            'dBr/dq2[4.0-4.53]', 'Br[Mll>0.2]', 'FS[Ecut>0.4]',
            'Br[high-q2]', 'M1[796,996]',
        ):
            issues = json_valid.validate_observable_name(name)
            self.assertIn('is a kinematic bin', ' '.join(issues), name)

        for name in (
            'FS', 'dBr', 'M1', 'Br[90%@CL]', 'Br[13TeV]',
            'Br[World.Average]', 'Br[mH=125GeV]', 'Br[composite_SSM]',
            'Br[k_Mpl_0.01]', 'Br[bayes]',
        ):
            self.assertEqual(json_valid.validate_observable_name(name), [], name)

    def test_channel_bearing_ratio_symbol_is_rejected(self):
        for name in (
            'RK', 'RK*', 'RK+', 'RD', 'RD*', 'Rmue', 'Rtaumu', 'Re/mu',
            'RWenu2Wmumu', 'RD*[tau/mu]', 'RK+[mu/e]',
        ):
            issues = json_valid.validate_observable_name(name)
            self.assertIn('embeds the channel', ' '.join(issues), name)

    def test_lepton_flavour_ratio_is_named_bare_R(self):
        for name in ('RBr[mu/e]', 'RGamma[tau/e]', 'RdBr/dq2[mu/e]', 'FL[mu/e]'):
            issues = json_valid.validate_observable_name(name)
            self.assertIn("a lepton-flavour ratio of rates is named 'R'",
                          ' '.join(issues), name)

        for name in ('R', 'DeltaFL[mu-e]', 'RBr[pi/K]', 'RFL[mu/e]',
                     'RACP[tau/mu]'):
            self.assertEqual(json_valid.validate_observable_name(name), [], name)

    def test_form_factor_value_names_are_accepted(self):
        for name in ('f+', 'f-', 'V', 'A0', 'A1', 'A2', 'A12'):
            self.assertEqual(json_valid.validate_observable_name(name), [], name)

    def test_form_factor_value_group_needs_no_scheme(self):
        data = [{
            'Cb_I0?_0-n_0.2.cC_I0-_1--_0.l-.vBar': self._channel(
                {**self._obs('V'), 'q2min': '-20', 'q2max': '-20'},
            ),
            'dataset': 'QCDSR',
        }]
        self.assertEqual(self._validate_data(data), [])

    def test_hqet_basis_form_factor_names_are_accepted(self):
        for name in ('f1', 'f2', 'g2', 'F1', 'F2'):
            self.assertEqual(json_valid.validate_observable_name(name), [], name)

    def test_hqet_basis_value_groups_need_no_scheme(self):
        data = [
            {
                'udb_I0?_1+n_0.2.uud_I1?_1+n_0.l-.vBar': self._channel(
                    {**self._obs('f1'), 'q2min': '0', 'q2max': '0'},
                    {**self._obs('f2'), 'q2min': '0', 'q2max': '0'},
                ),
                'dataset': 'LCSR',
            },
            {
                'udb_I0?_1+n_0.2.uds_I0?_1+n_0.l-.vBar': self._channel(
                    {**self._obs('g2'), 'q2min': '0', 'q2max': '0'},
                ),
                'dataset': 'LCSR',
            },
            {
                'udb_I0?_1+n_0.2.uud_I1?_1+n_0.l-.vBar': self._channel(
                    self._obs_with_components('F1'),
                    self._obs_with_components('F2'),
                ),
                'dataset': 'LQCD',
            },
        ]
        self.assertEqual(self._validate_data(data), [])

    def test_obsolete_lfu_q_symbols_are_rejected(self):
        for name in ('Q1[mu-e]', 'Q4[mu-e]', 'Q5[mu/e]', 'Q6[mu-e]',
                     'Q8[mu-e]', 'QFL[mu-e]'):
            with self.subTest(name=name):
                issues = json_valid.validate_observable_name(name)
                self.assertTrue(any(
                    'obsolete LFU-difference symbol' in issue for issue in issues
                ))

    def test_lfu_delta_symbols_are_accepted(self):
        for name in ('DeltaFL[mu-e]', 'DeltaP1[mu-e]', 'DeltaP3[mu-e]',
                     'DeltaP4p[mu-e]', 'DeltaP5p[mu-e]', 'DeltaP6p[mu-e]',
                     'DeltaP8p[mu-e]'):
            self.assertEqual(json_valid.validate_observable_name(name), [], name)

    def test_transition_mode_is_hyphenated(self):
        for mode in ('leptonic-decay', 'semileptonic-decay', 'non-leptonic-decay',
                     'radiative-decay', 'neutron-beta-decay', 'higgs-decay',
                     'mixing', 'scattering', 'electroweak-precision',
                     'w-production', 'higgs-production', 'low-energy',
                     'oblique-corrections'):
            self.assertEqual(json_valid.validate_transition_mode(mode), [], mode)

        self.assertTrue(json_valid.validate_transition_mode('semileptonic decay'))
        self.assertTrue(json_valid.validate_transition_mode('Higgs decay'))
        self.assertTrue(json_valid.validate_transition_mode('electroweak precision'))

    def test_pid_transition_keys_are_accepted(self):
        for key in (
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0',
            'uB_I1?_0-n_0.2.uS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0',
            'WB_I??_1??_0.2.mu_I??_1+n_0.VMU_I??_1+n_0',
            'uB_I1?_0-n_0.2.uS_I1?_0-n_0.l+.v',
            'uud_I1?_1+n_0.UUD_I1?_1+n_0.2.Z_I??_1??_0.2.l+.l-',
            'qQ_I1?_0-n_0.2.Ud_I2-_0-n_0.E_I??_1+n_0.ve_I??_1+n_0',
            'dB_I1?_0-n_0.2.cC_I0-_1--_0.qQ_I1?_0-n_0',
            'Cb_I0?_0-n_0.2.cC_I0-_1--_0.l-.vBar',
            'no-transition',
        ):
            self.assertEqual(json_valid.validate_transition_key(key), [], key)

    def test_legacy_particle_tokens_are_rejected(self):
        for key in (
            'B0.2.K*0.mu+.mu-',
            'B0.2.Kst0.mu+.mu-',
            'W-.2.mu-.nuBar',
            'B0.2.K*0bar.v.vBar',
            'B0Bar.2.D0*+(2300).l-.vBar',
        ):
            issues = json_valid.validate_transition_key(key)
            self.assertTrue(issues, key)
            self.assertIn('is not a registered pid', ' '.join(issues), key)

    def test_empty_particle_state_is_rejected(self):
        for key in (
            '.2.', '.2.dS_I1?_1-n_0', 'dB_I1?_0-n_0.2.',
            'dB_I1?_0-n_0.2..2.dS_I1?_1-n_0',
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0/uB_I1?_0-n_0.2.',
        ):
            issues = json_valid.validate_transition_key(key)
            self.assertIn('empty particle state', ' '.join(issues), key)

    def test_particle_type_order(self):
        issues = json_valid.validate_transition_key(
            'dB_I1?_0-n_0.2.MU_I??_1+n_0.dS_I1?_1-n_0'
        )
        self.assertTrue(issues)
        self.assertIn('orders charged lepton before meson', ' '.join(issues))

    def test_mass_order_within_particle_type(self):
        issues = json_valid.validate_transition_key(
            'dB_I1?_0-n_0.2.E_I??_1+n_0.mu_I??_1+n_0'
        )
        self.assertTrue(issues)
        self.assertIn('light to heavy', ' '.join(issues))
        self.assertIn('mu_I??_1+n_0.E_I??_1+n_0', ' '.join(issues))

    def test_charge_order_for_equal_masses(self):
        issues = json_valid.validate_transition_key(
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.mu_I??_1+n_0.MU_I??_1+n_0'
        )
        self.assertTrue(issues)
        self.assertIn('charge order', ' '.join(issues))

    def test_ratio_keys_check_each_transition(self):
        good = (
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.E_I??_1+n_0.e_I??_1+n_0/'
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0'
        )
        self.assertEqual(json_valid.validate_transition_key(good), [])
        bad = (
            'dB_I1?_0-n_0.2.MU_I??_1+n_0.dS_I1?_1-n_0/'
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0'
        )
        self.assertTrue(json_valid.validate_transition_key(bad))

    def test_inclusive_system_follows_parent_b_flavour(self):
        for key in (
            'uB_I1?_0-n_0.2.Xc.e_I??_1+n_0.VE_I??_1+n_0',
            'dB_I1?_0-n_0.2.Xs.ph_I??_1--_0',
        ):
            issues = json_valid.validate_transition_key(key)
            self.assertIn('the inclusive system is', ' '.join(issues), key)

        for key in (
            'uB_I1?_0-n_0.2.XcBar.E_I??_1+n_0.ve_I??_1+n_0',
            'Ub_I1?_0-n_0.2.Xc.e_I??_1+n_0.VE_I??_1+n_0',
            'Db_I1?_0-n_0.2.Xs.ph_I??_1--_0',
            'dB_I1?_0-n_0.2.XsBar.ph_I??_1--_0',
            'B.2.Xc.l-.vBar',
            'uB_I1?_0-n_0.2.Xu.l-.vBar',
        ):
            self.assertEqual(json_valid.validate_transition_key(key), [], key)

    def test_charged_lepton_fixes_its_neutrino(self):
        for key in (
            'Db_I1?_0-n_0.2.Dc_I1?_0-n_0.tau_I??_1+n_0.v',
            'WB_I??_1??_0.2.tau_I??_1+n_0.vtau_I??_1+n_0',
            'uB_I1?_0-n_0.2.uS_I1?_0-n_0.l+.vBar',
        ):
            issues = json_valid.validate_transition_key(key)
            self.assertIn('must be accompanied by', ' '.join(issues), key)

        issues = json_valid.validate_transition_key(
            'qQ_I1?_0-n_0.2.Ud_I2-_0-n_0.MU_I??_1+n_0.ve_I??_1+n_0'
        )
        self.assertIn('does not match the charged lepton', ' '.join(issues))

        # scattering already carries the neutrino in the initial state
        self.assertEqual(json_valid.validate_transition_key(
            'qQ_I1?_0-n_0.vmu_I??_1+n_0.2.qQ_I1?_0-n_0.mu_I??_1+n_0'
        ), [])

    def test_lepton_energy_boundaries_are_kinematic_fields(self):
        obs = {**self._obs('M1'), 'emin': '0.4', 'emax': '+inf', 'unit': 'GeV'}
        self.assertEqual(self._validate_data([{
            'Ub_I1?_0-n_0.2.Xc.e_I??_1+n_0.VE_I??_1+n_0': {'obs@1': obs},
        }]), [])

    def test_scalar_meson_scenarios_share_one_pid(self):
        key = 'Db_I1?_0-n_0.2.Dc_I1?_0+n_0.l-.vBar'
        self.assertEqual(json_valid.validate_transition_key(key), [])
        # the scenario mass label belongs in the group note, not in the pid
        self.assertTrue(json_valid.validate_transition_key(
            'Db_I1?_0-n_0.2.Dc_I1?_0+n_0(2300).l-.vBar'
        ))

    def _validate_raw(self, raw):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as f:
            f.write(raw)
            f.flush()
            return json_valid.validate_json(f.name)

    def test_duplicate_json_keys_are_rejected(self):
        obs = ('{"name": "f+", "value": "0.4", '
               '"total_upper": "0.02", "total_lower": "0.02"}')
        channel = '{"obs@1": %s}' % obs
        cases = {
            'dB_I1?_0-n_0.2.Ud_I2-_0-n_0.l+.v': (
                '"data": [{"dB_I1?_0-n_0.2.Ud_I2-_0-n_0.l+.v": %s, "dB_I1?_0-n_0.2.Ud_I2-_0-n_0.l+.v": %s}]'
                % (channel, channel)
            ),
            'obs@1': (
                '"data": [{"dB_I1?_0-n_0.2.Ud_I2-_0-n_0.l+.v": {"obs@1": %s, "obs@1": %s}}]'
                % (obs, obs)
            ),
            'title': '"title": "Second", "data": []',
        }
        for key, tail in cases.items():
            with self.subTest(key=key):
                raw = ('{"inspire-hep": "[T:2024](https://inspirehep.net/literature/1)", '
                       '"author": "Doe, J.", "title": "Test", '
                       '"arxiv": "[hep-ex/2401.00001v1](https://arxiv.org/pdf/2401.00001)", '
                       '"time": "2024.01.01", "abstract": "Test abstract.", '
                       '"transition-mode": "semileptonic-decay", ' + tail + '}')
                issues = self._validate_raw(raw)
                self.assertTrue(
                    any(f"Duplicate JSON key '{key}'" in issue for issue in issues),
                    issues,
                )

    @staticmethod
    def _obs(name):
        return {
            'name': name,
            'value': '1.0',
            'total_upper': '0.1',
            'total_lower': '0.1',
        }

    @classmethod
    def _obs_with_components(cls, name):
        obs = cls._obs(name)
        del obs['total_upper'], obs['total_lower']
        obs.update({
            'type@1_error': 'stat',
            'type@1_upper': '0.035',
            'type@1_lower': '0.036',
            'type@2_error': 'syst',
            'type@2_upper': '0.017',
            'type@2_lower': '0.017',
        })
        return obs

    @classmethod
    def _channel(cls, *obs):
        return {f'obs@{i}': o for i, o in enumerate(obs, 1)}

    def _validate_data(self, data_block, mode='semileptonic-decay'):
        doc = {
            'inspire-hep': '[Test:2024](https://inspirehep.net/literature/1)',
            'author': 'Doe, J.',
            'title': 'Test',
            'arxiv': '[hep-ex/2401.00001v1](https://arxiv.org/pdf/2401.00001)',
            'time': '2024.01.01',
            'abstract': 'Test abstract.',
            'transition-mode': mode,
            'data': data_block,
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as f:
            json.dump(doc, f)
            f.flush()
            return json_valid.validate_json(f.name)

    def test_data_groups_allow_cross_channel_matrices(self):
        data = [{
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': self._channel(
                self._obs('FL'), self._obs('S3'),
            ),
            'uB_I1?_0-n_0.2.uS_I1?_0-n_0.MU_I??_1+n_0.mu_I??_1+n_0': self._channel(self._obs('FL')),
            'correlation': [[1.0, 0.5, 0.1], [0.5, 1.0, 0.2], [0.1, 0.2, 1.0]],
        }]
        self.assertEqual(self._validate_data(data), [])

    def test_group_note_acknowledges_out_of_range_correlation(self):
        data = [{
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': self._channel(
                self._obs('FL'), self._obs('S3'),
            ),
            'note': 'Authors print rho = 1.06 for this pair.',
            'correlation': [[1.0, 1.06], [1.06, 1.0]],
        }]
        self.assertEqual(self._validate_data(data), [])

    def test_group_note_must_be_non_empty_string(self):
        for value in ('', '   ', 1):
            with self.subTest(note=value):
                data = [{
                    'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': self._channel(self._obs('FL')),
                    'note': value,
                }]
                issues = self._validate_data(data)
                self.assertTrue(any('note: must be a non-empty string' in issue
                                    for issue in issues))

    def test_group_note_sits_before_matrix(self):
        data = [{
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': self._channel(self._obs('FL')),
            'correlation': [[1.0]],
            'note': 'documented',
        }]
        issues = self._validate_data(data)
        self.assertTrue(any("'note' appears after a matrix key" in issue
                            for issue in issues))

    def test_data_group_matrix_dimension_must_cover_all_channels(self):
        data = [{
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': self._channel(
                self._obs('FL'), self._obs('S3'),
            ),
            'uB_I1?_0-n_0.2.uS_I1?_0-n_0.MU_I??_1+n_0.mu_I??_1+n_0': self._channel(self._obs('FL')),
            'correlation': [[1.0, 0.5], [0.5, 1.0]],
        }]
        issues = self._validate_data(data)
        self.assertTrue(any('does not match the 3 observables' in issue for issue in issues))

    def test_data_group_channel_must_precede_matrix(self):
        data = [{
            'correlation': [[1.0]],
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': self._channel(self._obs('FL')),
        }]
        issues = self._validate_data(data)
        self.assertTrue(any('appears after a matrix key' in issue for issue in issues))

    def test_group_matrix_must_not_be_null(self):
        data = [{
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': self._channel(self._obs('FL')),
            'correlation': None,
        }]
        issues = self._validate_data(data)
        self.assertTrue(any('do not set it to null' in issue for issue in issues))

    def test_group_dataset_sits_between_channels_and_matrix(self):
        data = [{
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': self._channel(self._obs('FL')),
            'dataset': 'EXPE',
            'correlation': [[1.0]],
        }]
        self.assertEqual(self._validate_data(data), [])

    def test_group_dataset_accepts_canonical_sources(self):
        for value in ('LQCD', 'LCSR', 'QCDSR', 'EXPE', 'LQCD+LCSR',
                      'LQCD+LCSR+QCDSR', 'LQCD+LCSR+QCDSR+EXPE'):
            with self.subTest(dataset=value):
                data = [{
                    'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': self._channel(self._obs('FL')),
                    'dataset': value,
                }]
                self.assertEqual(self._validate_data(data), [])

    def test_group_dataset_rejects_non_source_values(self):
        for value in ('maximum likelihood', 'nominal', 'experiment',
                      'LCSR + LQCD', 'LCSR+LQCD', 'LQCD+LQCD', 'NLO',
                      'LQCD+QCDSR+LCSR'):
            with self.subTest(dataset=value):
                data = [{
                    'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': self._channel(self._obs('FL')),
                    'dataset': value,
                }]
                issues = self._validate_data(data)
                self.assertTrue(
                    any('dataset:' in issue for issue in issues), issues,
                )

    def test_observable_scheme_is_rejected(self):
        obs = self._obs('FL')
        obs['scheme'] = 'BCL'
        issues = self._validate_data([{
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': {'obs@1': obs},
        }])
        self.assertTrue(any("unknown observable field 'scheme'" in issue for issue in issues))

    def test_observable_ref_must_be_a_markdown_link(self):
        channel = 'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0'
        good = {**self._obs('FL'),
                'ref': '[LHCb:2015svh](https://inspirehep.net/literature/1409497)'}
        self.assertEqual(self._validate_data([{channel: {'obs@1': good}}]), [])

        for ref in ('LHCb:2015svh', '1409497', '[LHCb:2015svh]()', '[](https://x)'):
            obs = {**self._obs('FL'), 'ref': ref}
            issues = self._validate_data([{channel: {'obs@1': obs}}])
            self.assertTrue(any('must be a Markdown link' in i for i in issues), ref)

    def test_group_metadata_order_is_enforced(self):
        after_matrix = [{
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': self._channel(self._obs('FL')),
            'correlation': [[1.0]],
            'dataset': 'EXPE',
        }]
        issues = self._validate_data(after_matrix)
        self.assertTrue(any("'dataset' appears after a matrix key" in issue for issue in issues))

        after_dataset = [{
            'dataset': 'EXPE',
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': self._channel(self._obs('FL')),
        }]
        issues = self._validate_data(after_dataset)
        self.assertTrue(any("appears after 'dataset'" in issue for issue in issues))

        dataset_after_scheme = [{
            'Db_I1?_0-n_0.2.uD_I2-_0-n_0.l-.vBar': self._channel(self._obs('a0_f+')),
            'scheme': 'BCL',
            'dataset': 'LQCD+LCSR',
        }]
        issues = self._validate_data(dataset_after_scheme)
        self.assertTrue(any("'dataset' appears after 'scheme'" in issue for issue in issues))

    def test_group_dataset_must_be_non_empty_string(self):
        data = [{
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': self._channel(self._obs('FL')),
            'dataset': '',
        }]
        issues = self._validate_data(data)
        self.assertTrue(any('dataset: must be a non-empty string' in issue for issue in issues))

    def test_coefficient_group_requires_scheme(self):
        data = [{
            'Db_I1?_0-n_0.2.uD_I2-_0-n_0.l-.vBar': self._channel(self._obs('a0_f+')),
        }]
        issues = self._validate_data(data)
        self.assertTrue(any(
            "must declare a group-level 'scheme'" in issue
            for issue in issues
        ))

    def test_coefficient_group_accepts_canonical_scheme(self):
        for scheme in ('BK', 'BGL', 'BCL', 'BSZ', 'DLM', 'MR'):
            with self.subTest(scheme=scheme):
                data = [{
                    'Db_I1?_0-n_0.2.uD_I2-_0-n_0.l-.vBar': self._channel(self._obs('a0_f+')),
                    'dataset': 'LQCD+LCSR',
                    'scheme': scheme,
                    'correlation': [[1.0]],
                }]
                self.assertEqual(self._validate_data(data), [])

    def test_tagged_coefficient_name_still_requires_scheme(self):
        for name in ('a0_F+(nominal)', 'a1_f+[higher-order]', 'a0_f+'):
            with self.subTest(name=name):
                data = [{
                    'Db_I1?_0-n_0.2.uD_I2-_0-n_0.l-.vBar': self._channel(self._obs(name)),
                    'dataset': 'LQCD',
                }]
                issues = self._validate_data(data)
                self.assertTrue(any(
                    "must declare a group-level 'scheme'" in issue
                    for issue in issues
                ), issues)

        data = [{
            'Db_I1?_0-n_0.2.uD_I2-_0-n_0.l-.vBar': self._channel(self._obs('a0_F+(nominal)')),
            'dataset': 'LQCD',
            'scheme': 'BCL',
        }]
        self.assertEqual(self._validate_data(data), [])

    def test_obsolete_symbol_with_tag_is_rejected(self):
        for name in ('a0_fp(nominal)', 'a1_Fp[higher-order]', 'Q5[mu-e]'):
            with self.subTest(name=name):
                self.assertTrue(json_valid.validate_observable_name(name), name)

    def test_obsolete_form_factor_symbols_are_rejected(self):
        for name in ('a0_fp', 'a1_Fp', 'a2_Gp', 'a0_hp', 'a1_htp'):
            with self.subTest(name=name):
                data = [{
                    'Db_I1?_0-n_0.2.uD_I2-_0-n_0.l-.vBar': self._channel(self._obs(name)),
                    'dataset': 'LQCD',
                    'scheme': 'BCL',
                }]
                issues = self._validate_data(data)
                self.assertTrue(any(
                    'obsolete form-factor symbol' in issue for issue in issues
                ))

    def test_form_factor_helicity_plus_symbols_are_accepted(self):
        for name in ('a0_h+', 'a1_ht+'):
            with self.subTest(name=name):
                data = [{
                    'Db_I1?_0-n_0.2.uD_I2-_0-n_0.l-.vBar': self._channel(self._obs(name)),
                    'dataset': 'LQCD',
                    'scheme': 'BCL',
                }]
                self.assertEqual(self._validate_data(data), [])

    def test_primed_baryon_helicity_symbols_are_accepted(self):
        for name in ("a0_Fv'", "a1_Gv'", "a2_hv'", "a0_htv'"):
            with self.subTest(name=name):
                data = [{
                    'udb_I0?_1+n_0.2.uds_I0?_3-n_0.l+.l-': self._channel(self._obs(name)),
                    'dataset': 'LQCD',
                    'scheme': 'MR',
                }]
                self.assertEqual(self._validate_data(data), [])

    def test_scheme_rejects_long_or_unknown_values(self):
        for value in ('Bourrely-Caprini-Lellouch (arXiv:0807.2722)', 'bcl',
                      'BGL '):
            with self.subTest(scheme=value):
                data = [{
                    'Db_I1?_0-n_0.2.uD_I2-_0-n_0.l-.vBar': self._channel(self._obs('a0_f+')),
                    'scheme': value,
                }]
                issues = self._validate_data(data)
                self.assertTrue(any('unsupported value' in issue for issue in issues))

    def test_scheme_order_is_enforced(self):
        after_matrix = [{
            'Db_I1?_0-n_0.2.uD_I2-_0-n_0.l-.vBar': self._channel(self._obs('a0_f+')),
            'correlation': [[1.0]],
            'dataset': 'LQCD',
            'scheme': 'BCL',
        }]
        issues = self._validate_data(after_matrix)
        self.assertTrue(any(
            "'scheme' appears after a matrix key" in issue for issue in issues
        ))

        after_scheme = [{
            'scheme': 'BCL',
            'Db_I1?_0-n_0.2.uD_I2-_0-n_0.l-.vBar': self._channel(self._obs('a0_f+')),
        }]
        issues = self._validate_data(after_scheme)
        self.assertTrue(any(
            "appears after 'scheme'" in issue for issue in issues
        ))

    def test_single_component_error_must_be_total(self):
        obs = self._obs('FL')
        del obs['total_upper'], obs['total_lower']
        obs.update({
            'type@1_error': 'stat',
            'type@1_upper': '0.1',
            'type@1_lower': '0.1',
        })
        issues = self._validate_data([{
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': {'obs@1': obs},
        }])
        self.assertTrue(any(
            'single error must be written as the total error' in issue
            for issue in issues
        ))

    def test_multiple_component_errors_are_accepted(self):
        obs = self._obs_with_components('FL')
        self.assertEqual(self._validate_data([{
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': {'obs@1': obs},
        }]), [])

    def test_theo_source_labels_are_accepted(self):
        obs = self._obs_with_components('a0_f+')
        obs['type@1_error'] = 'theo:a2_a4'
        obs['type@2_error'] = 'theo:mu_pi'
        self.assertEqual(self._validate_data([{
            'Db_I1?_0-n_0.2.uD_I2-_0-n_0.l-.vBar': {'obs@1': obs},
            'scheme': 'BCL',
        }]), [])

    def test_theo_source_label_grammar_is_enforced(self):
        for label in ('theo:', 'theo:MU', 'theo:mu pi', 'theo:mu-pi'):
            obs = self._obs_with_components('a0_f+')
            obs['type@1_error'] = label
            issues = self._validate_data([{
                'Db_I1?_0-n_0.2.uD_I2-_0-n_0.l-.vBar': {'obs@1': obs},
                'scheme': 'BCL',
            }])
            self.assertTrue(issues, label)
            self.assertIn('unknown error label', ' '.join(issues), label)

    def test_unit_must_be_bare_ascii(self):
        channel = 'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0'
        for unit in (
            '1e-6', '10^{-4}', '1E-3', '10^-11',
            '1e-3GeV2', '1e-3GeV3', '1e-15 GeV',
            'GeV^{-2}', 'GeV$^{-2}$', '%',
        ):
            obs = self._obs('Br')
            obs['unit'] = unit
            issues = self._validate_data([{channel: {'obs@1': obs}}])
            self.assertTrue(
                any('is not a bare ASCII unit' in issue for issue in issues), unit
            )

        for unit in ('GeV', 'GeV-2', 'GeV2', 'MeV', 'ps-1'):
            obs = self._obs('Mass')
            obs['unit'] = unit
            self.assertEqual(
                self._validate_data([{channel: {'obs@1': obs}}]), [], unit
            )

    def test_total_and_component_errors_cannot_mix(self):
        obs = self._obs_with_components('FL')
        obs['total_upper'] = '0.1'
        obs['total_lower'] = '0.1'
        issues = self._validate_data([{
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': {'obs@1': obs},
        }])
        self.assertTrue(any(
            'mixes component errors' in issue for issue in issues
        ))

    def test_bound_needs_level_and_no_component_error(self):
        obs = {
            'name': 'Br',
            'type@1_upper': '5.9e-6',
            'type@1_level': '90%@CLs',
        }
        self.assertEqual(self._validate_data([{
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': {'obs@1': obs},
        }]), [])

        obs.pop('type@1_level')
        issues = self._validate_data([{
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': {'obs@1': obs},
        }])
        self.assertTrue(any(
            "present without 'type@1_level'" in issue for issue in issues
        ))

    def test_combined_fit_and_bound_use_distinct_slots(self):
        obs = self._obs_with_components('Br')
        obs.update({'type@3_upper': '5.9e-6', 'type@3_level': '90%@CLs'})
        self.assertEqual(self._validate_data([{
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': {'obs@1': obs},
        }]), [])

        shared = self._obs_with_components('Br')
        shared.update({'type@1_upper': '5.9e-6', 'type@1_level': '90%@CLs'})
        issues = self._validate_data([{
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': {'obs@1': shared},
        }])
        self.assertTrue(any(
            "is used both as a component error" in issue for issue in issues
        ))

    def test_legacy_error_fields_are_rejected(self):
        obs = self._obs('FL')
        del obs['total_upper'], obs['total_lower']
        obs.update({'error_upper': '0.1', 'error_lower': '0.1'})
        issues = self._validate_data([{
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': {'obs@1': obs},
        }])
        self.assertTrue(any(
            "unknown observable field 'error_upper'" in issue for issue in issues
        ))

    def test_legacy_channel_to_group_dict_is_rejected(self):
        issues = self._validate_data({
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': [{'obs@1': self._obs('FL')}],
        })
        self.assertTrue(any('data must be an array of data groups' in issue for issue in issues))

    def test_channel_must_be_observable_object(self):
        for channel in (
            [{'obs@1': self._obs('FL')}],
            [r'$B^{0}\to K^{*0}\mu^{+}\mu^{-}$', {'obs@1': self._obs('FL')}],
        ):
            issues = self._validate_data([{'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': channel}])
            self.assertTrue(
                any('must be an object of obs@N entries' in issue for issue in issues),
                channel,
            )

    def test_channel_latex_key_is_rejected(self):
        issues = self._validate_data([{
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': {
                'latex': r'$B^{0}\to K^{*0}\mu^{+}\mu^{-}$',
                'obs@1': self._obs('FL'),
            },
        }])
        self.assertTrue(any("disallowed field 'latex'" in issue for issue in issues))

    def test_no_transition_channel_is_observable_object(self):
        data = [{
            'no-transition': self._channel(self._obs('Mass(Z)')),
        }]
        self.assertEqual(self._validate_data(data), [])

    def test_observable_latex_is_rejected(self):
        obs = self._obs('FL')
        obs['latex'] = r'$F_L$'
        issues = self._validate_data([{
            'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': {'obs@1': obs},
        }])
        self.assertTrue(any("unknown observable field 'latex'" in issue for issue in issues))

    def test_top_level_pdf_is_rejected(self):
        doc = {
            'inspire-hep': '[Test:2024](https://inspirehep.net/literature/1)',
            'author': 'Doe, J.',
            'title': 'Test',
            'arxiv': '[hep-ex/2401.00001v1](https://arxiv.org/pdf/2401.00001)',
            'time': '2024.01.01',
            'abstract': 'Test abstract.',
            'pdf': 'https://arxiv.org/pdf/2401.00001',
            'transition-mode': 'semileptonic-decay',
            'data': [{
                'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': self._channel(self._obs('FL')),
            }],
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as f:
            json.dump(doc, f)
            f.flush()
            issues = json_valid.validate_json(f.name)
        self.assertTrue(any("Forbidden field present: 'pdf'" in issue for issue in issues))


    def test_world_average_spans_processes_in_one_file(self):
        data = [
            {
                'no-transition': self._channel(
                    {**self._obs('Tau(BsL0)'), 'unit': 'ps'},
                    {**self._obs('Tau(BsH0)'), 'unit': 'ps'},
                ),
            },
            {
                'Db_I1?_0-n_0.2.Dc_I1?_1-n_0.tau_I??_1+n_0.vBar': self._channel(
                    self._obs('Br'),
                ),
            },
        ]
        self.assertEqual(self._validate_data(data, mode='world-average'), [])

    def test_world_average_group_matrix_spans_all_channels(self):
        data = [{
            'Db_I1?_0-n_0.2.Dc_I1?_0-n_0.tau_I??_1+n_0.vBar/'
            'Db_I1?_0-n_0.2.Dc_I1?_0-n_0.l-.vBar': self._channel(
                self._obs('R'),
            ),
            'Db_I1?_0-n_0.2.Dc_I1?_1-n_0.tau_I??_1+n_0.vBar/'
            'Db_I1?_0-n_0.2.Dc_I1?_1-n_0.l-.vBar': self._channel(
                self._obs('R'),
            ),
            'note': 'combined R(D)-R(D*) average',
            'correlation': [[1.0, -0.38], [-0.38, 1.0]],
        }]
        self.assertEqual(self._validate_data(data, mode='world-average'), [])

    def test_world_average_matrix_must_cover_every_channel(self):
        data = [{
            'Db_I1?_0-n_0.2.Dc_I1?_0-n_0.tau_I??_1+n_0.vBar/'
            'Db_I1?_0-n_0.2.Dc_I1?_0-n_0.l-.vBar': self._channel(
                self._obs('R'),
            ),
            'Db_I1?_0-n_0.2.Dc_I1?_1-n_0.tau_I??_1+n_0.vBar/'
            'Db_I1?_0-n_0.2.Dc_I1?_1-n_0.l-.vBar': self._channel(
                self._obs('R'),
            ),
            'correlation': [[1.0]],
        }]
        issues = self._validate_data(data, mode='world-average')
        self.assertTrue(any('does not match' in issue for issue in issues))

    def test_world_average_values_are_float_strings(self):
        obs = {'name': 'Mass(W)', 'value': 80.3692,
               'total_upper': 0.0133, 'total_lower': 0.0133, 'unit': 'GeV'}
        issues = self._validate_data(
            [{'no-transition': self._channel(obs)}], mode='world-average',
        )
        self.assertTrue(any('value' in issue for issue in issues))

    def test_particle_label_argument_names_are_accepted(self):
        for name in ('Mass(Z)', 'Mass(W)', 'Mass(t)', 'Mass(H)', 'Mass(BsL0)',
                     'Tau(B0)', 'Tau(Lambdab0)', 'Gamma(Z)', 'mass(b)',
                     'alphas(MZ)'):
            with self.subTest(name=name):
                self.assertEqual(json_valid.validate_observable_name(name), [])

    def test_obsolete_mass_shortcuts_are_rejected(self):
        for name in ('MZ', 'MW', 'Mtop', 'MH', 'Mh'):
            with self.subTest(name=name):
                issues = json_valid.validate_observable_name(name)
                self.assertTrue(any(
                    'obsolete mass shortcut' in issue for issue in issues
                ))

    def test_legacy_snapshot_shapes_are_rejected(self):
        pdg = {
            'inspire-hep': '[PDG:2024](https://inspirehep.net/literature/1)',
            'author': 'Navas, S. and others',
            'collaboration': 'PDG',
            'title': 'Review of Particle Physics',
            'year': '2024',
            'data': {'PDG@W': {'obs@1': {
                'name': 'Mass(W)', 'value': 80.3692,
                'total_upper': 0.0133, 'total_lower': 0.0133,
            }}},
        }
        hflav = {
            'HFLAV@overview': {
                'group': 'HFLAV',
                'inspire-hep': '[HFLAV:2024](https://inspirehep.net/literature/1)',
                'observables': [{'name': 'Tau(B0)', 'value': 1.517}],
            },
        }
        for doc in (pdg, hflav):
            with self.subTest(keys=list(doc)):
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as f:
                    json.dump(doc, f)
                    f.flush()
                    issues = json_valid.validate_json(f.name)
                self.assertTrue(issues)
                self.assertTrue(any(
                    'transition-mode' in issue for issue in issues
                ))


class CorrelationMatrixTests(unittest.TestCase):
    def test_valid_correlation_passes(self):
        matrix = [[1.0, 0.5], [0.5, 1.0]]
        self.assertEqual(json_valid.validate_correlation(matrix, 'm'), [])

    def test_correlation_diagonal_must_be_one(self):
        matrix = [[1.0, 0.5], [0.5, 0.9]]
        self.assertTrue(any('expected 1.0' in issue for issue in
                            json_valid.validate_correlation(matrix, 'm')))

    def test_correlation_off_diagonal_range(self):
        matrix = [[1.0, 1.5], [1.5, 1.0]]
        self.assertTrue(any('outside [-1, 1]' in issue for issue in
                            json_valid.validate_correlation(matrix, 'm')))

    def test_correlation_out_of_range_is_an_error_by_default(self):
        matrix = [[1.0, 1.060], [1.060, 1.0]]
        self.assertTrue(any('outside [-1, 1]' in issue
                            for issue in json_valid.validate_correlation(
                                matrix, 'm')))

    def test_correlation_out_of_range_warns_when_acknowledged(self):
        matrix = [[1.0, 1.060], [1.060, 1.0]]
        self.assertEqual(json_valid.validate_correlation(
            matrix, 'm', acknowledged=True), [])

    def test_correlation_rejects_non_finite(self):
        for bad in (float('nan'), float('inf')):
            matrix = [[1.0, bad], [bad, 1.0]]
            self.assertTrue(any('not finite' in issue for issue in
                                json_valid.validate_correlation(matrix, 'm')))

    def test_correlation_rejects_boolean_element(self):
        matrix = [[1.0, True], [True, 1.0]]
        self.assertTrue(any('not numeric' in issue for issue in
                            json_valid.validate_correlation(matrix, 'm')))

    def test_correlation_rejects_asymmetry(self):
        matrix = [[1.0, 0.5], [0.2, 1.0]]
        self.assertTrue(any('not symmetric' in issue for issue in
                            json_valid.validate_correlation(matrix, 'm')))

    def test_covariance_diagonal_matches_variance(self):
        matrix = [[0.25, 0.1], [0.1, 0.49]]
        self.assertEqual(
            json_valid.validate_correlation(matrix, 'm', True, [0.5, 0.7]), [])

    def test_covariance_diagonal_wrong_scale_fails(self):
        matrix = [[999.0, 0.0], [0.0, 999.0]]
        self.assertTrue(any('does not match the observable variance' in issue
                            for issue in json_valid.validate_correlation(
                                matrix, 'm', True, [0.5, 0.7])))

    def test_covariance_negative_diagonal_fails(self):
        matrix = [[-0.25, 0.0], [0.0, 0.49]]
        self.assertTrue(any('negative' in issue for issue in
                            json_valid.validate_correlation(
                                matrix, 'm', True, [0.5, 0.7])))

    def test_covariance_tolerates_rounding_but_not_gross_error(self):
        self.assertEqual(
            json_valid.validate_correlation([[0.26]], 'm', True, [0.5]), [])
        self.assertTrue(
            json_valid.validate_correlation([[0.30]], 'm', True, [0.5]))

    def test_observable_sigma_total_and_components(self):
        total = {'total_upper': '0.4', 'total_lower': '0.6'}
        self.assertAlmostEqual(json_valid._observable_sigma(total), 0.5)
        comp = {
            'type@1_error': 'stat', 'type@1_upper': '0.3', 'type@1_lower': '0.3',
            'type@2_error': 'syst', 'type@2_upper': '0.4', 'type@2_lower': '0.4',
        }
        self.assertAlmostEqual(json_valid._observable_sigma(comp), 0.5)
        self.assertAlmostEqual(json_valid._observable_sigma(comp, 'type@1'), 0.3)
        self.assertIsNone(json_valid._observable_sigma({'value': '1.0'}))


class DashboardDataTests(unittest.TestCase):
    def test_skips_invalid_month_keys_and_corrupt_details(self):
        dashboard_path = PROJECT_ROOT / 'flav.py'
        source = dashboard_path.read_text(encoding='utf-8')
        namespace = {'__name__': 'dashboard_test'}
        exec(compile('from __future__ import annotations\n' + source, str(dashboard_path), 'exec'), namespace)

        with tempfile.TemporaryDirectory() as directory:
            group_dir = Path(directory) / 'Group' / '2020'
            group_dir.mkdir(parents=True)
            (group_dir / 'Group@2020.json').touch()
            records = namespace['get_cached_data'].__wrapped__(
                '', 'Group', [2020], [1], lambda path: {}, directory
            )

        self.assertEqual(records, [])

    def test_detect_years_checks_index_paths_without_loading_them(self):
        dashboard_path = PROJECT_ROOT / 'flav.py'
        source = dashboard_path.read_text(encoding='utf-8')
        namespace = {'__name__': 'dashboard_test'}
        exec(compile('from __future__ import annotations\n' + source, str(dashboard_path), 'exec'), namespace)

        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / 'Group' / '2020').mkdir(parents=True)
            (Path(directory) / 'Group' / '2020' / 'Group@2020.json').touch()
            years = namespace['detect_years'].__wrapped__(
                '', 'Group', 2019, 2020,
                lambda path: self.fail('detect_years should not parse index data'),
                directory,
            )

        self.assertEqual(years, [2020])

    def test_matrix_label_reads_group_observables(self):
        dashboard_path = PROJECT_ROOT / 'flav.py'
        source = dashboard_path.read_text(encoding='utf-8')
        namespace = {'__name__': 'dashboard_test'}
        exec(compile('from __future__ import annotations\n' + source, str(dashboard_path), 'exec'), namespace)

        obs = {'name': 'BR', 'type@1_error': 'stat',
               'type@1_upper': '0.1', 'type@1_lower': '0.1',
               'type@2_error': 'syst',
               'type@2_upper': '0.05', 'type@2_lower': '0.05'}
        group = {'dB_I1?_0-n_0.2.MU_I??_1+n_0.mu_I??_1+n_0': {'obs@1': obs}, 'type@1_correlation': [[1.0]]}
        self.assertEqual(
            namespace['matrix_label']('type@1_correlation', group),
            'STAT-CORRELATION',
        )


class AuthorFormattingTests(unittest.TestCase):
    def test_arxiv_name_to_bibtex_handles_particles_and_mononyms(self):
        self.assertEqual(common.arxiv_name_to_bibtex('Danny van Dyk'), 'van Dyk, Danny')
        self.assertEqual(common.arxiv_name_to_bibtex('Roel Aaij'), 'Aaij, Roel')
        self.assertEqual(common.arxiv_name_to_bibtex('LHCb'), 'LHCb')
        self.assertEqual(common.arxiv_name_to_bibtex('Aaij, Roel'), 'Aaij, Roel')

    def test_arxiv_author_str_uses_bibtex_tiers(self):
        names = ['Danny van Dyk', 'Blaženka Melić', 'Roel Aaij']
        result = common.format_authors(
            [common.arxiv_name_to_bibtex(n) for n in names])
        self.assertEqual(result, "van Dyk, D., Meli\\'{c}, B., and Aaij, R.")

    def test_format_authors_converts_unicode(self):
        self.assertEqual(common.format_authors(['Melić, B.']), "Meli\\'{c}, B.")

    def test_unicode_to_latex_accented_latin(self):
        cases = {
            'Melić': "Meli\\'{c}",
            'Čičić': "\\v{C}i\\v{c}i\\'{c}",
            'François': 'Fran\\c{c}ois',
            'Müller': 'M\\"{u}ller',
            'Łukasz': '\\Lukasz',
            'Øystein': '\\Oystein',
            'Straße': 'Stra\\sse',
            'µ': '\\mu',
        }
        for src, expected in cases.items():
            self.assertEqual(common.unicode_to_latex(src), expected, src)

    def test_unicode_to_latex_handles_decomposed_input(self):
        self.assertEqual(common.unicode_to_latex('e\u0301'), "\\'{e}")

    def test_validator_flags_non_ascii_author(self):
        with tempfile.NamedTemporaryFile(
                mode='w', suffix='.json', encoding='utf-8') as f:
            json.dump({'author': 'Melić'}, f)
            f.flush()
            issues = json_valid.validate_json(f.name)
        self.assertTrue(any('author' in i and 'non-ASCII' in i for i in issues))


class FakeResponse:
    """urlopen() stand-in supporting the context-manager protocol."""

    def __init__(self, payload: bytes):
        self._payload = payload

    def read(self):
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class ExternalMetadataTests(unittest.TestCase):
    def test_inspire_arxiv_link_old_style_id_no_double_prefix(self):
        hit = {'metadata': {
            'control_number': '123', 'texkeys': ['Boyd:1995bx'],
            'arxiv_eprints': [{'value': 'hep-ph/9504235', 'categories': ['hep-ph']}],
        }}
        link = inspirehep_ext.extract_metadata(hit)['arxiv_link']
        self.assertEqual(link, '[hep-ph/9504235](https://arxiv.org/pdf/hep-ph/9504235)')

    def test_inspire_arxiv_link_new_style_id_keeps_category(self):
        hit = {'metadata': {
            'control_number': '123', 'texkeys': ['LHCb:2015svh'],
            'arxiv_eprints': [{'value': '1512.04442', 'categories': ['hep-ex']}],
        }}
        link = inspirehep_ext.extract_metadata(hit)['arxiv_link']
        self.assertEqual(link, '[hep-ex/1512.04442](https://arxiv.org/pdf/1512.04442)')

    def test_arxiv_output_filename_sanitizes_old_style_id(self):
        info = {
            'title': 'T', 'author_str': 'A', 'published': '', 'time': '',
            'primary_category': 'hep-ph', 'arxiv_id_with_version': 'hep-ph/9504235v1',
            'categories': ['hep-ph'], 'journal_ref': '', 'doi': '', 'comment': '',
            'pdf_url': '', 'abs_url': '',
        }
        with tempfile.TemporaryDirectory() as directory:
            args = ['arxiv-ext.py', 'hep-ph/9504235', '--output_dir', directory, '--no-pdf']
            with patch.object(arxiv_ext.sys, 'argv', args), \
                    patch.object(arxiv_ext, 'get_arxiv_info', return_value=info):
                arxiv_ext.main()
            self.assertEqual(os.listdir(directory), ['hep-ph_9504235_arxiv.json'])

    def test_inspire_output_filename_stays_inside_output_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            args = ['inspirehep-ext.py', '--recid', '123', '--output_dir', directory]
            metadata = {
                'texkey': '../../outside', 'recid': '123', 'title': '',
                'author_str': '', 'collaboration': '', 'time': '',
                'journal': '', 'journal_volume': '', 'journal_year': '',
                'doi': '', 'citation_count': 0, 'citation_without_self': 0,
                'inspire_hep_link': '', 'arxiv_link': '',
            }
            with patch.object(inspirehep_ext.sys, 'argv', args), \
                    patch.object(inspirehep_ext, 'get_inspire_by_recid', return_value={}), \
                    patch.object(inspirehep_ext, 'extract_metadata', return_value=metadata):
                inspirehep_ext.main()

            files = os.listdir(directory)
            self.assertEqual(files, ['outside_inspire.json'])

    def test_inspire_search_selects_matching_arxiv_id(self):
        payload = {
            'hits': {'hits': [
                {'metadata': {'arxiv_eprints': [{'value': '9999.00001'}]}},
                {'metadata': {'arxiv_eprints': [{'value': '1512.04442'}]}},
            ]}
        }
        response = FakeResponse(json.dumps(payload).encode('utf-8'))
        with patch.object(common.urllib.request, 'urlopen', return_value=response):
            hit = inspirehep_ext.get_inspire_by_arxiv('1512.04442v2')
        self.assertEqual(hit['metadata']['arxiv_eprints'][0]['value'], '1512.04442')

    def test_arxiv_entry_without_id_raises_actionable_error(self):
        xml = '''<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
          <entry><published>2020-01-01</published><updated>2020-01-01</updated>
          <title>Title</title><summary>Abstract</summary></entry></feed>'''
        response = FakeResponse(xml.encode('utf-8'))
        with patch.object(common.urllib.request, 'urlopen', return_value=response):
            with self.assertRaisesRegex(ValueError, 'missing atom:id'):
                arxiv_ext.get_arxiv_info('2001.00001')

    def test_texkey_path_separators_are_sanitized(self):
        source = (IMPORTER_ROOT / 'scripts' / 'inspirehep-ext.py').read_text(encoding='utf-8')
        self.assertIn("re.sub(r'[^A-Za-z0-9._-]', '_', info['texkey'])", source)


class SharedHelperTests(unittest.TestCase):
    def test_open_url_normalizes_http_error(self):
        error = urllib.error.HTTPError('https://x', 404, 'Not Found', None, None)
        with patch.object(common.urllib.request, 'urlopen', side_effect=error):
            with self.assertRaisesRegex(ValueError, r'arXiv API request failed \(HTTP 404\)'):
                with common.open_url('https://x', label='arXiv API'):
                    pass

    def test_open_url_normalizes_connection_error(self):
        error = urllib.error.URLError('timed out')
        with patch.object(common.urllib.request, 'urlopen', side_effect=error):
            with self.assertRaisesRegex(ValueError, 'InspireHEP API connection failed: timed out'):
                with common.open_url('https://x', label='InspireHEP API'):
                    pass

    def test_open_url_closes_response(self):
        response = FakeResponse(b'body')
        with patch.object(common.urllib.request, 'urlopen', return_value=response):
            with common.open_url('https://x', label='arXiv API') as r:
                self.assertEqual(r.read(), b'body')

    def test_write_json_creates_parents_and_keeps_unicode(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, 'nested', 'sub', 'out.json')
            common.write_json(path, {'title': 'B \\to K', 'n': 1})
            text = Path(path).read_text(encoding='utf-8')
            self.assertIn('\n    "title"', text)
            self.assertEqual(json.loads(text), {'title': 'B \\to K', 'n': 1})


class ImporterDocumentationTests(unittest.TestCase):
    def test_skill_api_references_match_script_contract(self):
        skill = (IMPORTER_ROOT / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn("meta['recid']", skill)
        self.assertNotIn("meta['inspire_recid']", skill)
        self.assertIn('matrix_type, matrix, qualifiers = hepdata_ext.parse_yaml_correlation', skill)
        self.assertIn('transition-mode": "semileptonic-decay"', skill)
        self.assertLess(skill.index('"transition-mode": "semileptonic-decay"'), skill.index('"data": [', skill.index('"transition-mode": "semileptonic-decay"')))


class HepDataImporterTests(unittest.TestCase):
    def test_detect_table_type_matrix_without_header(self):
        yaml_text = (
            "dependent_variables:\n"
            "- header: {name: ''}\n"
            "  values: [{value: 1.0}, {value: 0.0}, {value: 0.0}, {value: 1.0}]\n"
        )
        self.assertEqual(hepdata_ext.detect_table_type(yaml_text), 'correlation')

    def test_detect_table_type_observable_with_axis_not_matrix(self):
        yaml_text = (
            "dependent_variables:\n"
            "- header: {name: 'DSIG/DQ2'}\n"
            "  values: [{value: 1}, {value: 2}, {value: 3}, {value: 4}]\n"
            "independent_variables:\n"
            "- header: {name: 'Q2'}\n"
            "  values: [{value: 1}, {value: 2}, {value: 3}, {value: 4}]\n"
        )
        self.assertEqual(hepdata_ext.detect_table_type(yaml_text), 'observable')

    def test_detect_table_type_covariance_header(self):
        yaml_text = (
            "dependent_variables:\n"
            "- header: {name: 'Covariance'}\n"
            "  values: [{value: 0.25}]\n"
        )
        self.assertEqual(hepdata_ext.detect_table_type(yaml_text), 'covariance')

    def test_download_metadata_skips_derived_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            summary = Path(directory) / 'hepdata_summary.json'
            summary.write_text(json.dumps({
                'record': {'inspire_id': '1409497'}, 'total_tables': 0,
            }), encoding='utf-8')
            real = Path(directory) / 'metadata.json'
            real.write_text(json.dumps({
                'inspire_id': '1409497', 'data_tables': [{'name': 'Table 1'}],
            }), encoding='utf-8')
            with patch.object(hepdata_ext, 'HEPDATA_CLI', '/fake/hepdata-cli'):
                result = hepdata_ext.download_metadata('1409497', directory)
            self.assertEqual(result, str(real))

    def test_download_metadata_ignores_unrelated_existing_json(self):
        with tempfile.TemporaryDirectory() as directory:
            stale = Path(directory) / 'old.json'
            stale.write_text(json.dumps({'inspire_id': '111'}), encoding='utf-8')

            def download(*args, **kwargs):
                fresh = Path(directory) / '1409497.json'
                fresh.write_text(json.dumps({'inspire_id': '1409497'}), encoding='utf-8')
                return type('Result', (), {'returncode': 0, 'stdout': '', 'stderr': ''})()

            with patch.object(hepdata_ext, 'HEPDATA_CLI', '/fake/hepdata-cli'), \
                    patch.object(hepdata_ext.subprocess, 'run', side_effect=download):
                result = hepdata_ext.download_metadata('1409497', directory)

            self.assertEqual(result, str(Path(directory) / '1409497.json'))

    def test_no_write_runs_summary_without_writing_output_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory) / 'output'
            args = ['hepdata-ext.py', '1409497', '--output_dir', str(output_dir), '--no-write']
            metadata = {
                'record': {'title': 'Paper', 'arxiv_id': '', 'doi': '', 'collaborations': []},
                'total_tables': 0,
                'observable_tables': [],
                'correlation_tables': [],
            }
            with patch.object(hepdata_ext, 'HEPDATA_CLI', '/fake/hepdata-cli'), \
                    patch.object(hepdata_ext.sys, 'argv', args), \
                    patch.object(hepdata_ext, 'fetch_table_names', return_value=[]), \
                    patch.object(hepdata_ext, 'download_metadata', return_value='/tmp/metadata.json'), \
                    patch.object(hepdata_ext, 'parse_metadata', return_value=metadata):
                self.assertEqual(hepdata_ext.main(), 0)

            self.assertFalse(output_dir.exists())


class ArxivSourceTests(unittest.TestCase):
    def test_unpack_source_extracts_archive_and_lists_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / 'src.tar.gz'
            with tarfile.open(archive, 'w:gz') as tar:
                for name, payload in (
                    ('main.tex', b'\\documentclass{article}'),
                    ('anc/coeffs.dat', b'0.404 0.013\n'),
                ):
                    info = tarfile.TarInfo(name)
                    info.size = len(payload)
                    tar.addfile(info, io.BytesIO(payload))

            files = arxiv_ext.unpack_source(
                str(archive), str(root / 'out')
            )

            self.assertEqual(files, ['anc/coeffs.dat', 'main.tex'])
            self.assertTrue((root / 'out' / 'anc' / 'coeffs.dat').exists())

    def test_unpack_source_rejects_path_traversal(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / 'src.tar.gz'
            with tarfile.open(archive, 'w:gz') as tar:
                payload = b'escaped'
                info = tarfile.TarInfo('../escaped.txt')
                info.size = len(payload)
                tar.addfile(info, io.BytesIO(payload))

            with self.assertRaises(ValueError):
                arxiv_ext.unpack_source(str(archive), str(root / 'out'))
            self.assertFalse((root / 'escaped.txt').exists())

    def test_unpack_source_handles_single_gzipped_tex(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / '2212.11624_src'
            with gzip.open(archive, 'wb') as f:
                f.write(b'\\documentclass{article}')

            files = arxiv_ext.unpack_source(
                str(archive), str(root / 'out')
            )

            self.assertEqual(files, ['2212.11624.tex'])


if __name__ == '__main__':
    unittest.main()
