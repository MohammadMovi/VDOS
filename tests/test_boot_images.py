import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NASM = shutil.which("nasm")


@unittest.skipUnless(NASM, "NASM is required to build boot-image examples")
class BootImageTests(unittest.TestCase):
    def test_examples_build_to_512_byte_boot_images(self):
        sources = (
            ROOT / "bootloader" / "boot.asm",
            ROOT / "keyboard_shell" / "shell.asm",
            ROOT / "command_shell" / "shell.asm",
        )
        with tempfile.TemporaryDirectory() as directory:
            for source in sources:
                with self.subTest(source=source.relative_to(ROOT)):
                    output = Path(directory) / f"{source.parent.name}.img"
                    subprocess.run(
                        [NASM, "-f", "bin", str(source), "-o", str(output)],
                        check=True,
                        capture_output=True,
                        text=True,
                    )
                    image = output.read_bytes()
                    self.assertEqual(len(image), 512)
                    self.assertEqual(image[-2:], b"\x55\xAA")


if __name__ == "__main__":
    unittest.main()
