"""CLI contracts for a compact ADR collection containing only current decisions."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

VALIDATOR = Path(__file__).resolve().parents[1] / 'scripts' / 'validate-adrs.py'


class CurrentDecisionsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.adrs = self.root / 'docs' / 'adr'
        self.adrs.mkdir(parents=True)

    def record(self, number, status='accepted', extra=''):
        filename = f'{number:04d}-boundary.md'
        (self.adrs / filename).write_text(
            f'---\nid: ADR-{number:04d}\ntitle: Boundary\nstatus: {status}\n'
            f'date: 2026-01-01\n{extra}---\n\nCurrent design constraint.\n'
        )
        return filename

    def index(self, *names):
        (self.adrs / 'README.md').write_text('\n'.join(f'[Decision]({n})' for n in names))

    def validate(self):
        run = subprocess.run(
            [sys.executable, str(VALIDATOR), '--root', str(self.root), '--json', '--strict'],
            capture_output=True, text=True,
        )
        return run.returncode, json.loads(run.stdout)

    def test_obsolete_documents_are_rejected(self):
        for status in ('superseded', 'deprecated', 'rejected'):
            with self.subTest(status=status):
                self.index(self.record(1, status))
                code, report = self.validate()
                self.assertEqual(code, 1, report)
                self.assertTrue(any('status' in e for e in report['errors']))

    def test_supersession_metadata_cannot_keep_an_archive_chain(self):
        self.index(self.record(1, extra='supersedes: []\n'))
        code, report = self.validate()
        self.assertEqual(code, 1, report)
        self.assertTrue(any('supersedes' in e for e in report['errors']))

    def test_consolidation_requires_repairing_index_and_code_links(self):
        surviving = self.record(1)
        self.index(surviving, '0003-old-boundary.md')
        source = self.root / 'app.py'
        source.write_text('# @decision ADR-0003\n')
        code, report = self.validate()
        self.assertEqual(code, 1, report)
        self.assertTrue(any('links to missing ADR' in e for e in report['errors']))
        self.assertTrue(any('@decision ADR-0003' in e for e in report['errors']))
        self.index(surviving)
        source.write_text('# @decision ADR-0001\n')
        code, report = self.validate()
        self.assertEqual(code, 0, report)


if __name__ == '__main__':
    unittest.main()
