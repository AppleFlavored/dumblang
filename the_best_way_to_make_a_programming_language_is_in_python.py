from dataclasses import dataclass
from enum import Enum, auto
import os
import subprocess
import sys
from this import d

class TheTokenKindEnum(Enum):
    TheUnknownTokenTokenKind = auto()
    TheIdentifierTokenKind = auto()
    TheStringLiteralTokenKind = auto()
    TheIntegerLiteralTokenKind = auto()
    ThePrintKeyworkTokenKind = auto()

@dataclass
class TheTokenDataStructure:
    theTokenType: TheTokenKindEnum
    theLexeme: str

Location = tuple[str, int, int]

keywords = {
    "print": TheTokenKindEnum.ThePrintKeyworkTokenKind
}

class Lexer:
    def init_lexer(self, filename: str, source: str):
        self.source = source
        self.position = 0
        self.char = self.source[self.position]

        self.filename = filename
        self.line = 1
        self.col = 1

    def advance(self):
        try:
            self.position += 1
            self.col += 1
            self.char = self.source[self.position]
            
            if self.char == '\n':
                self.line += 1
        except IndexError:
            self.position = len(self.source)
            self.char = ''

def scan_tokens(lexer: Lexer):
    while len(lexer.source) > lexer.position:
        while lexer.char.isspace():
            lexer.advance()
        
        ch = lexer.char
        loc: Location = (lexer.filename, lexer.line, lexer.col)

        # Identifier
        if ch.isalpha() or ch == '_':
            start = lexer.position
            while lexer.char.isalnum() or lexer.char == '_':
                lexer.advance()

            ident = lexer.source[start:lexer.position]
            yield TheTokenDataStructure(keywords.get(ident, TheTokenKindEnum.TheIdentifierTokenKind), ident)

        # Integer
        elif ch.isdigit():
            start = lexer.position
            while lexer.char.isdigit():
                lexer.advance()

            yield TheTokenDataStructure(TheTokenKindEnum.TheIntegerLiteralTokenKind, lexer.source[start:lexer.position])

        else:
            lexer.advance()
            
            if ch == '\"':
                start = lexer.position
                while lexer.char != '\"':
                    lexer.advance()
                
                yield TheTokenDataStructure(TheTokenKindEnum.TheStringLiteralTokenKind, lexer.source[start:lexer.position])
                lexer.advance()
            else:
                yield TheTokenDataStructure(TheTokenKindEnum.TheUnknownTokenTokenKind, ch)    

# Because the function name is simply not enough to say what a function does, this
# additional comment will be provided to ensure that everyone is able to understand
# the purpose of this function.
# the_lex_function_is_for_scanning_an_input_file_and_returns_a_list_of_tokens takes an
# input file path as a string, extracts the contents of the file at the provided file path,
# scans the contents for tokens, and returns said tokens.
def the_lex_function_is_for_scanning_an_input_file_and_returns_a_list_of_tokens(path: str) -> list[TheTokenDataStructure]:
    with open(path, 'r', encoding='utf-8') as f:
        contents = f.read()

    lexer = Lexer()
    lexer.init_lexer("", contents)
    tokens = [t for t in scan_tokens(lexer)]

    parse_and_compile_from_token_list(tokens)

class CompilationUnit:
    strings: list[str]
    buffer: list[str]

    def __init__(self):
        self.strings = []
        self.buffer = []

    def add_string(self, string: str) -> str:
        if string not in self.strings:
            self.strings.append(string)

        return "string_{}".format(self.strings.index(string))

    def add_syscall(self, n: int, fd: int, buf: str):
        # ...uhhhhhhhhhhhhh
        # I feel bad for anyone who stumbles upon this code

        idx = int(buf.replace("string_", ""))

        self.buffer.append("mov rax, " + str(n))
        self.buffer.append("mov rdi, " + str(fd))
        self.buffer.append("mov rsi, " + buf)
        self.buffer.append("mov rdx, " + str(len(self.strings[idx]) + 2))
        self.buffer.append("syscall")

    def dump(self, file: str):
        # Finalize the buffer before we dump it.
        self.buffer.append("mov rax, 60")
        self.buffer.append("xor rdi, rdi")
        self.buffer.append("syscall")

        f = open(file, 'w', encoding='utf-8')
        f.write("bits 64\n")
        f.write("global _start\n")

        f.write("section .text\n")
        f.write("_start:\n")
        for entry in self.buffer:
            f.write("    {}\n".format(entry))

        f.write("section .data\n")
        for string in self.strings:
           name = "string_{}".format(self.strings.index(string))
           f.write("    {0}: db \"{1}\", 10, 0\n".format(name, string))

        f.close()

def parse_and_compile_from_token_list(tokens: list[TheTokenDataStructure]):
    unit = CompilationUnit()

    while len(tokens) > 0:
        token = tokens.pop(0)
        if token.theTokenType == TheTokenKindEnum.ThePrintKeyworkTokenKind:
            token = tokens.pop(0)
            if token.theTokenType == TheTokenKindEnum.TheStringLiteralTokenKind:
                reference_name = unit.add_string(token.theLexeme)
                unit.add_syscall(1, 1, reference_name)
            else:
                print("Error: Can only print strings.")
        else:
            print("Unexpected token:", token)

    unit.dump("out.asm")
    subprocess.run(["yasm", "-f", "elf64", "-o", "main.o", "out.asm"])
    subprocess.run(["ld", "-o", "main", "main.o"])
    subprocess.run(["chmod", "+x", "main"])

    os.remove("main.o")

# Every professional program needs very unnecessary comments to describe
# what a function does. This function is the first to be executed will will
# call additional function related to making this epic programming language
# work as intended.
def the_main_function_is_the_start_to_this_epic_programming_language():
    the_lex_function_is_for_scanning_an_input_file_and_returns_a_list_of_tokens("an_example_file_to_test_the_programming_language_made_in_python.testlang")

if __name__ == "__main__":
    the_main_function_is_the_start_to_this_epic_programming_language()