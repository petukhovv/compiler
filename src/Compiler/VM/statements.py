# -*- coding: utf-8 -*-

from src.Compiler.VM.Deep.strings import *
from src.Compiler.VM.Deep.arrays import *

AST = sys.modules['src.Parser.AST.arrays']

""" Компиляция выражения присваивания """
def assign_statement(commands, data, variable, aexp):
    aexp.compile_vm(commands, data)
    value_type = commands.get_type(data)
    if isinstance(variable, AST.ArrayElement):
        variable.index.compile_vm(commands, data)
        commands.load_value(data.get_var(variable.array))
        ArrayCompiler.set_element(commands, data)
    else:
        commands.store_value(data.var(alias=variable.name, type=types.DYNAMIC), type_variable=value_type)

""" Компиляция составного выражения """
def compound_statement(commands, data, first, second):
    first.compile_vm(commands, data)
    second.compile_vm(commands, data)

""" Компиляция repeat-until цикла """
def repeat_statement(commands, data, condition, body):
    continue_label = data.label()
    commands.add(Label, continue_label)
    body.compile_vm(commands, data)
    condition.compile_vm(commands, data)
    commands.extract_value()
    # Если после очередной итерации условие останова не выполнилось, делаем следующую итерацию
    commands.add(Jz, continue_label)

""" Компиляция while цикла """
def while_statement(commands, data, condition, body):
    start_label = data.label()
    commands.add(Label, start_label)
    finish_label = data.label()
    condition.compile_vm(commands, data)
    # Если перед очередной итерации условие останова не выполнилось, завершаем цикл
    commands.extract_value()
    commands.add(Jz, finish_label)
    body.compile_vm(commands, data)
    # Делаем следующую итерацию
    commands.add(Jump, start_label)\
        .add(Label, finish_label)

""" Компиляция конструкции if с альтернативными ветками """
def if_statement(commands, data, condition, true_stmt, alternatives_stmt, false_stmt, label_endif):
    skip_true_stmt_label = data.label()

    condition.compile_vm(commands, data)
    commands.extract_value()
    # Если условие не выполнилось, пропускаем ветку.
    commands.add(Jz, skip_true_stmt_label)
    true_stmt.compile_vm(commands, data)

    # Первая ветка условия, метки конца условия ещё нет - создаём её.
    if label_endif is None:
        label_endif = data.label()

    # Если условие выполнилось, пропускаем все альтернативные ветки и переходим сразу к концу условия.
    commands.add(Jump, label_endif)\
        .add(Label, skip_true_stmt_label)

    # Компиляция составных альтернативных веток (elif)
    if alternatives_stmt:
        for alternative_stmt in alternatives_stmt:
            # Траслируем метку конца условия в альтернативные ветки,
            # чтобы в случае срабатывания условия в одной из веток
            # можно было перейти сразу к концу всего условия, не просматривая остальные ветки.
            alternative_stmt.compile_vm(commands, data, label_endif)

    # Если ни в одной из предыдущих веток не сработал переход к метке оконачния условия,
    # выполняем последнюю альтернативную (чистый else) ветку.
    if false_stmt:
        false_stmt.compile_vm(commands, data)

    commands.add(Label, label_endif)

""" Компиляция цикла for """
def for_statement(commands, data, stmt1, stmt2, stmt3, body):
    start_label = data.label()
    finish_label = data.label()

    stmt1.compile_vm(commands, data)
    commands.add(Label, start_label)
    stmt2.compile_vm(commands, data)
    # Если условия цикла не выполнилось, завешаем цикл
    commands.extract_value()
    commands.add(Jz, finish_label)
    body.compile_vm(commands, data)
    stmt3.compile_vm(commands, data)
    commands.add(Jump, start_label)\
        .add(Label, finish_label)

""" Компиляция оператора пропуска команды """
def skip_statement(commands, data):
    commands.add(Nop)
