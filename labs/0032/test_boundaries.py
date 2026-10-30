import json
import stat
import unittest
import zipfile
from boundaries import EXPECTED, archive, consume, injection_demo

REPORT = json.dumps({"schema": 1, "passed": 3, "total": 3})


class BoundaryTests(unittest.TestCase):
    def test_shell_data_boundary(self):
        self.assertEqual(injection_demo()[1], "safe: exact text preserved; marker absent")

    def test_data_only_report(self):
        self.assertEqual(consume(archive([("report.json", REPORT)]), EXPECTED),
                         "report: 3/3 checks passed (data only)")

    def test_wrong_run_even_with_success(self):
        wrong = dict(EXPECTED, run_id=321)
        with self.assertRaisesRegex(ValueError, "producer"):
            consume(archive([("report.json", REPORT)]), wrong)

    def test_path_and_executable_rejected(self):
        for name in ["../report.json", "/report.json", "build.sh", "folder/report.json"]:
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "exactly"):
                consume(archive([(name, REPORT)]), EXPECTED)

    def test_extra_file_rejected(self):
        with self.assertRaisesRegex(ValueError, "exactly"):
            consume(archive([("report.json", REPORT), ("script.sh", ":")]), EXPECTED)

    def test_schema_rejects_bool_and_extra_keys(self):
        for report in [{"schema": 1, "passed": True, "total": 3},
                       {"schema": 1, "passed": 4, "total": 3},
                       {"schema": 1, "passed": 3, "total": 3, "command": ":"}]:
            with self.subTest(report=report), self.assertRaisesRegex(ValueError, "schema"):
                consume(archive([("report.json", json.dumps(report))]), EXPECTED)

    def test_symlink_and_size_rejected(self):
        link = zipfile.ZipInfo("report.json")
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        for entry in [(link, "outside"), ("report.json", " " * 1025)]:
            with self.assertRaisesRegex(ValueError, "symlink or oversized"):
                consume(archive([entry]), EXPECTED)


if __name__ == "__main__":
    unittest.main()
