"""
CONJUNTO DE INSTRUÇÕES UTILIZADO
Transferência de dados
lw                          5 ciclos
sw                          4 ciclos

Aritmética/Lógica
add                         3 ciclos
sub                         3 ciclos
mul                         3 ciclos
div                         3 ciclos

Desvio
bne                         2 ciclos

UNIDADES FUNCIONAIS
Load1
Load2
Store1
Store2
Add1
Add2
Beq1
"""

"""
lw x0, 0(x1) 
add x1, x2, x3  
loop: sw x1, 0(x2)
sub x2, x1, x3
mul x2, x5, x6
lw x7, 0(x2)
bne x2, x3, loop
div x1, x7, x3
sw x8, 0(x9)
sub x5, x1, x6
"""

class Instruction:
    def __init__(self, op, dest, offset, vj, vk, label, remaining_cycles):
        self.op = op
        self.dest = dest
        self.offset = offset
        self.vj = vj
        self.vk = vk
        self.label = label
        self.remaining_cycles = remaining_cycles

    def toString(self):
        if self.op == '':
            return ''
        
        if self.op == "lw":
            return "{} {}, {}({})".format(self.op, self.dest, self.offset, self.vk)

        if self.op == "sw":
            return "{} {}, {}({})".format(self.op, self.vj, self.offset, self.vk)

        if self.op == "bne":
            return "{} {}, {}, {}".format(self.op, self.vj, self.vk, self.dest)

        return "{} {}, {}, {}".format(self.op, self.dest, self.vj, self.vk)

    def checkType(self):
        if self.op == "lw":
            return "Load"
        if self.op == "sw":
            return "Store"
        if self.op == "add" or self.op == "sub" or self.op == "mul" or self.op == "div":
            return "Add"
        return "Beq"

class InstructionDependencies:
    def __init__(self, entry, vj, vk, dest):
        self.entry = entry
        self.dest = dest
        self.vj = vj
        self.vk = vk

    def print(self):
        print("[Entry: {}, Dest: {}, Vj: {}, Vk: {}]".format(self.entry, self.dest, self.vj, self.vk))

"""
Exemplo
loop: lw x0, 0(x1)

{
    op: lw,
    dest: x0,
    offset: 0,
    vj: "",
    vk: x1,
    label: "loop",
    remaining_cycles: 5
}
"""

instructions = [
            Instruction("lw", "x0", "0", "", "x1", "", 5),
            Instruction("add", "x1", "", "x2", "x3", "", 3),
            Instruction("sw", "", "0", "x1", "x2", "loop", 4),
            Instruction("sub", "x2", "", "x1", "x3", "", 3),
            Instruction("mul", "x2", "", "x5", "x6", "", 3),
            Instruction("lw", "x7", "0", "", "x2", "", 5),
            Instruction("bne", "loop", "", "x2", "x3", "", 2),
            Instruction("div", "x1", "", "x7", "x3", "", 3),
            Instruction("sw", "", "0", "x8", "x9", "", 4),
            Instruction("sub", "x5", "", "x1", "x6", "", 3),

            # Instruction("lw", "x0", "0", "", "x1", "", 5),
            # Instruction("add", "x1", "", "x2", "x3", "", 3),
            # Instruction("sw", "", "0", "x1", "x2", "loop", 4),
            # Instruction("sub", "x2", "", "x1", "x3", "", 3),
            # Instruction("mul", "x2", "", "x5", "x6", "", 3),
            # Instruction("lw", "x7", "0", "", "x2", "", 5),
            # Instruction("bne", "loop", "", "x2", "x3", "", 2),
            # Instruction("div", "x1", "", "x7", "x3", "", 3),

            # Instruction("lw", "x0", "0", "", "x1", "", 1),
            # Instruction("add", "x1", "", "x2", "x3", "", 1),
            # Instruction("sw", "", "0", "x1", "x2", "loop", 1),
            # Instruction("sub", "x2", "", "x1", "x3", "", 1),
            # Instruction("mul", "x2", "", "x5", "x6", "", 1),
            # Instruction("lw", "x7", "0", "", "x2", "", 1),
            # Instruction("bne", "loop", "", "x2", "x3", "", 1),
            # Instruction("div", "x1", "", "x7", "x3", "", 1),
            # Instruction("sw", "", "0", "x8", "x9", "", 1),
            # Instruction("sub", "x5", "", "x1", "x6", "", 1),
        ]
