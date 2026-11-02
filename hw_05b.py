### HW_05b: Изменчивые функции и генераторы

###########
# Деревья #
###########

def tree(label, branches=None):
    """Создаёт новое дерево с заданным корневым значением и списком ветвей."""
    if branches is None:
        branches = []
    for branch in branches:
        assert is_tree(branch), 'ветви должны быть деревьями'
    return [label] + list(branches)

def label(tree):
    """Возвращает корневое значение дерева."""
    return tree[0]

def branches(tree):
    """Возвращает список ветвей дерева."""
    return tree[1:]

def is_tree(tree):
    """Возвращает True, если аргумент — дерево, иначе False."""
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def is_leaf(tree):
    """Возвращает True, если список веток пуст, иначе False."""
    return not branches(tree)

def print_tree(t, indent=0):
    """Выводит представление дерева, в котором каждое значение узла
    сдвигается на два пробела за каждый уровень глубины.

    >>> print_tree(tree(1))
    1
    >>> print_tree(tree(1, [tree(2)]))
    1
      2
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> print_tree(numbers)
    1
      2
      3
        4
        5
      6
        7
    """
    print('  ' * indent + str(label(t)))
    for b in branches(t):
        print_tree(b, indent + 1)

def copy_tree(t):
    """Возвращает копию t. Используется только для тестов.

    >>> t = tree(5)
    >>> copy = copy_tree(t)
    >>> t = tree(6)
    >>> print_tree(copy)
    5
    """
    return tree(label(t), [copy_tree(b) for b in branches(t)])

# Вопрос 1.
def make_counter():
    """Возвращает функцию counter.

    >>> c = make_counter()
    >>> c('a')
    1
    >>> c('a')
    2
    >>> c('b')
    1
    >>> c('a')
    3
    >>> c2 = make_counter()
    >>> c2('b')
    1
    >>> c2('b')
    2
    >>> c('b') + c2('b')
    5
    """
    counts = {}
    def counter(key):
        counts[key] = counts.get(key, 0) + 1
        return counts[key]
    return counter

# Вопрос 2.
def make_fib():
    """Возвращает функцию, возвращающую следующее число Фибоначчи при каждом вызове.

    >>> fib = make_fib()
    >>> fib()
    0
    >>> fib()
    1
    >>> fib()
    1
    >>> fib()
    2
    >>> fib()
    3
    >>> fib2 = make_fib()
    >>> fib() + sum([fib2() for _ in range(5)])
    12
    """
    previous, current = 0, 1
    def fib():
        nonlocal previous, current
        result = previous
        previous, current = current, previous + current
        return result
    return fib

# Вопрос 3.
def make_withdraw(balance, password):
    """Возвращает защищённую паролем функцию withdraw.

    >>> w = make_withdraw(100, 'hax0r')
    >>> w(25, 'hax0r')
    75
    >>> error = w(90, 'hax0r')
    >>> error
    'Недостаточно средств'
    >>> error = w(25, 'hwat')
    >>> error
    'Неверный пароль'
    >>> new_bal = w(25, 'hax0r')
    >>> new_bal
    50
    >>> w(75, 'a')
    'Неверный пароль'
    >>> w(10, 'hax0r')
    40
    >>> w(20, 'n00b')
    'Неверный пароль'
    >>> w(10, 'hax0r')
    "Твой аккаунт заблокирован. Попытки входа: ['hwat', 'a', 'n00b']"
    >>> w(10, 'l33t')
    "Твой аккаунт заблокирован. Попытки входа: ['hwat', 'a', 'n00b']"
    >>> type(w(10, 'l33t')) == str
    True
    """
    incorrect_passwords = []
    locked_message = None

    def withdraw(amount, entered_password):
        nonlocal balance, locked_message
        if locked_message is not None:
            return locked_message
        if entered_password != password:
            incorrect_passwords.append(entered_password)
            if len(incorrect_passwords) >= 3:
                locked_message = (
                    "Твой аккаунт заблокирован. Попытки входа: "
                    + str(incorrect_passwords)
                )
            return "Неверный пароль"
        if amount > balance:
            return "Недостаточно средств"
        balance -= amount
        return balance

    return withdraw

# Вопрос 4.
def make_joint(withdraw, old_password, new_password):
    """Возвращает защищенную паролем функцию, которая присоединяется к существующей функции withdraw с новым паролем.

    >>> w = make_withdraw(100, 'hax0r')
    >>> w(25, 'hax0r')
    75
    >>> make_joint(w, 'my', 'secret')
    'Неверный пароль'
    >>> j = make_joint(w, 'hax0r', 'secret')
    >>> w(25, 'secret')
    'Неверный пароль'
    >>> j(25, 'secret')
    50
    >>> j(25, 'hax0r')
    25
    >>> j(100, 'secret')
    'Недостаточно средств'

    >>> j2 = make_joint(j, 'secret', 'code')
    >>> j2(5, 'code')
    20
    >>> j2(5, 'secret')
    15
    >>> j2(5, 'hax0r')
    10

    >>> j2(25, 'password')
    'Неверный пароль'
    >>> j2(5, 'secret')
    "Твой аккаунт заблокирован. Попытки входа: ['my', 'secret', 'password']"
    >>> j(5, 'secret')
    "Твой аккаунт заблокирован. Попытки входа: ['my', 'secret', 'password']"
    >>> w(5, 'hax0r')
    "Твой аккаунт заблокирован. Попытки входа: ['my', 'secret', 'password']"
    >>> make_joint(w, 'hax0r', 'hello')
    "Твой аккаунт заблокирован. Попытки входа: ['my', 'secret', 'password']"
    """
    validation = withdraw(0, old_password)
    if type(validation) == str:
        return validation

    def joint(amount, entered_password):
        if entered_password == new_password:
            return withdraw(amount, old_password)
        return withdraw(amount, entered_password)

    return joint

# Вопрос 5.
def generate_paths(t, x):
    """Возвращает генератор всех возможных путей от корня t до значения x в виде списков.

    >>> t1 = tree(1, [tree(2, [tree(3), tree(4, [tree(6)]), tree(5)]), tree(5)])
    >>> print_tree(t1)
    1
      2
        3
        4
          6
        5
      5
    >>> next(generate_paths(t1, 6))
    [1, 2, 4, 6]
    >>> path_to_5 = generate_paths(t1, 5)
    >>> sorted(list(path_to_5))
    [[1, 2, 5], [1, 5]]

    >>> t2 = tree(0, [tree(2, [t1])])
    >>> print_tree(t2)
    0
      2
        1
          2
            3
            4
              6
            5
          5
    >>> path_to_2 = generate_paths(t2, 2)
    >>> sorted(list(path_to_2))
    [[0, 2], [0, 2, 1, 2]]
    """
    if label(t) == x:
        yield [label(t)]
    for branch in branches(t):
        for path in generate_paths(branch, x):
            yield [label(t)] + path