"""Лабораторная работа № 5: Списки и деревья"""




# Вопрос 1.
def acorn_finder(t):
    """Возвращает True, если t содержит узел со значением 'жёлудь', иначе False.

    >>> scrat = tree('жёлудь')
    >>> acorn_finder(scrat)
    True
    >>> sproul = tree('roots', [tree('ветвь1', [tree('лист'), tree('жёлудь')]), tree('ветвь2')])
    >>> acorn_finder(sproul)
    True
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> acorn_finder(numbers)
    False
    """
    if label(t) == 'жёлудь':
        return True
    return any(acorn_finder(branch) for branch in branches(t))


# Вопрос 2.
def prune_leaves(t, vals):
    """Возвращает копию t, из которой удалены листья со значениями из vals.

    Возвращает None, если исходное дерево — лист, который нужно удалить.
    Внутренний узел сохраняется, даже если после удаления его ветвей
    он становится листом.

    >>> t = tree(2)
    >>> print(prune_leaves(t, (1, 2)))
    None
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> print_tree(prune_leaves(numbers, (3, 4, 6, 7)))
    1
      2
      3
        5
      6
    """
    if is_leaf(t):
        return None if label(t) in vals else tree(label(t))

    kept_branches = []
    for branch in branches(t):
        pruned = prune_leaves(branch, vals)
        if pruned is not None:
            kept_branches.append(pruned)
    return tree(label(t), kept_branches)


# Вопрос 3.
def memory(n):
    """Возвращает функцию, которая применяет функцию к сохранённому значению n.

    >>> f = memory(10)
    >>> f(lambda x: x * 2)
    20
    >>> f(lambda x: x - 7)
    13
    >>> f(lambda x: x > 5)
    True
    """
    def update(fn):
        nonlocal n
        n = fn(n)
        return n
    return update


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
    return all(is_tree(branch) for branch in branches(tree))


def is_leaf(tree):
    """Возвращает True, если список ветвей пуст, иначе False."""
    return not branches(tree)


def print_tree(t, indent=0):
    """Выводит дерево с отступом в два пробела на каждый уровень."""
    print('  ' * indent + str(label(t)))
    for branch in branches(t):
        print_tree(branch, indent + 1)


def copy_tree(t):
    """Возвращает независимую копию дерева."""
    return tree(label(t), [copy_tree(branch) for branch in branches(t)])


# Шекспир и словари

# Вопрос 4.
def build_successors_table(tokens):
    """Возвращает словарь последующих слов для каждого слова.

    >>> text = ['We', 'came', 'to', 'investigate', ',', 'catch', 'bad', 'guys', 'and', 'to', 'eat', 'pie', '.']
    >>> table = build_successors_table(text)
    >>> sorted(table)
    [',', '.', 'We', 'and', 'bad', 'came', 'catch', 'eat', 'guys', 'investigate', 'pie', 'to']
    >>> table['to']
    ['investigate', 'eat']
    >>> table['pie']
    ['.']
    >>> table['.']
    ['We']
    """
    table = {}
    previous = '.'
    for word in tokens:
        if previous not in table:
            table[previous] = []
        table[previous].append(word)
        previous = word
    return table


# Вопрос 5.
def construct_sent(word, table):
    """Возвращает случайное предложение, начиная со слова word.

    >>> table = {'Wow': ['!'], 'Sentences': ['are'], 'are': ['cool'], 'cool': ['.']}
    >>> construct_sent('Wow', table)
    'Wow!'
    >>> construct_sent('Sentences', table)
    'Sentences are cool.'
    """
    import random

    result = []
    while word not in ['.', '!', '?']:
        result.append(word)
        word = random.choice(table[word])
    return ' '.join(result) + word


def shakespeare_tokens(path='shakespeare.txt',
                       url='http://composingprograms.com/shakespeare.txt'):
    """Возвращает слова пьес Шекспира списком."""
    import os
    from urllib.request import urlopen

    if os.path.exists(path):
        with open(path, encoding='ascii') as source:
            return source.read().split()
    response = urlopen(url)
    return response.read().decode(encoding='ascii').split()


# Для генерации случайных предложений раскомментируй следующие строки.
# tokens = shakespeare_tokens()
# table = build_successors_table(tokens)

def random_sent():
    """Генерирует случайное предложение по глобальной таблице table."""
    import random
    return construct_sent(random.choice(table['.']), table)


# Вопрос 6.
def sprout_leaves(t, vals):
    """Добавляет листья со значениями vals к каждому листу дерева t.

    >>> t1 = tree(1, [tree(2), tree(3)])
    >>> print_tree(sprout_leaves(t1, [4, 5]))
    1
      2
        4
        5
      3
        4
        5
    >>> t2 = tree(1, [tree(2, [tree(3)])])
    >>> print_tree(sprout_leaves(t2, [6, 1, 2]))
    1
      2
        3
          6
          1
          2
    """
    if is_leaf(t):
        return tree(label(t), [tree(value) for value in vals])
    return tree(label(t), [sprout_leaves(branch, vals) for branch in branches(t)])


# Вопрос 7.
def add_trees(t1, t2):
    """Складывает значения узлов деревьев с соответствующими позициями.

    Если у одного узла нет соответствующей ветви, ветвь другого дерева
    копируется без изменений.

    >>> numbers = tree(1, [tree(2, [tree(3), tree(4)]), tree(5, [tree(6, [tree(7)]), tree(8)])])
    >>> print_tree(add_trees(numbers, numbers))
    2
      4
        6
        8
      10
        12
          14
        16
    >>> print_tree(add_trees(tree(2), tree(3, [tree(4), tree(5)])))
    5
      4
      5
    >>> print_tree(add_trees(tree(2, [tree(3)]), tree(2, [tree(3), tree(4)])))
    4
      6
      4
    >>> print_tree(add_trees(tree(2, [tree(3, [tree(4), tree(5)])]), tree(2, [tree(3, [tree(4)]), tree(5)])))
    4
      6
        8
        5
      5
    """
    result_branches = []
    branches1 = branches(t1)
    branches2 = branches(t2)

    for index in range(max(len(branches1), len(branches2))):
        if index < len(branches1) and index < len(branches2):
            result_branches.append(add_trees(branches1[index], branches2[index]))
        elif index < len(branches1):
            result_branches.append(copy_tree(branches1[index]))
        else:
            result_branches.append(copy_tree(branches2[index]))

    return tree(label(t1) + label(t2), result_branches)



