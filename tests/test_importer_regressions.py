import importlib.util
import json
import os
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

        for name in ('FL(B0.2.Kst0.mu+.mu-)', 'FL(B02Kstmumu)'):
            self.assertTrue(json_valid.validate_observable_name(name), name)

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

    @staticmethod
    def _obs(name):
        return {
            'name': name,
            'value': '1.0',
            'type@1_error': 'stat',
            'type@1_upper': '0.1',
            'type@1_lower': '0.1',
        }

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
            'B0.2.Kst0.mu+.mu-': self._channel(
                self._obs('FL'), self._obs('S3'),
            ),
            'B+.2.K+.mu+.mu-': self._channel(self._obs('FL')),
            'correlation': [[1.0, 0.5, 0.1], [0.5, 1.0, 0.2], [0.1, 0.2, 1.0]],
        }]
        self.assertEqual(self._validate_data(data), [])

    def test_data_group_matrix_dimension_must_cover_all_channels(self):
        data = [{
            'B0.2.Kst0.mu+.mu-': self._channel(
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
            'B0.2.Kst0.mu+.mu-': self._channel(self._obs('FL')),
        }]
        issues = self._validate_data(data)
        self.assertTrue(any('appears after a matrix key' in issue for issue in issues))

    def test_group_method_sits_between_channels_and_matrix(self):
        data = [{
            'B0.2.Kst0.mu+.mu-': self._channel(self._obs('FL')),
            'method': 'maximum likelihood',
            'correlation': [[1.0]],
        }]
        self.assertEqual(self._validate_data(data), [])

    def test_observable_method_is_rejected(self):
        obs = self._obs('FL')
        obs['method'] = 'maximum likelihood'
        issues = self._validate_data([{
            'B0.2.Kst0.mu+.mu-': {'obs@1': obs},
        }])
        self.assertTrue(any("unknown observable field 'method'" in issue for issue in issues))

    def test_group_method_order_is_enforced(self):
        after_matrix = [{
            'B0.2.Kst0.mu+.mu-': self._channel(self._obs('FL')),
            'correlation': [[1.0]],
            'method': 'maximum likelihood',
        }]
        issues = self._validate_data(after_matrix)
        self.assertTrue(any("'method' appears after a matrix key" in issue for issue in issues))

        after_method = [{
            'method': 'maximum likelihood',
            'B0.2.Kst0.mu+.mu-': self._channel(self._obs('FL')),
        }]
        issues = self._validate_data(after_method)
        self.assertTrue(any("appears after 'method'" in issue for issue in issues))

    def test_group_method_must_be_non_empty_string(self):
        data = [{
            'B0.2.Kst0.mu+.mu-': self._channel(self._obs('FL')),
            'method': '',
        }]
        issues = self._validate_data(data)
        self.assertTrue(any('method: must be a non-empty string' in issue for issue in issues))

    def test_legacy_channel_to_group_dict_is_rejected(self):
        issues = self._validate_data({
            'B0.2.Kst0.mu+.mu-': [{'obs@1': self._obs('FL')}],
        })
        self.assertTrue(any('data must be an array of data groups' in issue for issue in issues))

    def test_channel_must_be_observable_object(self):
        for channel in (
            [{'obs@1': self._obs('FL')}],
            [r'$B^{0}\to K^{*0}\mu^{+}\mu^{-}$', {'obs@1': self._obs('FL')}],
        ):
            issues = self._validate_data([{'B0.2.Kst0.mu+.mu-': channel}])
            self.assertTrue(
                any('must be an object of obs@N entries' in issue for issue in issues),
                channel,
            )

    def test_channel_latex_key_is_rejected(self):
        issues = self._validate_data([{
            'B0.2.Kst0.mu+.mu-': {
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
            'B0.2.Kst0.mu+.mu-': {'obs@1': obs},
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
                'B0.2.Kst0.mu+.mu-': self._channel(self._obs('FL')),
            }],
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as f:
            json.dump(doc, f)
            f.flush()
            issues = json_valid.validate_json(f.name)
        self.assertTrue(any("Forbidden field present: 'pdf'" in issue for issue in issues))


class DashboardDataTests(unittest.TestCase):
    def test_skips_invalid_month_keys_and_corrupt_details(self):
        dashboard_path = PROJECT_ROOT / 'flav_dashboard.py'
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
        dashboard_path = PROJECT_ROOT / 'flav_dashboard.py'
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
        dashboard_path = PROJECT_ROOT / 'flav_dashboard.py'
        source = dashboard_path.read_text(encoding='utf-8')
        namespace = {'__name__': 'dashboard_test'}
        exec(compile('from __future__ import annotations\n' + source, str(dashboard_path), 'exec'), namespace)

        obs = {'name': 'BR', 'type@1_error': 'stat',
               'type@1_upper': '0.1', 'type@1_lower': '0.1'}
        group = {'B0.2.mu+.mu-': {'obs@1': obs}, 'type@1_correlation': [[1.0]]}
        self.assertEqual(
            namespace['matrix_label']('type@1_correlation', group),
            'STAT-CORRELATION',
        )


def load_dashboard():
    dashboard_path = PROJECT_ROOT / 'flav_dashboard.py'
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


class ExternalMetadataTests(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
