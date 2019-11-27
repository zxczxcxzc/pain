# PAIN: the paint programming language
# based on https://github.com/cslarsen/python-simple-vm
# licensed under public domain

import sys
from PIL import Image
from collections import deque

version = 1

class Stack(deque):
    push = deque.append
    def top(self):
        return self[-1]

class VM:
    def __init__(self, code):
        self.stack = Stack()
        self.instruction = 0
        self.code = code
        self.op_map = {
            "END": self.end,
            "ADD": self.add,
            "SUB": self.sub,
            "MUL": self.mul,
            "DIV": self.div,
            "OUT": self.out,
            "INP": self.inp,
            "IF": self.if_,
            "JMP": self.jmp
        }

    def pop(self):
        return self.stack.pop()

    def push(self, value):
        return self.stack.push(value)

    def top(self):
        return self.stack.top()
    
    def run(self):
        while self.instruction < len(self.code):
            opcode = self.code[self.instruction]
            self.instruction += 1
            self.dispatch(opcode)

    def dispatch(self, op):
        if op in self.op_map:
            self.op_map[op]()
        else:
            self.push(op)

    # OPERATIONS
    def end(self):
        sys.exit()

    def add(self):
        self.push(self.pop() + self.pop())

    def sub(self):
        last = self.pop()
        self.push(self.pop() - last)

    def mul(self):
        self.push(self.pop() * self.pop())

    def div(self):
        last = self.pop()
        self.push(self.pop() / last)

    def out(self):
        sys.stdout.write(chr(self.pop()))
    
    def inp(self):
        self.push(int(input("? ")))

    def if_(self):
        false_clause = self.pop()
        true_clause = self.pop()
        test = self.pop()
        self.push(true_clause if test else false_clause)

    def jmp(self):
        self.instruction = self.pop()

    def equ(self):
        self.push(1 if self.pop() == self.pop() else 0)

def parse(file):
    pix_map = {
        (255, 0, 0): "END",
        (255, 0, 255): "ADD",
        (128, 0, 255): "SUB",
        (0, 0, 255): "MUL",
        (0, 255, 255): "DIV",
        (0, 255, 0): "OUT",
        (128, 255, 0): "INP",
        (255, 255, 0): "IF",
        (255, 128, 0): "JMP"
    }

    im = Image.open(file)
    for y in range(im.size[1]):
        op = 0
        for x in range(im.size[0]):
            pixel = im.getpixel((x, y))
            if pixel == (0, 0, 0):
                op += 2**x
            elif pixel in pix_map:
                op = pix_map.get(pixel)
        code.append(op)
        if(op) == "END":
            break   
        
code = []

print("PAIN interpreter v" + str(version) +"\n")
print("parsing image..")
parse(sys.argv[1])
print("running..\n=========[output]=========")
VM(code).run()
