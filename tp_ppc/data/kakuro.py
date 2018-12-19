# -*- encoding: utf-8 -*-

import numpy as np


class cell:

    """ Class representing square of a Kakuro grid.

    A cell may be in three different states:
      - black (is_black() == True), the square is a black square, with no
        meaning.
      - empty (is_empty() == True), the square is an empty (blank) square.
      - otherwize, the cell contains either a bottom or a right information.

    If the cell is neither black nor empty (not is_black() and not is_empty()),
    then it contains a bottom and/or a right information that can be queried:

    >>> c = kakuro.cell(...)
    >>> c.is_black()
    False
    >>> c.is_empty()
    False
    >>> c.bottom   # No bottom sum
    None
    >>> c.right
    (4, ((3, 4), (3, 5))) # Right sum: c(3, 4) + c(3, 5) == 4
    """

    def __init__(self, i, j, bottom=None, right=None, black=False):
        self.__p = (i, j)
        self.__b = bottom
        self.__r = right
        self.__e = black

    @property
    def position(self):
        return self.__p

    def is_black(self):
        """ Return True if the cell is a black (useless) cell. """
        return self.__e

    def is_empty(self):
        """ Return True if the cell is an empty (which must be determinated)
        cell. """
        return not self.__e and self.__b is None and self.__r is None

    @property
    def bottom(self):
        """ Return bottom sum of the cell, or None if it does not exist. """
        return self.__b

    @property
    def right(self):
        """ Return right sum of the cell, or None if it does not exist. """
        return self.__r

    def __repr__(self):
        if self.is_black() or self.is_empty():
            return 'cell()'
        b = r = 0
        if self.bottom:
            b = self.bottom[0]
        if self.right:
            r = self.right[0]
        return 'cell({:2d}, {:2d})'.format(b, r)

    def __str__(self):
        return repr(self)


class problem:

    """ This class represent a kakuro problem.

    Each instance of the kakuro.problem class contains a grid of kakuro.cell
    object representing the kakuro original grid.

    You can access individual cells by different ways:

    >>> kakuro = kakuro.problem(...)
    >>> kakuro[i]           # return the i-th row
    >>> kakuro[i, j]        # return the cell at the position (i, j)
    >>> for row in kakuro:  # iterate over the rows of the grid...
    ...   for cell in row:
    ...     # do something with cell...
    """

    def __init__(self, data):

        """ Create a new instance of kakuro.problem, implementation defined. """

        self.__data = np.array(data, dtype=object)

        # Get number of rows / columns
        self.__nrows, self.__ncols = self.__data.shape

        # Construct the cells
        grid = []
        for i in range(self.__nrows):
            row = []
            for j in range(self.__ncols):
                dcol = self.__data[i, j]
                if dcol is None:
                    row.append(cell(i, j, black=True))
                elif dcol == 0:
                    row.append(cell(i, j))
                else:
                    bot, rig = dcol
                    if bot is not None:
                        cs = []
                        for ii in range(i + 1, self.__nrows):
                            if self.__data[ii, j] != 0:
                                break
                            cs.append((ii, j))
                        bot = (bot, tuple(cs))
                    if rig is not None:
                        cs = []
                        for jj in range(j + 1, self.__ncols):
                            if self.__data[i, jj] != 0:
                                break
                            cs.append((i, jj))
                        rig = (rig, tuple(cs))
                    row.append(cell(i, j, bottom=bot, right=rig))
            grid.append(row)
        self.__tuple = tuple(tuple(row) for row in grid)

    @property
    def nrows(self):
        """ Return the number of rows of this Kakuro instance. """
        return self.__nrows

    @property
    def ncolumns(self):
        """ Return the number of columns of this Kakuro instance. """
        return self.__ncols

    def str_with_solution(self, solution):
        """ Return a string representing the kakuro instance with the given
        solution.

        Parameters:
          - solution A dictionary {(x, y): value} for each empty cell. """
        bak = self.__data.copy()
        for k, v in solution.items():
            self.__data[k] = v
        res = str(self)
        self.__data = bak
        return res

    def __len__(self):
        return len(self.__tuple)

    def __getitem__(self, k):
        if type(k) == tuple:
            return self.__tuple[k[0]][k[1]]
        return self.__tuple[k]

    def __iter__(self):
        return iter(self.__tuple)

    def __repr__(self):
        return repr(self.__tuple)

    def __str__(self):
        def fmt(val, lgt=5):
            if val is None:
                return ' ' * lgt
            if isinstance(val, tuple):
                return '{}\\{}'.format(fmt(val[0], 2),
                                       fmt(val[1], 2))
            if val == 0:
                return ' ' * lgt
            return '{:{size}d}'.format(val, size=lgt)
        sep = '\n' + ('-' * 6 * self.ncolumns) + '\n'
        return sep.join('|'.join(fmt(x) for x in row) for row in self.__data)


Problems = []

Problems.append(problem([
    [None, (16, None), (44, None), (14, None), (12, None), None, (11, None), (44, None), None],
    [(None, 26), 0, 0, 0, 0, (None, 17), 0, 0, None],
    [(None, 14), 0, 0, 0, 0, (9, 4), 0, 0, (16, None)],
    [None, (None, 11), 0, 0, (10, 25), 0, 0, 0, 0],
    [None, (9, 26), 0, 0, 0, 0, (10, 9), 0, 0],
    [(None, 5), 0, 0, (12, 10), 0, 0, 0, 0, None],
    [(None, 24), 0, 0, 0, 0, (16, 11), 0, 0, (10, None)],
    [None, (None, 4), 0, 0, (None, 25), 0, 0, 0, 0],
    [None, (None, 7), 0, 0, (None, 15), 0, 0, 0, 0]
]))

Problems.append(problem([
    [None, (23, None), (30, None), None, None, (27, None), (12, None), (16, None)],
    [(None, 16), 0, 0, None, (17, 24), 0, 0, 0],
    [(None, 17), 0, 0, (15, 29), 0, 0, 0, 0],
    [(None, 35), 0, 0, 0, 0, 0, (12, None), None],
    [None, (None, 7), 0, 0, (7, 8), 0, 0, (7, None)],
    [None, (11, None), (10, 16), 0, 0, 0, 0, 0],
    [(None, 21), 0, 0, 0, 0, (None, 5), 0, 0],
    [(None, 6), 0, 0, 0, None, (None, 3), 0, 0],
]))

Problems.append(problem([
    [None, None, (28, None), (18, None), None, (11, None), (36, None), (15, None), None, None],
    [None, (None, 6), 0, 0, (11, 20), 0, 0, 0, (13, None), (16, None)],
    [None, (16, 42), 0, 0, 0, 0, 0, 0, 0, 0],
    [(None, 24), 0, 0, 0, 0, (None, 25), 0, 0, 0, 0],
    [(None, 10), 0, 0, 0, None, (20, 13), 0, 0, (42, 0), None],
    [(None, 3), 0, 0, None, (23, 29), 0, 0, 0, 0, (21, None)],
    [(None, 6), 0, 0, (33, 6), 0, 0, 0, (None, 4), 0, 0],
    [None, (None, 14), 0, 0, 0, 0, None, (30, 16), 0, 0],
    [None, (9, None), (4, 9), 0, 0, None, (7, 23), 0, 0, 0],
    [(None, 16), 0, 0, 0, 0, (5, 20), 0, 0, 0, 0],
    [(None, 43), 0, 0, 0, 0, 0, 0, 0, 0, None],
    [None, None, (None, 12), 0, 0, 0, (None, 17), 0, 0, None]
]))
