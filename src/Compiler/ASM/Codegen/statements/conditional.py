# -*- coding: utf-8 -*-

from ...Core.commands import Commands
from ...Core.registers import Registers


def if_statement(compiler, node):
    """ Компиляция конструкции if с альтернативными ветками """
    skip_true_stmt_label = compiler.labels.create()

    node.condition.compile_asm(compiler)
    compiler.types.pop()
    # Если условие не выполнилось, пропускаем ветку.
    compiler.code.add(Commands.POP, Registers.EAX)\
        .add(Commands.CMP, [Registers.EAX, 1])\
        .add(Commands.JNZ, skip_true_stmt_label)
    node.true_stmt.compile_asm(compiler)
    compiler.code.add(Commands.POP, Registers.EAX)

    is_first_if = node.label_endif is None
    # Первая ветка условия, метки конца условия ещё нет - создаём её.
    if node.label_endif is None:
        node.label_endif = compiler.labels.create()

    # Если условие выполнилось, пропускаем все альтернативные ветки и переходим сразу к концу условия.
    compiler.code.add(Commands.JMP, node.label_endif)\
        .add_label(skip_true_stmt_label)

    # Компиляция составных альтернативных веток (elif)
    if node.alternatives_stmt:
        for alternative_stmt in node.alternatives_stmt:
            # Траслируем метку конца условия в альтернативные ветки,
            # чтобы в случае срабатывания условия в одной из веток
            # можно было перейти сразу к концу всего условия, не просматривая остальные ветки.
            alternative_stmt.label_endif = node.label_endif
            alternative_stmt.compile_asm(compiler)

    # Если ни в одной из предыдущих веток не сработал переход к метке оконачния условия,
    # выполняем последнюю альтернативную (чистый else) ветку.
    if node.false_stmt:
        node.false_stmt.compile_asm(compiler)

    if is_first_if:
        compiler.code.add_label(node.label_endif)
