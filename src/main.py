# region imports
from wilsons_generator import wilsons
from print_wilson import wilson_print
from draw_wilson import maze
import random
# endregion

# 1809627, 6
# 3809627, 6

rows = cols = 7
cell_size = 70

w = wilsons(randomizer = random, seed = 53801279, rows = rows, columns = cols)

#w.traverse_grid()
w.traverse_grid((0,0),(w.rows - 1, w.columns - 1))

# mv = wilson_print(w)
# mv.print_steps(sleep=0.3)
# mv.dump_paths(top=1, type=0)
# mv.dump_paths(top=1, type=1)

m = maze(w, cell_size)

#m.carve(clock_tick=3, save_frames=True)
m.instant_carve()
#m.scout(clock_tick=10, save_frames=False)