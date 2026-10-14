# assembler.py - تبدیل زبان اسمبلی ساده به بایت‌کد

opcode_table = {
    "LOAD": "01",
    "ADD": "02",
    "STORE": "03",
    "HALT": "FF"
}

variable_table = {
    "A": "00",
    "B": "01",
    "C": "02"
}


def assemble_line(line):
    line = line.split(";", 1)[0].strip()
    if not line:
        return None

    parts = line.split()
    instr = parts[0].upper()
    op = opcode_table.get(instr)
    if op is None:
        raise ValueError(f"Unknown instruction: {instr}")

    if instr == "HALT":
        if len(parts) != 1:
            raise ValueError("HALT does not take an operand")
        operand = "00"
    else:
        if len(parts) != 2:
            raise ValueError(f"{instr} requires exactly one operand")
        arg = parts[1]
        if instr == "STORE":
            operand = variable_table.get(arg.upper())
            if operand is None:
                raise ValueError(f"Unknown STORE target: {arg}")
        else:
            try:
                value = int(arg, 10)
            except ValueError as exc:
                raise ValueError(f"{instr} operand must be a decimal integer") from exc
            if not 0 <= value <= 0xFF:
                raise ValueError(f"{instr} operand must be between 0 and 255")
            operand = f"{value:02X}"

    return f"{op} {operand}"

def assemble_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    bytecode = []
    for line in lines:
        assembled = assemble_line(line)
        if assembled:
            bytecode.append(assembled)

    return bytecode

if __name__ == "__main__":
    bytecode = assemble_file("example.asm")
    with open("program.vdos", "w") as f:
        for line in bytecode:
            f.write(line + "\n")
    print("✅ Bytecode written to program.vdos")
