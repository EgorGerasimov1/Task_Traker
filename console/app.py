from core import TasksList

TASKS = TasksList()

#Вспомогательные функции
def act(action):
    if action == 1:
        return TASKS.get_all()
    elif action == 2:
        return TASKS.get_active()
    else:
        return TASKS.get_completed()

def fix_it(task, begin):
    status = '✅' if task.done else '❌'
    text = task.task_text
    date = task.date
    priority = task.priority
    return f'{begin}: {status}: {text}; важность: {priority}; дата: {date}'

def input_int(begin, min, max, menu=None):
    while True:
        try:
            value = input(begin).strip()
            if not value:
                print('⚠️ :ВВОД НЕ ДОЛЖЕН БЫТЬ ПУСТЫМ!!!')
                if menu:
                    print(menu)
                continue

            num = int(value)
            if num < min or num > max:
                print(f'⚠️ :УКАЖИТЕ ОТ {min} ДО {max}!!!')
                if menu:
                    print(menu)
                continue

            return num
        except ValueError:
            print('⚠️ :УКАЖИТЕ ЧИСЛО!!!')
            if menu:
                print(menu)

def input_str(begin):
    while True:
        text = input(begin).strip()
        if not text:
            print('⚠️ :ВВОД НЕ ДОЛЖЕН БЫТЬ ПУСТЫМ!!!')
            continue
        return text

def get_priority():
    value = input('🎯:Укажите важность 1-Важно, 2-Очень важно или Enter-неважно: ').strip()
    if value in ['1','2']:
        return int(value)
    elif value == '':
        return 0
    else:
        print('⚠️ :Вы указали неправильный приоритет, приоритет установлен как 0')
        return 0

def printer(action):
    tasks = act(action)
    if not tasks:
        print('❔:Этот список пуст')
        return False
    else:
        print('-------------------------------------------------------')
        for i, task in enumerate(tasks, 1):
            print(fix_it(task, i))
        print('-------------------------------------------------------')
        return True


#Методы операций Task Traker
def delete(number_task, action):
    tasks = act(action)
    if number_task <= len(tasks):
        delete_task_id = tasks[number_task-1].id
        delete_task = TASKS.delete(delete_task_id)
        if delete_task:
            return fix_it(delete_task, '💥:Задача удалена')
    return 'Такой задачи нет'

def edit(number_task, new_text, priority, action):
    tasks = act(action)
    if number_task <= len(tasks):
        edit_task_id = tasks[number_task-1].id
        edit_task = TASKS.edit(edit_task_id, new_text, priority)
        if edit_task:
            return fix_it(edit_task, '🔄:Задача отредактирована')
    return 'Такой задачи нет'

def append(text, priority):
    newtask = TASKS.append(text, priority)
    return fix_it(newtask, '🆕:Задача добавлена')

def complete(number_task, action):
    tasks = act(action)
    if number_task <= len(tasks):
        complete_id = tasks[number_task-1].id
        complete_task = TASKS.complete(complete_id)
        if complete_task:
            return fix_it(complete_task, '👍:Задача завершена')
    return 'Такой задачи нет'



# Начало цикла программы
def run():
    # Константы
    TASK_ALL = 1
    TASK_ACTIVE = 2
    TASK_COMPLETE = 3
    EXIT = 4

    COMPLETE = 1
    EDIT = 2
    DELETE = 3
    APPEND = 4
    HEAD_MENU = 5

    MENU1 = f'''Меню Task Traker:
{TASK_ALL}:Все; {TASK_ACTIVE}:Активные; {TASK_COMPLETE}:Завершенные; {EXIT}:Выход'''
    MENU2 = f'''Способ взаимодействия: 
{COMPLETE}:Завершить {EDIT}:Редактировать {DELETE}:Удалить {APPEND}:Добавить {HEAD_MENU}:Главное меню'''

    try:
        while True:
            print('_________________________________________________________________')
            print(MENU1)

            action1 = input_int('🏹:Укажите номер операции: ', 1, 4, MENU1)
            if action1 == EXIT:
                print('👋 До свидания красивый человек!')
                break

            tasks = act(action1)
            not_empty = printer(action1)
            if not not_empty:
                if action1 == TASK_ALL:
                    print('➕:Добавьте свою первую задачу используя 4!')
                elif action1 == TASK_ACTIVE:
                    print('➕:Все задачи выполнены, добавьте новую используя 4')
                else:
                    print('❔:У вас нету завершенных задач или они были удалены')
                    continue
                
            while True:
                print(MENU2)
                action2 = input_int('🏹:Укажите номер операции: ', 1, 5, MENU2)
                if action2 not in [APPEND,HEAD_MENU] and not tasks:
                    print('❔:Список пуст! Добавь➕ задачу используя 4')
                elif action2 == COMPLETE:
                    complete_task = input_int('🏹:Укажите номер задачи: ', 1, len(tasks))
                    print(complete(complete_task, action1))

                elif action2 == EDIT:
                    edit_task = input_int('🏹:Укажите номер задачи: ', 1, len(tasks))
                    text = input_str('📝:Новый текст задачи: ')
                    priority = get_priority()
                    print(edit(edit_task, text, priority, action1))

                elif action2 == DELETE:
                    delete_task = input_int('🏹:Укажите номер задачи: ', 1, len(tasks))
                    print(delete(delete_task, action1))

                elif action2 == APPEND:
                    text = input_str('📝:Напишите текст задачи: ').strip()
                    priority = get_priority()
                    print(append(text, priority))

                elif action2 == HEAD_MENU:
                    break

                else:
                    print('⚠️ :НЕВЕРНО УКАЗАН НОМЕР!!!')
                print('_________________________________________________________________')
    except KeyboardInterrupt:
        print('\nПрограмма прервана!👋 До свидания!')