import importlib.util
import gzip
import io
import json
import os
import tarfile
import tempfile
import unittest
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
        for name in ('FL', 'R', 'RBr[mu/e]', 'DeltaACP[mu-e]', 'Vcb(CLN)', 'f+.Vcs'):
            self.assertEqual(json_valid.validate_observable_name(name), [], name)

        for name in ('FL(B0.2.K*0.mu+.mu-)', 'FL(B02K*mumu)'):
            self.assertTrue(json_valid.validate_observable_name(name), name)

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

    def test_vector_meson_names_use_star(self):
        for key in ('B0.2.K*0.mu+.mu-', 'B+.2.K*+.mu+.mu-',
                    'B0.2.D*0.mu+.mu-', 'B+.2.Ds*+.mu+.mu-'):
            self.assertEqual(json_valid.validate_transition_key(key), [], key)

        for key in ('B0.2.Kst0.mu+.mu-', 'B+.2.Kst+.mu+.mu-',
                    'B0.2.Dst0.mu+.mu-', 'B+.2.Dsst+.mu+.mu-'):
            self.assertTrue(json_valid.validate_transition_key(key), key)

    def test_neutrino_tokens_use_v_not_nu(self):
        for key in ('W-.2.mu-.vBar', 'B+.2.K+.v.vBar',
                    'B+.2.mu+.ve', 'B+.2.e+.vmuBar',
                    'B+.2.tau+.vtau'):
            self.assertEqual(json_valid.validate_transition_key(key), [], key)

        for key in ('W-.2.mu-.nuBar', 'B+.2.K+.nu.nuBar',
                    'B+.2.mu+.nue', 'B+.2.e+.numubar',
                    'BBar.2.Xcl.nubar'):
            self.assertTrue(json_valid.validate_transition_key(key), key)

    def test_hadron_tokens_follow_handwritten_case(self):
        for key in ('B0.2.pi0.mu+.mu-', 'Lambdab0.2.p+.pi-.vBar',
                    'B0.2.KS0.v.vBar', 'Sigma+.2.p+.mu+.mu-',
                    'Lambdac+.2.p+.mu+.mu-', 'B0.2.KL0.v.vBar'):
            self.assertEqual(json_valid.validate_transition_key(key), [], key)

        for key in ('B0.2.K0S.v.vBar', 'B0s.2.mu+.mu-',
                    'B0.2.K0bar.v.vBar', 'B0.2.fbar.v.vBar',
                    'B0.2.K0L.v.vBar',
                    'LambdacBar-.2.p+Bar.mu+.mu-',
                    'Lambda0.2.p+bar.vBar'):
            self.assertTrue(json_valid.validate_transition_key(key), key)

    def test_charge_uses_plus_minus_zero(self):
        for key in ('B+.2.K*+.mu+.mu-', 'B-.2.D*0.tau-.vBar',
                    'Bc+.2.J/psi0.l+.v'):
            self.assertEqual(json_valid.validate_transition_key(key), [], key)

        for key in ('Bp.2.K*+.mu+.mu-', 'Bm.2.D0.mu-.vBar',
                    'B+.2.K+.mup.mum', 'B+.2.K+.ep.em',
                    'B+.2.pip.pim', 'B+.2.D*p.D*m',
                    'B+.2.K*p.taup.taum'):
            issues = json_valid.validate_transition_key(key)
            self.assertTrue(issues, key)
            self.assertIn('writes its charge', ' '.join(issues), key)

        # Lowercase antiparticle marker is rejected, capital Bar is accepted.
        self.assertTrue(json_valid.validate_transition_key('B0.2.K*0bar.v.vBar'))
        self.assertEqual(json_valid.validate_transition_key('B0Bar.2.XsBar.e+.e-'), [])

    def test_particle_states_require_an_explicit_charge(self):
        for key in ('p+.p+.2.Z.2.mu+.mu-', 'n0.2.p+.e-.veBar',
                    'Lambda0.2.p+.pi-', 'B0.2.phi0.K*0',
                    'B0.2.J/psi0.K*0', 'H0.2.W+.W-',
                    'B+.2.D*+Bar.mu-.vBar', 'B0Bar.2.K*0Bar.v.vBar'):
            self.assertEqual(json_valid.validate_transition_key(key), [], key)

        for key in ('p.p.2.Z.2.mu+.mu-', 'B0.2.phi.mu+.mu-',
                    'Lambdab0.2.p.J/psi.pi-', 'n.2.p.e-.veBar',
                    'H.2.W.W', 'Lambda.2.p+.vBar',
                    'B0.2.J/psi.K*0', 'B0.2.K*.mu+.mu-',
                    'B+.2.mu.e'):
            issues = json_valid.validate_transition_key(key)
            self.assertTrue(issues, key)
            self.assertIn('no charge marker', ' '.join(issues), key)

    def test_particle_grammar_exemptions(self):
        for key in ('W-.2.mu-.vBar', 'B0.2.K*0.v.vBar',
                    'W-.2.e-.vBar', 'B0.2.KS0.v.vBar',
                    'B0.2.Xs.gamma', 'p+.p+.2.Z.2.l+.l-',
                    'B0.2.K+.l+.v', 'B0.2.D0.q.qBar'):
            self.assertEqual(json_valid.validate_transition_key(key), [], key)

    def test_particle_grammar_placement(self):
        for key, expected in (
            ('B+.2.D+*.e+.ve', 'vector marker'),
            ('B0.2.K*Bar+.mu+.mu-', 'vector marker'),
            ('LambdacBar-.2.p+.mu+.mu-', 'Bar'),
            ('B0.2.K*0bar.v.vBar', 'lowercase'),
        ):
            issues = json_valid.validate_transition_key(key)
            self.assertTrue(issues, key)
            self.assertIn(expected, ' '.join(issues), key)

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

    def _validate_data(self, data_block):
        doc = {
            'inspire-hep': '[Test:2024](https://inspirehep.net/literature/1)',
            'author': 'Doe, J.',
            'title': 'Test',
            'arxiv': '[hep-ex/2401.00001v1](https://arxiv.org/pdf/2401.00001)',
            'time': '2024.01.01',
            'abstract': 'Test abstract.',
            'transition-mode': 'semileptonic-decay',
            'data': data_block,
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as f:
            json.dump(doc, f)
            f.flush()
            return json_valid.validate_json(f.name)

    def test_data_groups_allow_cross_channel_matrices(self):
        data = [{
            'B0.2.K*0.mu+.mu-': self._channel(
                self._obs('FL'), self._obs('S3'),
            ),
            'B+.2.K+.mu+.mu-': self._channel(self._obs('FL')),
            'correlation': [[1.0, 0.5, 0.1], [0.5, 1.0, 0.2], [0.1, 0.2, 1.0]],
        }]
        self.assertEqual(self._validate_data(data), [])

    def test_group_note_acknowledges_out_of_range_correlation(self):
        data = [{
            'B0.2.K*0.mu+.mu-': self._channel(
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
                    'B0.2.K*0.mu+.mu-': self._channel(self._obs('FL')),
                    'note': value,
                }]
                issues = self._validate_data(data)
                self.assertTrue(any('note: must be a non-empty string' in issue
                                    for issue in issues))

    def test_group_note_sits_before_matrix(self):
        data = [{
            'B0.2.K*0.mu+.mu-': self._channel(self._obs('FL')),
            'correlation': [[1.0]],
            'note': 'documented',
        }]
        issues = self._validate_data(data)
        self.assertTrue(any("'note' appears after a matrix key" in issue
                            for issue in issues))

    def test_data_group_matrix_dimension_must_cover_all_channels(self):
        data = [{
            'B0.2.K*0.mu+.mu-': self._channel(
                self._obs('FL'), self._obs('S3'),
            ),
            'B+.2.K+.mu+.mu-': self._channel(self._obs('FL')),
            'correlation': [[1.0, 0.5], [0.5, 1.0]],
        }]
        issues = self._validate_data(data)
        self.assertTrue(any('does not match the 3 observables' in issue for issue in issues))

    def test_data_group_channel_must_precede_matrix(self):
        data = [{
            'correlation': [[1.0]],
            'B0.2.K*0.mu+.mu-': self._channel(self._obs('FL')),
        }]
        issues = self._validate_data(data)
        self.assertTrue(any('appears after a matrix key' in issue for issue in issues))

    def test_group_dataset_sits_between_channels_and_matrix(self):
        data = [{
            'B0.2.K*0.mu+.mu-': self._channel(self._obs('FL')),
            'dataset': 'EXPE',
            'correlation': [[1.0]],
        }]
        self.assertEqual(self._validate_data(data), [])

    def test_group_dataset_accepts_canonical_sources(self):
        for value in ('LQCD', 'LCSR', 'EXPE', 'LQCD+LCSR', 'LQCD+LCSR+EXPE'):
            with self.subTest(dataset=value):
                data = [{
                    'B0.2.K*0.mu+.mu-': self._channel(self._obs('FL')),
                    'dataset': value,
                }]
                self.assertEqual(self._validate_data(data), [])

    def test_group_dataset_rejects_non_source_values(self):
        for value in ('maximum likelihood', 'nominal', 'experiment',
                      'LCSR + LQCD', 'LCSR+LQCD', 'LQCD+LQCD', 'NLO'):
            with self.subTest(dataset=value):
                data = [{
                    'B0.2.K*0.mu+.mu-': self._channel(self._obs('FL')),
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
            'B0.2.K*0.mu+.mu-': {'obs@1': obs},
        }])
        self.assertTrue(any("unknown observable field 'scheme'" in issue for issue in issues))

    def test_group_metadata_order_is_enforced(self):
        after_matrix = [{
            'B0.2.K*0.mu+.mu-': self._channel(self._obs('FL')),
            'correlation': [[1.0]],
            'dataset': 'EXPE',
        }]
        issues = self._validate_data(after_matrix)
        self.assertTrue(any("'dataset' appears after a matrix key" in issue for issue in issues))

        after_dataset = [{
            'dataset': 'EXPE',
            'B0.2.K*0.mu+.mu-': self._channel(self._obs('FL')),
        }]
        issues = self._validate_data(after_dataset)
        self.assertTrue(any("appears after 'dataset'" in issue for issue in issues))

        dataset_after_scheme = [{
            'B0Bar.2.pi+.l-.vBar': self._channel(self._obs('a0_f+')),
            'scheme': 'BCL',
            'dataset': 'LQCD+LCSR',
        }]
        issues = self._validate_data(dataset_after_scheme)
        self.assertTrue(any("'dataset' appears after 'scheme'" in issue for issue in issues))

    def test_group_dataset_must_be_non_empty_string(self):
        data = [{
            'B0.2.K*0.mu+.mu-': self._channel(self._obs('FL')),
            'dataset': '',
        }]
        issues = self._validate_data(data)
        self.assertTrue(any('dataset: must be a non-empty string' in issue for issue in issues))

    def test_coefficient_group_requires_scheme(self):
        data = [{
            'B0Bar.2.pi+.l-.vBar': self._channel(self._obs('a0_f+')),
        }]
        issues = self._validate_data(data)
        self.assertTrue(any(
            "must declare a group-level 'scheme'" in issue
            for issue in issues
        ))

    def test_coefficient_group_accepts_canonical_scheme(self):
        for scheme in ('BGL', 'BCL', 'BSZ', 'DLM'):
            with self.subTest(scheme=scheme):
                data = [{
                    'B0Bar.2.pi+.l-.vBar': self._channel(self._obs('a0_f+')),
                    'dataset': 'LQCD+LCSR',
                    'scheme': scheme,
                    'correlation': [[1.0]],
                }]
                self.assertEqual(self._validate_data(data), [])

    def test_obsolete_form_factor_symbols_are_rejected(self):
        for name in ('a0_fp', 'a1_Fp', 'a2_Gp', 'a0_hp', 'a1_htp'):
            with self.subTest(name=name):
                data = [{
                    'B0Bar.2.pi+.l-.vBar': self._channel(self._obs(name)),
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
                    'B0Bar.2.pi+.l-.vBar': self._channel(self._obs(name)),
                    'dataset': 'LQCD',
                    'scheme': 'BCL',
                }]
                self.assertEqual(self._validate_data(data), [])

    def test_scheme_rejects_long_or_unknown_values(self):
        for value in ('Bourrely-Caprini-Lellouch (arXiv:0807.2722)', 'bcl',
                      'BGL '):
            with self.subTest(scheme=value):
                data = [{
                    'B0Bar.2.pi+.l-.vBar': self._channel(self._obs('a0_f+')),
                    'scheme': value,
                }]
                issues = self._validate_data(data)
                self.assertTrue(any('unsupported value' in issue for issue in issues))

    def test_scheme_order_is_enforced(self):
        after_matrix = [{
            'B0Bar.2.pi+.l-.vBar': self._channel(self._obs('a0_f+')),
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
            'B0Bar.2.pi+.l-.vBar': self._channel(self._obs('a0_f+')),
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
            'B0.2.K*0.mu+.mu-': {'obs@1': obs},
        }])
        self.assertTrue(any(
            'single error must be written as the total error' in issue
            for issue in issues
        ))

    def test_multiple_component_errors_are_accepted(self):
        obs = self._obs_with_components('FL')
        self.assertEqual(self._validate_data([{
            'B0.2.K*0.mu+.mu-': {'obs@1': obs},
        }]), [])

    def test_scale_factor_unit_is_rejected(self):
        for unit in ('1e-6', '10^{-4}', '1E-3', '10^-11'):
            obs = self._obs('Br')
            obs['unit'] = unit
            issues = self._validate_data([{
                'B0.2.K*0.mu+.mu-': {'obs@1': obs},
            }])
            self.assertTrue(
                any('pure scale factor' in issue for issue in issues), unit
            )

        obs = self._obs('Mass')
        obs['unit'] = 'GeV'
        self.assertEqual(self._validate_data([{
            'B0.2.K*0.mu+.mu-': {'obs@1': obs},
        }]), [])

    def test_total_and_component_errors_cannot_mix(self):
        obs = self._obs_with_components('FL')
        obs['total_upper'] = '0.1'
        obs['total_lower'] = '0.1'
        issues = self._validate_data([{
            'B0.2.K*0.mu+.mu-': {'obs@1': obs},
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
            'B0.2.K*0.mu+.mu-': {'obs@1': obs},
        }]), [])

        obs.pop('type@1_level')
        issues = self._validate_data([{
            'B0.2.K*0.mu+.mu-': {'obs@1': obs},
        }])
        self.assertTrue(any(
            "present without 'type@1_level'" in issue for issue in issues
        ))

    def test_combined_fit_and_bound_use_distinct_slots(self):
        obs = self._obs_with_components('Br')
        obs.update({'type@3_upper': '5.9e-6', 'type@3_level': '90%@CLs'})
        self.assertEqual(self._validate_data([{
            'B0.2.K*0.mu+.mu-': {'obs@1': obs},
        }]), [])

        shared = self._obs_with_components('Br')
        shared.update({'type@1_upper': '5.9e-6', 'type@1_level': '90%@CLs'})
        issues = self._validate_data([{
            'B0.2.K*0.mu+.mu-': {'obs@1': shared},
        }])
        self.assertTrue(any(
            "is used both as a component error" in issue for issue in issues
        ))

    def test_legacy_error_fields_are_rejected(self):
        obs = self._obs('FL')
        del obs['total_upper'], obs['total_lower']
        obs.update({'error_upper': '0.1', 'error_lower': '0.1'})
        issues = self._validate_data([{
            'B0.2.K*0.mu+.mu-': {'obs@1': obs},
        }])
        self.assertTrue(any(
            "unknown observable field 'error_upper'" in issue for issue in issues
        ))

    def test_legacy_channel_to_group_dict_is_rejected(self):
        issues = self._validate_data({
            'B0.2.K*0.mu+.mu-': [{'obs@1': self._obs('FL')}],
        })
        self.assertTrue(any('data must be an array of data groups' in issue for issue in issues))

    def test_channel_must_be_observable_object(self):
        for channel in (
            [{'obs@1': self._obs('FL')}],
            [r'$B^{0}\to K^{*0}\mu^{+}\mu^{-}$', {'obs@1': self._obs('FL')}],
        ):
            issues = self._validate_data([{'B0.2.K*0.mu+.mu-': channel}])
            self.assertTrue(
                any('must be an object of obs@N entries' in issue for issue in issues),
                channel,
            )

    def test_channel_latex_key_is_rejected(self):
        issues = self._validate_data([{
            'B0.2.K*0.mu+.mu-': {
                'latex': r'$B^{0}\to K^{*0}\mu^{+}\mu^{-}$',
                'obs@1': self._obs('FL'),
            },
        }])
        self.assertTrue(any("disallowed field 'latex'" in issue for issue in issues))

    def test_no_transition_channel_is_observable_object(self):
        data = [{
            'no-transition': self._channel(self._obs('MZ')),
        }]
        self.assertEqual(self._validate_data(data), [])

    def test_observable_latex_is_rejected(self):
        obs = self._obs('FL')
        obs['latex'] = r'$F_L$'
        issues = self._validate_data([{
            'B0.2.K*0.mu+.mu-': {'obs@1': obs},
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
                'B0.2.K*0.mu+.mu-': self._channel(self._obs('FL')),
            }],
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as f:
            json.dump(doc, f)
            f.flush()
            issues = json_valid.validate_json(f.name)
        self.assertTrue(any("Forbidden field present: 'pdf'" in issue for issue in issues))


    def _validate_snapshot_doc(self, doc):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as f:
            json.dump(doc, f)
            f.flush()
            return json_valid.validate_json(f.name)

    @staticmethod
    def _pdg_snapshot(obs):
        return {
            'inspire-hep': '[PDG:2024](https://inspirehep.net/literature/1)',
            'author': 'Navas, S. and others',
            'collaboration': 'PDG',
            'title': 'Review of Particle Physics',
            'year': '2024',
            'data': {'PDG@W': {'obs@1': obs}},
        }

    def test_pdg_snapshot_accepts_numeric_total_error(self):
        doc = self._pdg_snapshot({
            'name': 'MW', 'value': 80.3692,
            'total_upper': 0.0133, 'total_lower': 0.0133, 'unit': 'GeV',
        })
        self.assertEqual(self._validate_snapshot_doc(doc), [])

    def test_pdg_snapshot_rejects_scalar_error(self):
        doc = self._pdg_snapshot({
            'name': 'MW', 'value': 80.3692, 'error': 0.0133,
        })
        issues = self._validate_snapshot_doc(doc)
        self.assertTrue(any(
            "unknown observable field 'error'" in issue for issue in issues
        ))
        self.assertTrue(any(
            'missing required field: total_upper' in issue for issue in issues
        ))

    def test_pdg_snapshot_requires_numeric_total_error(self):
        doc = self._pdg_snapshot({
            'name': 'MW', 'value': 80.3692,
            'total_upper': '0.0133', 'total_lower': '0.0133',
        })
        issues = self._validate_snapshot_doc(doc)
        self.assertTrue(any(
            'total_upper: must be a number' in issue for issue in issues
        ))

    def test_hflav_snapshot_accepts_numeric_total_error(self):
        doc = {
            'HFLAV@overview': {
                'group': 'HFLAV',
                'inspire-hep': '[HFLAV:2024](https://inspirehep.net/literature/1)',
                'description': 'overview of popular observables',
                'observables': [{
                    'name': 'Tau(B0)', 'value': 1.517,
                    'total_upper': 0.004, 'total_lower': 0.004, 'unit': 'ps',
                }],
                'correlation': None,
            },
        }
        self.assertEqual(self._validate_snapshot_doc(doc), [])


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
        group = {'B0.2.mu+.mu-': {'obs@1': obs}, 'type@1_correlation': [[1.0]]}
        self.assertEqual(
            namespace['matrix_label']('type@1_correlation', group),
            'STAT-CORRELATION',
        )


def load_dashboard():
    dashboard_path = PROJECT_ROOT / 'flav.py'
    namespace = {'__name__': 'dashboard_test'}
    exec(compile('from __future__ import annotations\n' + dashboard_path.read_text(encoding='utf-8'),
                 str(dashboard_path), 'exec'), namespace)
    return namespace


class StreamlitSnapshotTests(unittest.TestCase):
    def test_latest_snapshot_picks_newest_year(self):
        namespace = load_dashboard()
        with tempfile.TemporaryDirectory() as directory:
            for year in ('2023', '2024'):
                folder = Path(directory) / 'HFLAV' / year
                folder.mkdir(parents=True)
                (folder / f'HFLAV@{year}.json').write_text('{}', encoding='utf-8')

            found = namespace['_latest_snapshot'](
                str(Path(directory) / 'HFLAV'), 'HFLAV'
            )

        self.assertEqual(found[0], '2024')
        self.assertTrue(found[1].endswith('HFLAV@2024.json'))

    def test_latest_snapshot_missing_directory_returns_none(self):
        namespace = load_dashboard()
        with tempfile.TemporaryDirectory() as directory:
            missing = str(Path(directory) / 'Missing')
            self.assertIsNone(namespace['_latest_snapshot'](missing, 'HFLAV'))

    def test_latest_snapshot_accepts_flat_snapshot_file(self):
        namespace = load_dashboard()
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / 'PDG'
            folder.mkdir()
            (folder / 'PDG@2022.json').write_text('{}', encoding='utf-8')

            found = namespace['_latest_snapshot'](str(folder), 'PDG')

        self.assertEqual(found[0], '2022')


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
        response = type('Response', (), {
            'read': lambda self: json.dumps(payload).encode('utf-8')
        })()
        with patch.object(inspirehep_ext.urllib.request, 'urlopen', return_value=response):
            hit = inspirehep_ext.get_inspire_by_arxiv('1512.04442v2')
        self.assertEqual(hit['metadata']['arxiv_eprints'][0]['value'], '1512.04442')

    def test_arxiv_entry_without_id_raises_actionable_error(self):
        xml = '''<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
          <entry><published>2020-01-01</published><updated>2020-01-01</updated>
          <title>Title</title><summary>Abstract</summary></entry></feed>'''
        response = type('Response', (), {'read': lambda self: xml.encode('utf-8')})()
        with patch.object(arxiv_ext.urllib.request, 'urlopen', return_value=response):
            with self.assertRaisesRegex(ValueError, 'missing atom:id'):
                arxiv_ext.get_arxiv_info('2001.00001')

    def test_texkey_path_separators_are_sanitized(self):
        source = (IMPORTER_ROOT / 'scripts' / 'inspirehep-ext.py').read_text(encoding='utf-8')
        self.assertIn("re.sub(r'[^A-Za-z0-9._-]', '_', info['texkey'])", source)


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
