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

def first_elem(ll):
    """Get the first element in imbricates lists
    # TODO: Fonction pourrie mais j'ai pas le temps de faire mieux! |mar. janv. 28 22:32:22 CET 2014

    :param list: list of lists of lists...
    :returns: the first element

    >>> first_elem(1)
    1
    >>> first_elem([1,2])
    1
    >>> first_elem([["abc"]])
    'a'
    >>> first_elem("abc")
    'a'
    >>> first_elem([[[1,2],[3,4]], [5,6]])
    1
    >>> first_elem([[["ab",2],[3,4]], [5,6]])
    'a'

    """
    if hasattr(ll, '__contains__'):
        if len(ll) == 1 and type(ll) == str:
            return ll[0]
        else:
            return first_elem(ll[0])
    else:
        return ll

def last_elem(ll):
    """Get the last element in imbricates lists
    # TODO: Fonction pourrie mais j'ai pas le temps de faire mieux! |mar. janv. 28 22:32:22 CET 2014

    :param list: list of lists of lists...
    :returns: the last element

    >>> last_elem(1)
    1
    >>> last_elem([1,2])
    2
    >>> last_elem([["abc"]])
    'c'
    >>> last_elem("abc")
    'c'
    >>> last_elem([[[1,2],[3,4]], [5,6]])
    6
    >>> last_elem([[["ab",2],[3,4]], [5,6]])
    6

    """
    if hasattr(ll, '__contains__'):
        if len(ll) == 1 and type(ll) == str:
            return ll[-1]
        else:
            return last_elem(ll[-1])
    else:
        return ll


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

def convolution_dict(D1, D2, op = lambda x,y:x*y,\
        op_key = lambda x,y: x + y, \
        commutative = True, op_twice = lambda x,y: x + y):
    """Convolution of two dictionaries

    :param D1: First dictionary
    :param D2: Second dictionary
    :param op: Operation of perform in value
    :param commutative: keys are commutative?
    :param op_twice: operation on value if the key appear twice

    >>> convolution_dict({"a": 1, "b":3}, {"a":2, "":4}) == {"aa":2, "a": 4, "ba":6, "b":12}
    True
    >>> convolution_dict({"a": 1, "b":3}, {"a":2, "b":4}) == {"aa":2, "ab":10, "bb":12}
    True
    >>> convolution_dict({"a": 1, "b":3}, {"a":2, "b":4}, commutative = False) == {"aa":2, "ab":10, "bb":12}
    False
    >>> convolution_dict({"a": 1, "b":3}, {"a":2, "b":4}, commutative = False) == {"aa":2, "ab":4,"ba":6,  "bb":12}
    True
    >>> convolution_dict({"a": 1, "b":3}, {"a":2, "b":4}, \
            op_twice = lambda x,y:[x,y]) == {"aa":2, "ab":[4,6], "bb":12}
    True

    """
    new_dict = {}

    for k1 in sorted(D1.keys()):
        for k2 in sorted(D2.keys()):
            if op_key(k1,k2) in new_dict.keys():
                key = op_key(k1,k2)
                new_dict[key] = op_twice(new_dict[key], op(D1[k1],D2[k2]))

            elif op_key(k2,k1) in new_dict.keys() and commutative:
                key = op_key(k2,k1)
                new_dict[key] = op_twice(new_dict[key], op(D1[k1],D2[k2]))

            else:
                key = op_key(k1,k2)
                new_dict[key] = op(D1[k1],D2[k2])

    return new_dict

if __name__ == '__main__':
    import doctest
    doctest.testmod()


# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
