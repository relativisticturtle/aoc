from collections import deque, defaultdict


#       MNEM,  READ_V, F(V), Assignment ADDR, Conditional JMP ADDR,
NORMAL_OP = {
    1: ('ADD', [0, 1], lambda V: V[0] + V[1], 2, None, lambda S: " + ".join(S)),
    2: ('MUL', [0, 1], lambda V: V[0] * V[1], 2, None, lambda S: " * ".join(S)),
    5: ('JNZ', [0, 1], lambda V: V[0] != 0, None, lambda pos, v: v, None),
    6: ('JZ ', [0, 1], lambda V: V[0] == 0, None, lambda pos, v: v, None),
    7: ('LES', [0, 1], lambda V: V[0] < V[1], 2, None, lambda S: " < ".join(S)),
    8: ('EQU', [0, 1], lambda V: V[0] == V[1], 2, None, lambda S: " == ".join(S)),
}


def get_op(code, pos):
    # Probably the operation is already known,
    # we need to know the parameter mode
    opcode = "%09d" % code[pos]
    modes = opcode[-3::-1]
    op = int(opcode[-2:])
    return op, modes


def consume_args(code, pos, r_base, N):
    _, modes = get_op(code, pos)

    V = list()
    for n in N:
        if modes[n] == "0":
            V.append(code[code[pos + 1 + n]])
        elif modes[n] == "1":
            V.append(code[pos + 1 + n])
        elif modes[n] == "2":
            V.append(code[code[pos + 1 + n]+r_base])
        else:
            assert False
    return V


def print_args(code, pos, r_base, N):
    _, modes = get_op(code, pos)

    S = list()
    for n in N:
        if modes[n] == "0":
            S.append("C[%d]" % code[pos + 1 + n])
        elif modes[n] == "1":
            S.append("%d" % code[pos + 1 + n])
        elif modes[n] == "2":
            S.append("C[<%d> + %d]" % (r_base, code[pos + 1 + n]))
        else:
            S.append("???")
    return S


def print_addr(code, pos, r_base, n):
    _, modes = get_op(code, pos)
    if modes[n] == "0":
        return "C[%d]" % code[pos + 1 + n]
    elif modes[n] == "2":
        return "C[<%d> + %d]" % (r_base, code[pos + 1 + n])
    else:
        return "???"


def write_val(code, pos, r_base, n, val):
    _, modes = get_op(code, pos)
    if modes[n] == "0":
        code[code[pos + 1 + n]] = val
    elif modes[n] == "2":
        code[code[pos + 1 + n]+r_base] = val
    else:
        assert False




class Machine:
    def __init__(self, code):
        self.pos = 0
        self.r_base = 0
        self.code = code.copy() + [0]*10000
        self.input = deque()
        self.output = deque()
        self.halted = False
        self.blocked = True
        self.profiler = defaultdict(int)
        self.breakpoints = dict()

    def set_input(self, input):
        if isinstance(input, deque):
            self.input = input.copy()
        elif isinstance(input, list):
            self.input = deque(input)
        else:
            self.input = input

    def consume_input(self):
        if isinstance(self.input, deque):
            return self.input.popleft() if len(self.input) > 0 else None
        else:
            return self.input

    def push_input(self, input):
        if isinstance(input, list):
            self.input.extend(input)
        else:
            self.input.append(input)

    def pop_output(self):
        output = list(self.output)
        self.output.clear()
        return output

    def goto(self, pos):
        self.pos = pos
        self.profiler[self.pos] += 1
        if self.pos in self.breakpoints:
            self.breakpoints[self.pos](self)

    def step_forward(self):
        op, modes = get_op(self.code, self.pos)

        if op == 99:
            self.halted = True
            return None
        elif op == 3:
            inp = self.consume_input()
            if inp is not None:
                write_val(self.code, self.pos, self.r_base, 0, inp)
                self.goto(self.pos + 2)
                return None
            else:
                self.blocked = True
                return None
        elif op == 4:
            V = consume_args(self.code, self.pos, self.r_base, [0])
            self.output.append(V[0])
            self.goto(self.pos + 2)
            return None
        elif op == 9:
            V = consume_args(self.code, self.pos, self.r_base, [0])
            self.r_base += V[0]
            self.goto(self.pos + 2)
            return None
        elif op in NORMAL_OP:
            OP = NORMAL_OP[op]

            # Read args
            V = consume_args(self.code, self.pos, self.r_base, OP[1])

            # Calculate (maybe...)
            val = OP[2](V) if OP[2] else None
            assert val is not None

            # Write value (maybe...)
            if OP[3] is not None:
                write_val(self.code, self.pos, self.r_base, OP[3], val)

            # Update pos
            instruction_length = 1 + len(V) + int(OP[3] is not None)
            if OP[4] and val:  # jump
                self.goto(OP[4](self.pos, V[1]))
            else:  # normal
                self.goto(self.pos + instruction_length)

            return None
        else:
            raise ValueError

    # disasm: [Mnemnomic, args, target, expression]
    def peek_forward(self, pos=None):
        pos = pos if pos is not None else self.pos
        op, modes = get_op(self.code, pos)

        if op == 99:
            instruction_length = 1
            #disasm = "STOP"
            disasm = ["STOP"]
            return instruction_length, disasm
        elif op == 3:
            instruction_length = 2
            if isinstance(self.input, deque):
                I = self.input[0] if len(self.input) > 0 else 9999
            else:
                I = self.input
            try:
                T = print_addr(self.code, pos, self.r_base, 0)
                disasm = ["IN", "%d" % I, T, "%s <-- %d" % (T, I)]
            except IndexError:
                disasm = ["IN", "%d" % I, "C[X]", "C[X] <-- %d" % I]
            return instruction_length, disasm
        elif op == 4:
            instruction_length = 2
            try:
                V = consume_args(self.code, pos, self.r_base, [0])
            except IndexError:
                V = [9999]
            S = print_args(self.code, pos, self.r_base, [0])
            disasm = ["OUT", S[0], "", "%s --> %d" % (S[0], V[0])]
            return instruction_length, disasm
        elif op == 9:
            instruction_length = 2
            try:
                V = consume_args(self.code, pos, self.r_base, [0])
            except IndexError:
                V = [9999]
            S = print_args(self.code, pos, self.r_base, [0])
            disasm = ["ARB", S[0], "", "RB += %d" % V[0]]
            return instruction_length, disasm
        elif op in NORMAL_OP:
            OP = NORMAL_OP[op]

            # Read args
            S = print_args(self.code, pos, self.r_base, OP[1])
            disasm = [OP[0], ", ".join(S), "", ""]

            V = []
            for i, addr in enumerate(OP[1]):
                try:
                    V.extend(consume_args(self.code, pos, self.r_base, [addr]))
                except IndexError:
                    V.append(9999)

            # Calculate (maybe...)
            val = OP[2](V) if OP[2] else None
            assert val is not None

            # Write value (maybe...)
            if OP[3] is not None:
                T = print_args(self.code, pos, self.r_base, [OP[3]])[0]
                #disasm = "%-24s -> %s" % (disasm, T)
                #T = print_addr(self.code, pos, self.r_base, OP[3])
                disasm[2] = T

            # Update pos
            instruction_length = 1 + len(V) + int(OP[3] is not None)
            if OP[4] and val is not None:  # jump
                new_pos = OP[4](pos, V[1])
                disasm[2] = "%d" % val
                disasm[3] = "jump %d" % new_pos if val else "----"
                #disasm = "%-24s      (%s)    --> %7d" % (disasm, "jump" if val else "----", new_pos)

            if OP[5]:
                disasm[3] = "%s = (%s) = %d" % (T, OP[5](S), val)
                #disasm = "%-40s=   %s      =     %d" % (disasm, OP[5](S), val)
            return instruction_length, disasm
        else:
            #return 1, "[%4d]" % self.code[pos]
            return 1, ["[%4d]" % self.code[pos]]

    def run(self, print_code=True):
        self.blocked = False
        while 0 <= self.pos < len(self.code) and not self.blocked and not self.halted:
            if print_code:
                instruction_length, disasm = self.peek_forward()
                print("%5d | %s" % (self.pos, disasm))
            self.step_forward()

    def print(self):
        pos = 0
        while pos < len(self.code):
            instruction_length, disasm = self.peek_forward(pos=pos)
            print("%5d | %s" % (pos, disasm))
            pos += instruction_length

