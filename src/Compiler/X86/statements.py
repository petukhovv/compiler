# -*- coding: utf-8 -*-

from pprint import pprint

""" Компиляция выражения присваивания """
def assign_statement(compiler, variable, aexp):
    value_type = aexp.compile_x86(compiler)

    variable.context = 'assign'
    variable.type = value_type
    variable.compile_x86(compiler)

""" Компиляция составного выражения """
def compound_statement(compiler, first, second):
    first.compile_x86(compiler)
    second.compile_x86(compiler)

""" Компиляция repeat-until цикла """
def repeat_statement(compiler, condition, body):
    continue_label = compiler.labels.create()
    compiler.code.add(continue_label + ':', [])
    body.compile_x86(compiler)
    condition.compile_x86(compiler)
    compiler.code.add('cmp', ['eax', 1])
    compiler.code.add('jnz near', [continue_label])

""" Компиляция while цикла """
def while_statement(compiler, condition, body):
    start_label = compiler.labels.create()
    compiler.code.add(start_label + ':', [])
    finish_label = compiler.labels.create()

    condition.compile_x86(compiler)
    # Если перед очередной итерации условие останова не выполнилось, завершаем цикл
    compiler.code.add('cmp', ['eax', 1])
    compiler.code.add('jnz near', [finish_label])
    body.compile_x86(compiler)
    # Делаем следующую итерацию
    compiler.code.add('jmp near', [start_label])
    compiler.code.add(finish_label + ':', [])

""" Компиляция конструкции if с альтернативными ветками """
def if_statement(compiler, condition, true_stmt, alternatives_stmt, false_stmt, label_endif):
    skip_true_stmt_label = compiler.labels.create()

    condition.compile_x86(compiler)
    # Если условие не выполнилось, пропускаем ветку.
    compiler.code.add('cmp', ['eax', 1])
    compiler.code.add('jnz near', [skip_true_stmt_label])
    true_stmt.compile_x86(compiler)

    is_first_if = label_endif is None
    # Первая ветка условия, метки конца условия ещё нет - создаём её.
    if label_endif is None:
        label_endif = compiler.labels.create()

    # Если условие выполнилось, пропускаем все альтернативные ветки и переходим сразу к концу условия.
    compiler.code.add('jmp near', [label_endif])
    compiler.code.add(skip_true_stmt_label + ':', [])

    # Компиляция составных альтернативных веток (elif)
    if alternatives_stmt:
        for alternative_stmt in alternatives_stmt:
            # Траслируем метку конца условия в альтернативные ветки,
            # чтобы в случае срабатывания условия в одной из веток
            # можно было перейти сразу к концу всего условия, не просматривая остальные ветки.
            alternative_stmt.compile_x86(compiler, label_endif)

    # Если ни в одной из предыдущих веток не сработал переход к метке оконачния условия,
    # выполняем последнюю альтернативную (чистый else) ветку.
    if false_stmt:
        false_stmt.compile_x86(compiler)

    if is_first_if:
        compiler.code.add(label_endif + ':', [])

""" Компиляция оператора пропуска команды """
def skip_statement(compiler):
    compiler.code.add('nop', [])
