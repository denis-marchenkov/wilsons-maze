#region imports
import os
import time
#endregion

# print grid to console
# mainly for debugging purposes
class wilson_print():

    def __init__(self, wilson):
        self.w = wilson

    def print_steps(self,  sleep: float):
        self.__cls()
        for path in self.w.all_paths:
            display_grid = self.__grid()
            sy,sx,_ = path[0]
            ey, ex,_ = path[-1]
            display_grid[sy][sx] = "S"
            display_grid[ey][ex] = "E"

            for step in path:
                self.__cls()

                y,x,d = step

                if y == sy and x == sx:
                    display_grid[y][x] = f'S{d}'
                elif y == ey and x == ex:
                    display_grid[y][x] = f'F{d}'
                else:
                     display_grid[y][x] = d

                self.__print_grid(display_grid)

                time.sleep(sleep)


    def dump_carve_paths(self, top=10):
        self.__cls()
        for i, path in enumerate(self.w.paths_to_carve):
            if i>top:
                break
            print(f'\n{i} path: {path}\n')
            display_grid = self.__grid()
            sy,sx,_ = path[0]
            ey, ex,_ = path[-1]
            display_grid[sy][sx] = "S"
            display_grid[ey][ex] = "E"

            for step in path:
                y,x,d = step
                if y == sy and x == sx:
                    display_grid[y][x] = f'S{d}'
                elif y == ey and x == ex:
                    display_grid[y][x] = f'F{d}'
                else:
                     display_grid[y][x] = d

            self.__print_grid(display_grid)



    def __cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')


    def __print_grid(self, grid):
        for row in grid:
            print(row)

    def __grid(self):
        return [[' ' for c in range(self.w.columns)] for r in range(self.w.rows)]


