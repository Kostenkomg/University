def replace_leaf(t, old, new):
    """Возвращает новое дерево, в котором все листы со значением old заменены на new.

    >>> yggdrasil = tree('odin',
    ...                  [tree('balder',
    ...                        [tree('thor'),
    ...                         tree('loki')]),
    ...                   tree('frigg',
    ...                        [tree('thor')]),
    ...                   tree('thor', [tree('loki')])])
    >>> print_tree(replace_leaf(yggdrasil, 'thor', 'freya'))
    odin
      balder
        freya
        loki
      frigg
        freya
      thor
        loki
    """
    if is_leaf(t) and label(t) == old:
        return tree(new)
    else:
        new_branches = [replace_leaf(b, old, new) for b in branches(t)]
        return tree(label(t), new_branches)
