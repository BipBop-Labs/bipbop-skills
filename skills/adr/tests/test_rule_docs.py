"""CLI contracts for policy and procedure folders next to the ADR folder."""
from datetime import date
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

VALIDATOR = Path(__file__).resolve().parents[1] / 'scripts' / 'validate-adrs.py'
TODAY = date.today().isoformat()


class RuleDocsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'src').mkdir()
        (self.root / 'src' / 'app.py').write_text('print(1)\n')
        self.adrs = self.root / 'docs' / 'adr'
        self.policies = self.root / 'docs' / 'policies'
        self.procedures = self.root / 'docs' / 'procedures'
        for folder in (self.adrs, self.policies, self.procedures):
            folder.mkdir(parents=True)
        (self.adrs / '0001-boundary.md').write_text(
            '---\nid: ADR-0001\ntitle: Boundary\nstatus: accepted\ndate: 2026-01-01\n---\n\nConstraint.\n'
        )
        (self.adrs / 'README.md').write_text('[Boundary](0001-boundary.md)\n')

    def policy(self, name='product-metrics', extra='', body='Count active users per week. See ADR-0001.\n',
               reviewed=TODAY, review_in='6 months'):
        (self.policies / f'{name}.md').write_text(
            f'---\ntitle: Product metrics\nstatus: accepted\nowner: data\npaths: [src/**]\n'
            f'last_reviewed: {reviewed}\nreview_in: {review_in}\n{extra}---\n\n{body}'
        )
        return f'{name}.md'

    def procedure(self, name='deploy', body='1. Build.\n2. Deploy.\n3. Verify.\n', verified=TODAY):
        (self.procedures / f'{name}.md').write_text(
            f'---\ntitle: Deploy\nowner: ops\ntrigger: release\nlast_verified: {verified}\n---\n\n{body}'
        )
        return f'{name}.md'

    def index(self, folder, *names):
        (folder / 'README.md').write_text('\n'.join(f'[Doc]({n})' for n in names))

    def validate(self, *extra):
        run = subprocess.run(
            [sys.executable, str(VALIDATOR), '--root', str(self.root), '--json', *extra],
            capture_output=True, text=True,
        )
        return run.returncode, json.loads(run.stdout) if run.stdout.startswith('{') else run.stderr

    def test_valid_policy_and_procedure_pass_strict(self):
        self.index(self.policies, self.policy())
        self.index(self.procedures, self.procedure())
        code, report = self.validate('--strict')
        self.assertEqual(code, 0, report)
        self.assertEqual((report['summary']['policies'], report['summary']['procedures']), (1, 1))

    def test_missing_fields_numbered_name_and_unlisted_doc_are_errors(self):
        (self.policies / '0002-metrics.md').write_text('---\ntitle: Metrics\nstatus: accepted\n---\n\nRule.\n')
        self.index(self.policies)
        self.index(self.procedures)
        code, report = self.validate()
        self.assertEqual(code, 1, report)
        errors = ' | '.join(report['errors'])
        self.assertIn('looks like an ADR', errors)
        (self.policies / '0002-metrics.md').unlink()
        (self.policies / 'metrics.md').write_text('---\ntitle: Metrics\nstatus: final\n---\n\nRule.\n')
        code, report = self.validate()
        errors = ' | '.join(report['errors'])
        self.assertEqual(code, 1, report)
        for text in ("'owner'", "'review_in'", "status 'final'", 'does not list metrics.md'):
            self.assertIn(text, errors)

    def test_procedure_needs_numbered_steps(self):
        self.index(self.policies)
        self.index(self.procedures, self.procedure(body='Build it, then deploy it.\n'))
        code, report = self.validate()
        self.assertEqual(code, 1, report)
        self.assertTrue(any('numbered steps' in e for e in report['errors']))

    def test_expired_review_and_stale_paths_are_warnings(self):
        self.index(self.policies, self.policy(reviewed='2020-01-01', extra='', review_in='1 year'))
        self.index(self.procedures, self.procedure(verified='2020-01-01'))
        (self.policies / 'product-metrics.md').write_text(
            (self.policies / 'product-metrics.md').read_text().replace('src/**', 'gone/**')
        )
        code, report = self.validate()
        self.assertEqual(code, 0, report)
        warnings = ' | '.join(report['warnings'])
        self.assertIn('policies/product-metrics.md: expired on 2020-12-31', warnings)
        self.assertIn('procedures/deploy.md: expired', warnings)
        self.assertIn("'gone/**' matches nothing", warnings)
        self.assertEqual(self.validate('--strict')[0], 1)

    def test_broken_adr_mentions_and_links_are_errors(self):
        self.index(self.policies, self.policy(body='See ADR-0009 and [deploy](../procedures/missing.md).\n'))
        self.index(self.procedures)
        code, report = self.validate()
        errors = ' | '.join(report['errors'])
        self.assertEqual(code, 1, report)
        self.assertIn('ADR-0009', errors)
        self.assertIn('missing file ../procedures/missing.md', errors)

    def test_proposed_policy_fails_with_fail_on_proposed(self):
        name = self.policy()
        (self.policies / name).write_text((self.policies / name).read_text().replace('accepted', 'proposed'))
        self.index(self.policies, name)
        self.index(self.procedures)
        self.assertEqual(self.validate()[0], 0)
        code, report = self.validate('--fail-on-proposed')
        self.assertEqual(code, 1, report)

    def test_adrs_only_ignores_other_kinds_and_rule_docs_work_without_adrs(self):
        (self.policies / 'broken.md').write_text('no frontmatter\n')
        code, report = self.validate('--adrs-only')
        self.assertEqual(code, 0, report)
        self.assertEqual(report['summary']['policies'], 0)
        for path in self.adrs.iterdir():
            path.unlink()
        self.adrs.rmdir()
        (self.policies / 'broken.md').unlink()
        self.index(self.policies, self.policy(body='No ADR here.\n'))
        self.index(self.procedures)
        code, report = self.validate()
        self.assertEqual(code, 0, report)
        self.assertEqual(self.validate('--adr-dir', 'docs/adr')[0], 2)


if __name__ == '__main__':
    unittest.main()
