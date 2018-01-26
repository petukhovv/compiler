# -*- coding: utf-8 -*-

from .Core.commands import Commands
from .Core.registers import Registers


def assign_statement(compiler, variable, aexp):
    """ Компиляция выражения присваивания """
    value_type = aexp.compile_asm(compiler)
    compiler.types.pop()
    variable.context = 'assign'
    variable.type = value_type
    variable.compile_asm(compiler)


def compound_statement(compiler, first, second):
    """ Компиляция составного выражения """
    first.compile_asm(compiler)
    compiler.code.fix_stack_balance()
    second.compile_asm(compiler)
    compiler.code.fix_stack_balance()


def repeat_statement(compiler, condition, body):
    """ Компиляция repeat-until цикла """
    continue_label = compiler.labels.create()
    compiler.code.add_label(continue_label)
    body.compile_asm(compiler)
    condition.compile_asm(compiler)
    compiler.types.pop()
    compiler.code.add(Commands.CMP, [Registers.EAX, 1])\
        .add(Commands.JNZ, continue_label)


def while_statement(compiler, condition, body):
    """ Компиляция while цикла """
    start_label = compiler.labels.create()
    compiler.code.add_label(start_label)
    finish_label = compiler.labels.create()

    condition.compile_asm(compiler)
    compiler.types.pop()
    # Если перед очередной итерации условие останова не выполнилось, завершаем цикл
    compiler.code.add(Commands.CMP, [Registers.EAX, 1])\
        .add(Commands.JNZ, finish_label)
    body.compile_asm(compiler)
    # Делаем следующую итерацию
    compiler.code.add(Commands.JMP, start_label)\
        .add_label(finish_label)


def for_statement(compiler, stmt1, stmt2, stmt3, body):
    """ Компиляция цикла for """
    start_label = compiler.labels.create()
    finish_label = compiler.labels.create()

    stmt1.compile_asm(compiler)
    compiler.code.add_label(start_label)
    stmt2.compile_asm(compiler)
    compiler.types.pop()
    # Если условия цикла не выполнилось, завешаем цикл
    compiler.code.add(Commands.CMP, [Registers.EAX, 1])\
        .add(Commands.JNZ, finish_label)
    body.compile_asm(compiler)
    stmt3.compile_asm(compiler)
    compiler.code.add(Commands.JMP, start_label)\
        .add_label(finish_label)


def if_statement(compiler, condition, true_stmt, alternatives_stmt, false_stmt, label_endif):
    """ Компиляция конструкции if с альтернативными ветками """
    skip_true_stmt_label = compiler.labels.create()

    condition.compile_asm(compiler)
    compiler.types.pop()
    # Если условие не выполнилось, пропускаем ветку.
    compiler.code.add(Commands.POP, Registers.EAX)\
        .add(Commands.CMP, [Registers.EAX, 1])\
        .add(Commands.JNZ, skip_true_stmt_label)
    true_stmt.compile_asm(compiler)
    compiler.code.add(Commands.POP, Registers.EAX)

    is_first_if = label_endif is None
    # Первая ветка условия, метки конца условия ещё нет - создаём её.
    if label_endif is None:
        label_endif = compiler.labels.create()

    # Если условие выполнилось, пропускаем все альтернативные ветки и переходим сразу к концу условия.
    compiler.code.add(Commands.JMP, label_endif)\
        .add_label(skip_true_stmt_label)

    # Компиляция составных альтернативных веток (elif)
    if alternatives_stmt:
        for alternative_stmt in alternatives_stmt:
            # Траслируем метку конца условия в альтернативные ветки,
            # чтобы в случае срабатывания условия в одной из веток
            # можно было перейти сразу к концу всего условия, не просматривая остальные ветки.
            alternative_stmt.compile_asm(compiler, label_endif)

    # Если ни в одной из предыдущих веток не сработал переход к метке оконачния условия,
    # выполняем последнюю альтернативную (чистый else) ветку.
    if false_stmt:
        false_stmt.compile_asm(compiler)

    if is_first_if:
        compiler.code.add_label(label_endif)


def skip_statement(compiler):
    """ Компиляция оператора пропуска команды """
    compiler.code.add(Commands.NOP)
