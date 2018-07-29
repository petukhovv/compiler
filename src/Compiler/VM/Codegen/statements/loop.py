from ...Helpers.commands import Label, Jz, Jump


def repeat_statement(commands, data, node):
    """ Компиляция repeat-until цикла """
    continue_label = data.label()
    commands.add(Label, continue_label)
    node.body.compile_vm(commands, data)
    node.condition.compile_vm(commands, data)
    commands.clean_type()
    # Если после очередной итерации условие останова не выполнилось, делаем следующую итерацию
    commands.add(Jz, continue_label)


def while_statement(commands, data, node):
    """ Компиляция while цикла """
    start_label = data.label()
    commands.add(Label, start_label)
    finish_label = data.label()
    node.condition.compile_vm(commands, data)
    commands.clean_type()
    # Если перед очередной итерации условие останова не выполнилось, завершаем цикл
    commands.add(Jz, finish_label)
    node.body.compile_vm(commands, data)
    # Делаем следующую итерацию
    commands.add(Jump, start_label)\
        .add(Label, finish_label)


def for_statement(commands, data, node):
    """ Компиляция цикла for """
    start_label = data.label()
    finish_label = data.label()

    node.stmt1.compile_vm(commands, data)
    commands.add(Label, start_label)
    node.stmt2.compile_vm(commands, data)
    commands.clean_type()
    # Если условия цикла не выполнилось, завешаем цикл
    commands.add(Jz, finish_label)
    node.body.compile_vm(commands, data)
    node.stmt3.compile_vm(commands, data)
    commands.add(Jump, start_label)\
        .add(Label, finish_label)
