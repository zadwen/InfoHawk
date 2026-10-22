import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest


class AppTests(unittest.TestCase):
    def test_navigation_and_phone_report(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py')).run(timeout=20)
        self.assertEqual(len(app.exception), 0)
        app.sidebar.radio[0].set_value('Phone').run()
        next(x for x in app.text_input if x.label == 'Target').set_value('+442083661177')
        next(x for x in app.button if x.label == 'Run lookup').click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.session_state['reports']), 1)
        app.sidebar.radio[0].set_value('Reports').run()
        self.assertEqual(len(app.exception), 0)
        next(x for x in app.button if x.label == 'Clear session reports').click().run()
        self.assertEqual(len(app.session_state['reports']), 0)
        for section in ['Domain & DNS', 'Email', 'Username']:
            app.sidebar.radio[0].set_value(section).run()
            self.assertEqual(len(app.exception), 0)

    def test_invalid_input_does_not_create_report(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py')).run()
        next(x for x in app.text_input if x.label == 'Target').set_value('https://bad/path')
        next(x for x in app.button if x.label == 'Run lookup').click().run()
        self.assertEqual(len(app.error), 1)
        self.assertEqual(len(app.session_state['reports']), 0)
