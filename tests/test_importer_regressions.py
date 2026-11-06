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
        source = PROJECT_ROOT / 'tests/Experimental/CERN-LHCb/2015/12/LHCb:2015svh.json'
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
        for name in ('FL', 'RBr[mu/e]', 'DeltaACP[mu-e]', 'Vcb(CLN)', 'f+.Vcs'):
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


class StreamlitMissingDirectoryTests(unittest.TestCase):
    def test_hflav_page_loads_latest_year_indexed_snapshot(self):
        source = (PROJECT_ROOT / 'Experimental/HFLAV/HFLAV.py').read_text(encoding='utf-8')
        self.assertIn('f"HFLAV@{year}.json"', source)
        self.assertIn('latest_year = candidate_years[0]', source)

    def test_snapshot_pages_guard_missing_directories(self):
        for relative_path in (
            'Experimental/HFLAV/HFLAV.py',
            'Experimental/PDG/PDG.py',
        ):
            source = (PROJECT_ROOT / relative_path).read_text(encoding='utf-8')
            guard = 'if not os.path.isdir(base_dir):'
            listing = 'os.listdir(base_dir)'
            self.assertIn(guard, source, relative_path)
            self.assertLess(source.index(guard), source.index(listing), relative_path)


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
        self.assertLess(skill.index('"transition-mode": "semileptonic-decay"'), skill.index('"data": {', skill.index('"transition-mode": "semileptonic-decay"')))


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
