import tempfile
import unittest
from pathlib import Path

from assembler.assembler import assemble_file, assemble_line


class AssembleLineTests(unittest.TestCase):
    def test_assembles_each_supported_instruction(self):
        self.assertEqual(assemble_line("LOAD 5"), "01 05")
        self.assertEqual(assemble_line("ADD 255"), "02 FF")
        self.assertEqual(assemble_line("STORE b"), "03 01")
        self.assertEqual(assemble_line("HALT"), "FF 00")

    def test_ignores_blank_lines_and_comments(self):
        self.assertIsNone(assemble_line("  ; comment only"))
        self.assertEqual(assemble_line(" load 7  ; load a value"), "01 07")

    def test_rejects_unknown_instruction_and_store_target(self):
        with self.assertRaisesRegex(ValueError, "Unknown instruction"):
            assemble_line("JUMP 3")
        with self.assertRaisesRegex(ValueError, "Unknown STORE target"):
            assemble_line("STORE D")

    def test_rejects_missing_or_extra_operands(self):
        for source in ("LOAD", "LOAD 1 2", "STORE", "HALT 0"):
            with self.subTest(source=source):
                with self.assertRaises(ValueError):
                    assemble_line(source)

    def test_rejects_non_decimal_and_out_of_range_values(self):
        for source in ("LOAD abc", "ADD -1", "LOAD 256"):
            with self.subTest(source=source):
                with self.assertRaises(ValueError):
                    assemble_line(source)

    def test_assembles_utf8_file_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "example.asm"
            source.write_text("; نمونه\nLOAD 1\nHALT\n", encoding="utf-8")
            self.assertEqual(assemble_file(source), ["01 01", "FF 00"])


if __name__ == "__main__":
    unittest.main()
