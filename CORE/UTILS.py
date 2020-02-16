#!/usr/bin/env python3
#
# Author : Nikhil Nayak (nikhil.nixel@gmail.com)
# Usage  : .py
# 


import os


def tabulate(list_2d):
    """
    Input(2D list) ->        [[x, y], [a, b]]
    Output(ASCII art) ->     ┌─┬─┐
                             │x│y│
                             ├─┼─┤
                             │a│b│
                             └─┴─┘
    """

    table = '┌'  # Solution Stored Here! (OUTPUT)
    eo_table = '└'  # End of Table
    spacing = []  # Stores each Column box inner length

    # Check and Augment unaligned cols to make a perfect Matrix
    max_len_row = max(map(len, list_2d))
    for i in range(len(list_2d)):
        for j in range(max_len_row):
            while len(list_2d[i]) != max_len_row:
                list_2d[i].append('')
    #

    for i in range(len(list_2d[0])):
        spacing.append(
            max([len(str(list_2d[j][i])) for j in range(len(list_2d))]) + 1
        )
    # Table Processing
    num_col = len(spacing)
    for i in range(num_col):
        table += '─' * (spacing[i] - 1)
        eo_table += '─' * (spacing[i] - 1)
        if i == num_col - 1:
            table += '┐\n'
            eo_table += '┘'
        else:
            table += '┬'
            eo_table += '┴'

    num_row = len(list_2d)
    for row in range(num_row):
        table += '│'
        for col in range(num_col):
            table += list_2d[row][col] + ' ' * (spacing[col] - len(str(list_2d[row][col])) - 1) + '│'

        table += '\n'
        if row != num_row - 1:
            table += '├'
            for i in range(num_col):
                table += '─' * (spacing[i] - 1)
                if i == num_col - 1:
                    table += '┤\n'
                else:
                    table += '┼'

    #
    return table + eo_table


def sweep_dir(path):
    # path format "path/to/dir"
    folder = path
    if not os.path.exists(folder):
        return None
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)

            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    print(tabulate([['456', 'sh', '56', '0'], ['8673', 'mycroft', '5']]))
