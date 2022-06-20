def __str__(tab):
    for i in tab:
        print(i)
    return tab[0][0]


def numberPath(rows, cols):
    grid = [[0]*(cols) for i in range(rows)]

    # == Add '1' to end Rows ==
    for elmtRows in range(rows - 1, -1, -1):
        grid[elmtRows][-1] = 1

    # == Add '1' to end Cols ==
    for elmtCols in range(cols - 1, -1, -1):
        grid[-1][elmtCols] = 1

    # == Add adition between x-1 and y+1 to know the path number ==
    for x in range(rows -2, -1, -1):
        for y in range(cols -2, -1, -1):
            # print('=> x, y :', x, y)
            grid[x][y] = grid[x + 1][y] + grid[x][y + 1]

    return __str__(grid)

print(numberPath(5, 6))