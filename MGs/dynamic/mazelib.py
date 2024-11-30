class Maze:
    """A 7Ã—7 maze, with methods for adding and removing walls,
    checking the existence of walls, and producing both a printable
    version and a MP8-compatible JSON version of the resulting maze
    """
    def __init__(self):
        self._cells = [[0 for i in range(7)] for j in range(7)]
        self.fixBorders()
    def _toggleWall(self, cell, direction):
        """Internal helper method, not intended for direct use"""
        self._cells[cell[1]][cell[0]] ^= (1<<direction)
        dx = (-1,0,1,0)[direction]
        dy = (0,1,0,-1)[direction]
        c2 = (cell[0] + dx, cell[1] + dy)
        if 0 <= c2[0] < 7 and 0 <= c2[1] < 7:
            self._cells[c2[1]][c2[0]] ^= (1<<((2+direction)&3))
    @staticmethod
    def _dirParse(direction):
        """Internal helper method, not intended for direct use"""
        if direction in ('west','south','east','north'):
            direction = ('west','south','east','north').index(direction)
        elif direction in ('left','down','right','up'):
            direction = ('left','down','right','up').index(direction)
        elif direction in tuple('WSEN'):
            direction = tuple('WSEN').index(direction)
        elif direction in tuple('LDRU'):
            direction = tuple('LDRU').index(direction)
        assert type(direction) is int and 0 <= direction < 4, f"Unknown direction {direction!r}"
        return direction
    @staticmethod
    def _dirFromCellPair(cfrom, cto):
        assert abs(cfrom[0]-cto[0]) + abs(cfrom[1]-cto[1]) == 1
        if cfrom[0] > cto[0]: return 0
        if cfrom[0] < cto[0]: return 2
        if cfrom[1] > cto[1]: return 3
        if cfrom[1] < cto[1]: return 1
    def addWall(self, cell, direction):
        """Add a wall on the given direction of the given cell.
        Cells are (column, row) pairs, from (0,0) to (6,6)
        Directions are 
            3 == 'north' == 'N' == 'up' == 'U'
            2 == 'east' == 'E' = 'right' == 'R'
            1 == 'south' == 'S' == 'down' == 'D'
            0 == 'west' == 'W' == 'left' == 'L'
            a neighboring cell
        returns True if the wall didn't exist before, False if it did
        """
        if type(direction) in (tuple,list):
            direction = Maze._dirFromCellPair(cell,direction)
        else:
            direction = Maze._dirParse(direction)
        old = self._cells[cell[1]][cell[0]]
        if old & (1<<direction): return False
        self._toggleWall(cell, direction)
        return True
    def removeWall(self, cell, direction):
        """Remove a wall on the given direction of the given cell.
        See addWall for rules on cell and direction formats.
        returns True if the wall existed before, False if it did not
        """
        if type(direction) in (tuple,list):
            direction = Maze._dirFromCellPair(cell,direction)
        else:
            direction = Maze._dirParse(direction)
        old = self._cells[cell[1]][cell[0]]
        if not (old & (1<<direction)): return False
        self._toggleWall(cell, direction)
        return True
    def fixBorders(self):
        """Ensures the outer edges of the maze have walls except in the center"""
        for i in range(7):
            if i == 3:
                self.removeWall((0,i),'left')
                self.removeWall((6,i),'right')
                self.removeWall((i,0),'up')
                self.removeWall((i,6),'down')
            else:
                self.addWall((0,i),'left')
                self.addWall((6,i),'right')
                self.addWall((i,0),'up')
                self.addWall((i,6),'down')
    def removeAllWalls(self):
        """removes all walls, resulting in a big open room"""
        for row in range(7):
            for column in range(7):
                self._cells[row][column] = 0
        self.fixBorders()
    def addAllWalls(self):
        """adds all walls, resulting in every cell being isolated"""
        for row in range(7):
            for column in range(7):
                self._cells[row][column] = 0xF
        self.fixBorders()
    def allPotentialWalls(self):
        """Returns one (cell, direction) pair for each potential passage/wall"""
        return tuple(((col,row),Maze._dirParse('down')) for col in range(7) for row in range(6))+tuple(((col,row),Maze._dirParse('right')) for col in range(6) for row in range(7))
    def allNeighboringPairs(self):
        """Returns one (cell1, cell2) pair for each pair of adjacent cells"""
        return tuple(((col,row),(col,row+1)) for col in range(7) for row in range(6))+tuple(((col,row),(col+1,row)) for col in range(6) for row in range(7))
    def hasWall(self, cell, direction):
        """Returns True if a wall exists, False if not
        See addWall for rules on cell and direction formats.
        """
        if type(direction) in (tuple,list):
            direction = Maze._dirFromCellPair(cell,direction)
        else:
            direction = Maze._dirParse(direction)
        old = self._cells[cell[1]][cell[0]]
        return bool(old & (1<<direction))
    def __str__(self):
        """A printable ASCII-art representation of the maze"""
        rows = ['+'+'+'.join('--' if self.hasWall((c,0),'up') else '  ' for c in range(7))+'+']
        for row in range(7):
            rows.append(('|' if self.hasWall((0,row),'left') else ' ')+'  '+'  '.join('|' if self.hasWall((c,row),'right')else ' ' for c in range(7)))
            rows.append('+'+'+'.join('--' if self.hasWall((c,row),'down') else '  ' for c in range(7))+'+')
        return '\n'.join(rows)
    def sendable(self):
        """Returns the format of this maze needed for the maze MP"""
        return [''.join(f'{_:x}' for _ in row) for row in self._cells]
    
