from ...Helpers.commands import Jz, Jump, Label


def if_statement(commands, data, node):
    """ Компиляция конструкции if с альтернативными ветками """
    skip_true_stmt_label = data.label()

    node.condition.compile_vm(commands, data)
    commands.clean_type()
    # Если условие не выполнилось, пропускаем ветку.
    commands.add(Jz, skip_true_stmt_label)
    node.true_stmt.compile_vm(commands, data)

    # Первая ветка условия, метки конца условия ещё нет - создаём её.
    if node.label_endif is None:
        node.label_endif = data.label()

    # Если условие выполнилось, пропускаем все альтернативные ветки и переходим сразу к концу условия.
    commands.add(Jump, node.label_endif)\
        .add(Label, skip_true_stmt_label)

    # Компиляция составных альтернативных веток (elif)
    if node.alternatives_stmt:
        for alternative_stmt in node.alternatives_stmt:
            # Траслируем метку конца условия в альтернативные ветки,
            # чтобы в случае срабатывания условия в одной из веток
            # можно было перейти сразу к концу всего условия, не просматривая остальные ветки.
            alternative_stmt.label_endif = node.label_endif
            alternative_stmt.compile_vm(commands, data)

    # Если ни в одной из предыдущих веток не сработал переход к метке оконачния условия,
    # выполняем последнюю альтернативную (чистый else) ветку.
    if node.false_stmt:
        node.false_stmt.compile_vm(commands, data)

    commands.add(Label, node.label_endif)