import json
import sys
import unittest
from unittest.mock import Mock, patch
import dns.resolver
import dns.exception
import requests
from autosave import make_report, export_json
from modules.utils import domain_name, email_address, username
from modules.domainrecon import lookup
from modules.emailintel import analyze as analyze_email
from modules.phonelookup import analyze as analyze_phone
from modules.leaksearch import check_breaches
from modules.runners import run_tool


class CoreTests(unittest.TestCase):
    def test_validation(self):
        self.assertEqual(domain_name(' EXAMPLE.com. '), 'example.com')
        self.assertEqual(domain_name('bücher.de'), 'xn--bcher-kva.de')
        for value in ['https://example.com/a', '-x.com', '127.0.0.1', 'a..com', 'x.com;id']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                domain_name(value)
        for value in ['--help', 'x;id', 'a/b']:
            with self.assertRaises(ValueError):
                username(value)
        self.assertEqual(email_address('person@example.com'), 'person@example.com')

    def test_dns_statuses(self):
        resolver = Mock()
        resolver.resolve.side_effect = [dns.resolver.NoAnswer(), dns.exception.Timeout()]
        result = lookup('example.com', resolver, ('MX', 'TXT'))
        self.assertEqual(result['records']['MX']['status'], 'no_records')
        self.assertEqual(result['records']['TXT']['status'], 'timeout')
        resolver.resolve.side_effect = dns.resolver.NXDOMAIN()
        self.assertEqual(lookup('example.com', resolver)['records']['A']['status'], 'domain_not_found')

    def test_null_mx(self):
        with patch('modules.emailintel.lookup', return_value={'records': {'MX': {'values': ['0 .']}}}):
            self.assertIn('does not accept', analyze_email('person@example.com')['mail_assessment'])

    def test_phone(self):
        result = analyze_phone('+442083661177', 'GB')
        self.assertTrue(result['valid_pattern'])
        self.assertEqual(result['region'], 'GB')
        with self.assertRaises(ValueError):
            analyze_phone('not a number')

    def test_hibp_statuses_and_secrets(self):
        for code, expected in [(404, 'not_found'), (401, 'api_error'), (403, 'api_error'),
                               (429, 'rate_limited'), (503, 'api_error')]:
            response = Mock(status_code=code, headers={'Retry-After': '5'})
            get = Mock(return_value=response)
            result = check_breaches('person@example.com', 'secret-key', get)
            self.assertEqual(result['status'], expected)
            self.assertNotIn('secret-key', json.dumps(result))
            self.assertFalse(get.call_args.kwargs['allow_redirects'])
        get = Mock(side_effect=requests.Timeout())
        self.assertEqual(check_breaches('person@example.com', 'key', get)['status'], 'connection_failed')
        with self.assertRaises(ValueError):
            check_breaches('person@example.com', '')

    def test_hibp_payload(self):
        response = Mock(status_code=200)
        response.json.return_value = [{'Name': 'Example', 'Description': '<script>bad</script>'}]
        result = check_breaches('person@example.com', 'key', Mock(return_value=response))
        self.assertEqual(result['breaches'][0]['Name'], 'Example')
        self.assertNotIn('Description', result['breaches'][0])
        response.json.return_value = {'error': 'wrong shape'}
        self.assertEqual(check_breaches('person@example.com', 'key', Mock(return_value=response))['status'], 'invalid_response')

    def test_optional_runner(self):
        with patch('modules.runners.shutil.which', return_value=None):
            self.assertEqual(run_tool('sherlock', 'testuser')['status'], 'not_installed')
        with self.assertRaises(ValueError):
            run_tool('sherlock', '--help')
        with patch('modules.runners.shutil.which', return_value='/bin/tool'), \
             patch('modules.runners.subprocess.Popen') as popen:
            import io
            proc = popen.return_value
            proc.stdout = io.BytesIO(b'found profile\n')
            proc.returncode = 0
            result = run_tool('holehe', 'person@example.com')
            self.assertEqual(result['status'], 'ok')
            self.assertEqual(popen.call_args.args[0], ['/bin/tool', 'person@example.com'])
            self.assertNotIn('shell', popen.call_args.kwargs)

    def test_runner_real_timeout_and_output_limit(self):
        import subprocess
        real_popen = subprocess.Popen
        with patch('modules.runners.shutil.which', return_value=sys.executable):
            def noisy(args, **kwargs):
                return real_popen([sys.executable, '-c', 'print("x" * 200000)'], **kwargs)
            with patch('modules.runners.subprocess.Popen', side_effect=noisy):
                result = run_tool('sherlock', 'sample', timeout=5)
                self.assertTrue(result['output_truncated'])
                self.assertEqual(len(result['output']), 128 * 1024)
            def slow(args, **kwargs):
                return real_popen([sys.executable, '-c', 'import time; time.sleep(30)'], **kwargs)
            with patch('modules.runners.subprocess.Popen', side_effect=slow):
                self.assertEqual(run_tool('sherlock', 'sample', timeout=0.1)['status'], 'timeout')

    def test_report(self):
        report = make_report('Phone', 'sample', {'valid_pattern': False})
        self.assertEqual(json.loads(export_json(report)), report)
        self.assertTrue(report['created_at'].endswith('+00:00'))


if __name__ == '__main__':
    unittest.main()
