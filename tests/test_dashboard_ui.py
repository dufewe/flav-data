"""Headless UI regressions for the shared dashboard renderer.

Run with the project venv: ``.venv/bin/python -m unittest discover -s tests``.
"""
import pathlib
import sys
import unittest

from streamlit.testing.v1 import AppTest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

PAGE = """
import sys
sys.path.insert(0, {root!r})
from defs import (get_json, month_label, year_min, year_max,
                  EXPERIMENTAL_BASE, THEORETICAL_BASE)
from flav import run_dashboard
run_dashboard({lab!r}, {group!r}, year_min, year_max, get_json,
              month_label=month_label,
              base_path={base!r})
"""


def page(lab, group, base='EXPERIMENTAL_BASE'):
    folder = 'expe-data' if base == 'EXPERIMENTAL_BASE' else 'theo-data'
    src = PAGE.format(root=str(ROOT), lab=lab, group=group,
                      base=str(ROOT / folder))
    return AppTest.from_string(src, default_timeout=60)


def expander_keys(at):
    return [k for k in at.session_state.to_dict() if k.startswith('view_data_')]


def open_expander(at, fragment):
    matches = [k for k in expander_keys(at) if fragment in k]
    if len(matches) != 1:
        raise AssertionError(f'{fragment!r} matched {matches}')
    at.session_state[matches[0]] = True
    return at.run()


def metric(at, label):
    values = [m.value for m in at.metric if m.label == label]
    if len(values) != 1:
        raise AssertionError(f'{label!r} matched {values}')
    return int(values[0])


class DashboardRendering(unittest.TestCase):
    def test_experimental_page_renders(self):
        at = page('CERN', 'LHCb').run()
        self.assertEqual([e.value for e in at.exception], [])
        self.assertGreater(metric(at, 'Total Experiments'), 0)
        self.assertGreater(metric(at, 'Total Observables'), 0)
        self.assertEqual(len(expander_keys(at)),
                         metric(at, 'Total Experiments'))
        self.assertEqual(len(at.table), 0)

    def test_theoretical_page_renders(self):
        at = page('', 'QCD', 'THEORETICAL_BASE').run()
        self.assertEqual([e.value for e in at.exception], [])
        self.assertGreater(metric(at, 'Total Observables'), 0)

    def test_unknown_group_warns(self):
        at = page('CERN', 'NoSuchGroup').run()
        self.assertEqual([e.value for e in at.exception], [])
        self.assertEqual(len(at.warning), 1)
        self.assertIn('No NoSuchGroup data found', at.warning[0].value)


class DashboardInteraction(unittest.TestCase):
    def setUp(self):
        self.at = page('CERN', 'LHCb').run()
        self.assertEqual([e.value for e in self.at.exception], [])

    def test_expander_reveals_observables_and_ratio_channel(self):
        at = open_expander(self.at, 'LHCb:2022vje')
        self.assertEqual([e.value for e in at.exception], [])
        self.assertGreater(len(at.table), 0)
        channels = [m.value for m in at.markdown if m.value.startswith('- **')]
        self.assertTrue(
            any('.MU_I??_1+n_0.mu_I??_1+n_0/' in c and
                '.E_I??_1+n_0.e_I??_1+n_0' in c for c in channels),
            'the R(K)/R(K*) ratio channel is not rendered as a full '
            'numerator/denominator key',
        )

    def test_correlation_matrix_is_rendered(self):
        at = open_expander(self.at, 'LHCb:2022vje')
        labels = [m.value for m in at.markdown if 'CORRELATION' in m.value.upper()]
        self.assertTrue(labels, 'no correlation matrix label rendered')

    def test_transition_filter_shrinks_the_sample(self):
        before = metric(self.at, 'Total Experiments')
        at = self.at.checkbox(key='tx_semileptonic-decay').uncheck().run()
        self.assertEqual([e.value for e in at.exception], [])
        self.assertLess(metric(at, 'Total Experiments'), before)

    def test_year_range_filter_shrinks_the_sample(self):
        before = metric(self.at, 'Total Experiments')
        slider = self.at.slider[0]
        low, high = slider.value
        at = slider.set_value((high, high)).run()
        self.assertEqual([e.value for e in at.exception], [])
        self.assertLess(metric(at, 'Total Experiments'), before)
        self.assertGreater(metric(at, 'Total Experiments'), 0)
        self.assertNotEqual((low, high), (high, high))


if __name__ == '__main__':
    unittest.main()