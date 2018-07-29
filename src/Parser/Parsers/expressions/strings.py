from Lexer.types import STRING, CHAR

from ...AST.expressions.strings import StrLen, StrGet, StrSub, StrDup, StrCat, StrCmp, StrMake, String, Char


string_predefined_functions = {
    'strlen': StrLen,
    'strget': StrGet,
    'strsub': StrSub,
    'strdup': StrDup,
    'strcat': StrCat,
    'strcmp': StrCmp,
    'strmake': StrMake
}


def str_exp():
    from ..common import Tag

    return Tag(STRING) ^ String


def char_exp():
    from ..common import Tag

    return Tag(CHAR) ^ Char
