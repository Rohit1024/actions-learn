import unittest
from contract import cache_key, run


class DataContractTests(unittest.TestCase):
    def test_local_build_and_copy(self):
        run()

    def test_cache_is_not_install(self):
        with self.assertRaisesRegex(ValueError, "MODULE_NOT_FOUND"):
            run(skip_install=True)

    def test_tamper_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            run(tamper=True)

    def test_name_is_part_of_contract(self):
        with self.assertRaisesRegex(ValueError, "artifact name mismatch"):
            run(wrong_name=True)

    def test_key_declares_relevant_inputs(self):
        base = cache_key("Linux", "X64", 24, b"lock-a")
        self.assertEqual(base, cache_key("Linux", "X64", 24, b"lock-a"))
        for args in [("Linux", "ARM64", 24, b"lock-a"), ("Linux", "X64", 26, b"lock-a"), ("Linux", "X64", 24, b"lock-b")]:
            self.assertNotEqual(base, cache_key(*args))


if __name__ == "__main__":
    unittest.main()
