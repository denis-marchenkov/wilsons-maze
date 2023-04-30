# naive implementation of wilsons maze generation algorithm;
# we pick start and finish cells at random and begin scouting randomly
# until we reach finish cell or any already visited cell;
# during the scouting we record in which direction we exit each cell;
# if we walk through the same cell again and exit in a different direction - 
# we override stored direction for that cell;
# after finish is reached we go back to the start cell and use the recorded directions
# to build a path from start to finish.

# all the paths stored in paths_to_carve as lists,
# so 'carving' boils down to iterating through each list,
# obtaining exit direction and grid cell coordinates from each list item
# and removing one of the cell 'walls' towards which direction is pointing
class wilsons():

    def __init__(self, randomizer, seed=  None, rows = 4, columns = 4):

        self.rows = rows
        self.columns = columns
        self.visited = 0
        self.unvisited = 1
        self.random = randomizer
        if seed != None:
            self.random.seed(seed)

        # 2D list filled with 'unvisited' tokens
        self.grid = [[self.unvisited for c in range(self.columns)] for r in range(self.rows)]
        
        # movement directions
        self.top, self.right, self.bottom, self.left = '↑','→','↓','←'
        self.step_x = { self.right:1, self.left:-1}
        self.step_y = { self.top:-1, self.bottom:1}
        self.directions = [self.top, self.right, self.bottom, self.left]
        self.reverse_direction = {self.top:self.bottom, self.bottom:self.top, self.left:self.right, self.right:self.left}

        # record every step of the scouting process (for future visualization mostly, otherwise it's unnecesary)
        self.all_paths = []

        # record the actual paths from start to finish
        # we will use this to 'carve' paths in the grid
        self.paths_to_carve = []


    # check that coordinate is within the grid
    def in_grid(self, coord: tuple):
        if coord == None:
            return False
        y,x = coord
        return 0 <= x < self.columns and 0 <= y < self.rows


    # add direction to the current cell coordinates in order to get the next cell coordinates
    def add_direction(self, coord: tuple, direction):

        y,x = coord
        next_y = y + self.step_y.get(direction, 0)
        next_x = x + self.step_x.get(direction, 0)

        return (next_y, next_x)


    # start randomly scouting beginning from specified cell
    # until we reach finish cell or any already visited cell;
    # coordinates should be tuples (y, x)
    def walk_once(self, direction, start: tuple, finish: tuple) -> dict:

        dirs = self.directions.copy()

        dir = direction
        current = start

        current_path = []

        # dictionary of cells scout passed through during this walk;
        # key is tuple (y, x) - coordinates of a cell
        # and value is last exit direction
        scouted_cells = {}
        scouted_cells[start] = direction
        while True:
            y,x = current

            # if we stumble upon visited cell - simply make it our finish
            # and start over
            if self.grid[y][x] == self.visited:
                finish = current

            # reached our finish;
            # break the loop
            if current == finish:
                scouted_cells[current] = self.reverse_direction[direction]
                current_path.append((*current, self.reverse_direction[direction]))
                self.all_paths.append(current_path)
                break

            # shuffle directions until we find a valid one
            while True:

                self.random.shuffle(dirs)
                dir = dirs[0]

                next = self.add_direction(current, dir)

                if not self.in_grid(next):
                    continue

                break

            # record this cell as scouted;
            # record exit direction;
            # if we step over this cell later - we will override direction
            scouted_cells[current] = dir
            current_path.append((*current, dir))

            current = next

        # finally reached finish;
        # now walk from the start to finish using the last exit direction;
        # mark as visited only cells that we pass, all the other scouted cells remain unvisited;
        # reverse direction for the last cell in the path to target previous cell
        # so when we 'carve' walls towards direction we won't carve extra wall next to the last cell
        carved_path = []
        c = start
        d = scouted_cells[c]
        pd = d
        while True:
            d = scouted_cells[c]
            self.grid[c[0]][c[1]] = self.visited
            if c == finish:
                carved_path.append((*c, self.reverse_direction[pd]))
                break

            carved_path.append((*c, d))

            # previous direction, keep it for the last cell
            pd = d

            # we know that exit direction of this cell targets the next cell on our path towards finish
            # so move to that cell and repeat
            c = self.add_direction(c, d)

        self.paths_to_carve.append(carved_path)



    # walk over the entire grid, marking cells as visited
    # and recording paths from start to finish;
    # if entrance and exit coordinates specified - first walk will build a path
    # from entrance to the exit and then fall back to random walking
    def traverse_grid(self, entrance: tuple = None, exit: tuple = None):

        set_entrance = self.in_grid(entrance) and self.in_grid(exit)
        dirs = self.directions.copy()

        while True:

            unvisited_cells = []
            for y in range(0, self.rows):
                for x in range(0, self.columns):
                    if self.grid[y][x] == self.unvisited:
                        unvisited_cells.append((y, x))

            u_len = len(unvisited_cells)
            # all visited, we're done
            if u_len ==0:
                break
            
            # reshuffle starting coordinates and directions
            # if they are not in grid
            while True:

                start = unvisited_cells[self.random.randint(0, u_len-1)]
                self.random.shuffle(unvisited_cells)
                finish = unvisited_cells[self.random.randint(0, u_len-1)]

                if set_entrance:
                    start = entrance
                    finish = exit

                self.random.shuffle(dirs)
                dir = dirs[0]
                current = self.add_direction(start, dir)

                # reshuffle
                if not self.in_grid(current):
                    continue

                break

            set_entrance = False

            self.walk_once(dir, start, finish)





