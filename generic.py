#!/usr/bin/env python
# encoding: utf-8


class Stack(object):
    """Docstring for Stack """

    def __init__(self):
        """@todo: to be defined1 """
        self.items = []

    def pushFromList(self, list):
        """Push the list in the stack

        :param list: a list
        """
        for i in list[::-1]:
            self.push(i)

    def isEmpty(self):
        """ Says if the stack is empty
        :returns: @todo

        """
        return self.items == []

    def push(self,  item):
        """Push an item in the stack

        :param item: @todo
        :returns: @todo

        """
        self.items.append(item)

    def pop(self):
        """Getting the last item and remove it
        :returns: last item

        """
        return self.items.pop()

    def peek(self, posi = 0):
        """Getting the last item
        :param posi: which item to peek 0 (last) 1 (the onebefore the last)...
        :returns: the item

        """
        return self.items[-1 - posi]

    def __len__(self):
        return len(self.items)

    def __str__(self):
        return str(self.items) + " -> "

    def __add__(self, addList):
        return self.items + addList


def flatten_list(a, result=None):
    """Flattens a nested list.

        >>> flatten_list([ [1, 2, [3, 4] ], [5, 6], 7])
        [1, 2, 3, 4, 5, 6, 7]
    """
    if result is None:
        result = []

    for x in a:
        if isinstance(x, list):
            flatten_list(x, result)
        else:
            result.append(x)

    return result

def expand_list(list_list):
    """Expand list of list

    >>> expand_list([1,2,[3,4],5,[6,7,8]])
    [[1, 2, 3, 5, 6], [1, 2, 4, 5, 7], [1, 2, 4, 5, 8]]
    >>> expand_list([1,2,4,5,6,7,8])
    [[1, 2, 4, 5, 6, 7, 8]]

    """
    list_in_list = [i for i in list_list if type(i) == list].copy()

    try:
        nbr_ans_list = max([len(i) for i in list_in_list])

        ans = [list_list.copy() for i in range(nbr_ans_list)]
        for (i,l) in enumerate(ans):
            for (j,e) in enumerate(l):
                if type(e) == list:
                    ans[i][j] = e[min(i,len(e)-1)]
    # S'il n'y a pas de liste dans la liste (2e exemple)
    except ValueError:
        ans = [list_list]

    return ans

def add_in_dict(dict1, dict2):
    """Merge dictionary keys and add the content from dict1 and dict2

    :param dict1: first dictionary
    :param dict2: second dictionary
    :returns: merged and added dictionary

    >>> add_in_dict({'a':1, 'b':2}, {'c':3, 'd': 4}) == {'d': 4, 'a': 1, 'c': 3, 'b': 2}
    True
    >>> add_in_dict({'a':1, 'b':2}, {'a':3, 'b': 4}) == {'a': 4, 'b': 6}
    True
    >>> add_in_dict({'a':1, 'b':2}, {'a':3, 'c': 4}) == {'a': 4, 'b': 2, 'c': 4}
    True

    """
    new_dict = {}
    new_dict.update(dict1)
    for (k,v) in dict2.items():
        if k in new_dict.keys():
            new_dict[k] += v
        else:
            new_dict[k] = v

    return new_dict

def remove_in_dict(d, value = 0):
    """ In a dictionary, remove keys which have certain value

    :param d: the dictionary
    :param value: value to remove
    :returns: new dictionary whithout unwanted value

    >>> remove_in_dict({'b': 1, 'a': 0}) == {'b': 1}
    True
    >>> remove_in_dict({'b': 1, 'a': 0}, 1) == {'a': 0}
    True
    """
    new_dict = {}
    for (k,v) in d.items():
        if v != value:
            new_dict[k] = v
    return new_dict

if __name__ == '__main__':
    import doctest
    doctest.testmod()

# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
