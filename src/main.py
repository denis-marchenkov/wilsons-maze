# region imports
from wilsons_generator import wilsons
from print_wilson import wilson_print
from draw_wilson import maze
import random
# endregion

rows = cols = 6
cell_size = 50

w = wilsons(randomizer = random, seed = 21327140567, rows = rows, columns = cols)

#w.traverse_grid()
w.traverse_grid((0,0),(w.rows - 1, w.columns - 1))

# mv = wilson_print(w)
# mv.print_steps(sleep=0.3)
# mv.dump_paths(top=1, type=0)
# mv.dump_paths(top=1, type=1)

m = maze(w, cell_size = cell_size)
#m.carve(clock_tick=30)
#m.instant_carve()
m.scout(clock_tick=10)