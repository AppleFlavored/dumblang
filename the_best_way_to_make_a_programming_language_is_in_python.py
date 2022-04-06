from dataclasses import dataclass
from enum import Enum, auto

class TheTokenKindEnum(Enum):
    TheIdentifierTokenKind = auto()

@dataclass
class TheTokenDataStructure:
    theTokenType: TheTokenKindEnum
    theLexeme: str

# Because the function name is simply not enough to say what a function does, this
# additional comment will be provided to ensure that everyone is able to understand
# the purpose of this function.
# the_lex_function_is_for_scanning_an_input_file_and_returns_a_list_of_tokens takes an
# input file path as a string, extracts the contents of the file at the provided file path,
# scans the contents for tokens, and returns said tokens.
def the_lex_function_is_for_scanning_an_input_file_and_returns_a_list_of_tokens(path: str) -> list[TheTokenDataStructure]:
    with open(path, 'r', encoding='utf-8') as f:
        contents = f.read()

# Every professional program needs very unnecessary comments to describe
# what a function does. This function is the first to be executed will will
# call additional function related to making this epic programming language
# work as intended.
def the_main_function_is_the_start_to_this_epic_programming_language():
    pass

if __name__ == "__main__":
    the_main_function_is_the_start_to_this_epic_programming_language()