# Contributing to VDOS

Thanks for helping improve VDOS. It is an educational prototype, so small, focused changes with a clear explanation are especially useful.

## Before you start

1. Check the README and open issues to see what already exists.
2. For a bug, include the exact command, expected result, and actual result. For a larger feature, open an issue first so the scope can be agreed on.
3. Keep changes focused on one behavior. Avoid committing generated `.img` or `.vdos` files unless the change specifically updates a checked-in example artifact.

## Set up and run checks

Requirements depend on the area you change:

- Python 3 for the assembler, VM, and unit tests
- NASM for boot-image checks and assembly examples
- QEMU for manually trying bootable images

Run the automated checks from the repository root:

```sh
python -m unittest discover -s tests -v
```

Boot-image tests are skipped when NASM is unavailable. The GitHub Actions workflow installs NASM and runs the complete suite for every pull request.

To try a boot image manually, assemble it and launch it with QEMU. For example:

```sh
nasm -f bin bootloader/boot.asm -o vdos-boot.img
qemu-system-x86_64 -drive format=raw,file=vdos-boot.img
```

The automated check validates image size and boot signature; it does not prove that the image behaves correctly in an emulator. Include QEMU version and observed behavior in a pull request when changing real-mode assembly.

## Pull request checklist

- [ ] The change has a focused description and links the issue it addresses.
- [ ] Tests cover the changed behavior, or the pull request explains why a test is not practical.
- [ ] `python -m unittest discover -s tests -v` passes locally.
- [ ] Assembly changes were built with NASM; emulator behavior was checked when relevant.
- [ ] Documentation and example commands match the updated behavior.
- [ ] No credentials, personal data, or unrelated generated files are included.

Use a short, descriptive title such as `Fix STORE operand validation` or `Bound command input buffer`.

## Current license status

The repository does not currently contain a `LICENSE` file. Please do not assume that public visibility grants permission to reuse or redistribute the project. The maintainer should choose and add a license before representing VDOS as open-source software.
