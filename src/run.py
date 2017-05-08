import sys

from pprint import pprint

from Lexer.tokenizer import tokenize
from Parser.run import parse

test_id = '026'

sys.stdout.write('\nExpected input:\n')
test_input_file = '../compiler-tests/core/test' + test_id + '.input'
test_input = open(test_input_file).read()
sys.stdout.write(test_input + '\n')

test_expr_file = '../compiler-tests/core/test' + test_id + '.expr'
test_expr = open(test_expr_file).read()
tokens = tokenize(test_expr)
#pprint(tokens)
parse_result = parse(tokens)
if not parse_result:
    sys.stderr.write('Parse error!\n')
    sys.exit(1)
pprint(parse_result.value)
ast = parse_result.value
env = {
    'v': {},    # variables environment
    'f': {}     # functions environment
}
sys.stdout.write('Output:\n')
ast.eval(env)
sys.stdout.write('\nExpected output:\n')

test_output_file = '../compiler-tests/core/orig/test' + test_id + '.log'
test_output = open(test_output_file).read()
sys.stdout.write(test_output + '\n')

sys.stdout.write('\n')
pprint(env)
