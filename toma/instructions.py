"""
CONJUNTO DE INSTRUÇÕES UTILIZADO
Transferência de dados: 4 ciclos
lw
sw

Aritmética/Lógica: 3 ciclos
add
sub
mul
div

Desvio: 2 ciclos
bne

UNIDADES FUNCIONAIS
Load1
Load2
Store1
Store2
Add1
Add2
bne
"""

"""
loop: lw x0, 0(x1)
add x1, x2, x3
sw x1, 0(x2)
sub x2, x1, x3
mul x2, x5, x6
lw x1, 0(x2)
bne x2, x3, loop
div x2, x7, x3
"""

class Instruction:
    def __init__(self, op, dest, vj, vk, label):
        self.op = op
        self.dest = dest
        self.vj = vj
        self.vk = vk
        self.label = label

    def toString(self):
        if self.dest == '':
            return ''
        
        if self.op == "lw" or self.op == "sw":
            return "{} {}, {}".format(self.op, self.dest, self.vj)

        if self.op == "bne":
            return "{} {}, {}, {}".format(self.op, self.vj, self.vk, self.label)

        return "{} {}, {}, {}".format(self.op, self.dest, self.vj, self.vk)

instructions = [
            Instruction("lw", "x0", "0(x1)", "", "loop"),
            Instruction("add", "x1", "x2", "x3", ""),
            Instruction("sw", "x1", "0(x2)", "", ""),
            Instruction("sub", "x2", "x1", "x3", ""),
            Instruction("mul", "x2", "x5", "x6", ""),
            Instruction("lw", "x1", "0(x2)", "", ""),
            Instruction("bne", "x2", "x3", "loop", ""),
            Instruction("div", "x2", "x7", "x3", ""),
        ]
