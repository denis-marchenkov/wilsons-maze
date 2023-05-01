# region imports
from wilsons_generator import wilsons
from print_wilson import wilson_print
from draw_wilson import maze
import random
# endregion

rows = cols = 16
cell_size = 60
clock_tick = 50

w = wilsons(randomizer = random, seed = 327111667, rows = rows, columns = cols)

w.traverse_grid((0,0),(w.rows - 1, w.columns - 1))

# mv = wilson_print(w)
# mv.print_steps(sleep=0.3)
# mv.dump_paths(top=1, type=0)
# mv.dump_paths(top=1, type=1)

m = maze(w, cell_size = cell_size)
#m.carve(clock_tick=clock_tick)
m.instant_carve()