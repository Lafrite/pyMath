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

# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
