# Arquivo contendo todas as instruções suportadas pelo MIPS

class MipsInstructions:        
    # Instruções aritméticas
    ADD   = 'add'  # add a, b, c 	a = b + c 	adds signed numbers.
    SUB   = 'sub'  # subtracts signed numbers.
    MUL   = 'mul'  # gives low 32 bits of signed multiplication.
    DIV   = 'div'  # gives quotient of signed division.

    # ADDU  = 'addu' # adds unsigned numbers.
    # SUB_U = 'subu' # Unsigned subtraction
    # MUL_U = 'mulu' # Unsigned multiplication
    # DIV_U = 'divu' # Unsigned division
    # REM   = 'rem'  # gives remainder of signed division.
    # REM_U = 'remu' # Unsigned Remainder of division
    # MHFI  = 'mfhi' # after mul, gives high 32 bits. after div, gives remainder.
    # MFLO  = 'mflo' # after mul, gives low 32 bits. after div, gives quotient.

    # Instruções lógicas
    XOR = 'xor' # a = b ^ c 	bitwise XORs numbers.
    OR  = 'or'  # a = b | c 	bitwise ORs numbers.
    AND = 'and' # a = b & c 	bitwise ANDs numbers.
    
    # Instruções de desvio
    BEQ  = 'beq'  # Branch if Equal
    BNE  = 'bne'  # Branch if Not Equal
    # BLEZ = 'blez' # Branch if Less Than or Equal to Zero
    # BGTZ = 'bgtz' # Branch on Greater Than Zero
    
    # Load
    LW = 'lw' # Load Word
    # Store
    SB = 'sb' # Store Byte
    SH = 'sh' # Store Halfword
    SW = 'sw' # Store Word
    
























    # Shifts
    # SLT = 'slt' # Set to 1 if Less Than
    # SLTI = 'slti' # Set to 1 if Less Than Immediate
    # SLTIU = 'sltiu' # Set to 1 if Less Than Unsigned Immediate
    # SLTU = 'sltu' # Set to 1 if Less Than Unsigned

    # SLL = 'sll' # Logical Shift Left
    # SRL = 'srl' # Logical Shift Right (0-extended)
    # SRA = 'sra' # Arithmetic Shift Right (sign-extended)

































    # Instrucoes que vao na UF de soma
    # INSTRUCOES_ADD = [ADD, ADDU, SUB, SUB_U, NEG, AND, OR, XOR]

    # Instrucoes que vao na UF de mul
    # INSTRUCOES_MUL = [MUL, MUL_U, DIV, DIV_U, REM, REM_U, MHFI, MFLO]

    # Instrucoes de desvio
    # INSTRUCOES_DESVIO = [BEQ, BLEZ, BNE, BGTZ]

    # Instrucoes que vao na UF de memoria
    # INSTRUCOES_MEM  = [LW, SB, SH, SW, SLT, SLTI, SLTIU, SLTU, SLL, SRL, SRA]





















    # Instrucoes que vao na UF de soma
    INSTRUCOES_LOGICAS = [ADD, SUB, AND, OR, XOR]

    # Instrucoes que vao na UF de mul
    # INSTRUCOES_MUL = [MUL, DIV]

    # Instrucoes de desvio
    INSTRUCOES_DESVIO = [BEQ, BNE]

    # Instrucoes que vao na UF de memoria
    INSTRUCOES_MEM  = [LW, SB, SH, SW]
