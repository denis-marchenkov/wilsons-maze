# region imports
import sys
sys.path.insert(0, './src/visualize')
import random
from wilsons_generator import wilsons
from print_wilson import wilson_print
from draw_wilson import maze
from gif import save_gif
# endregion

# 1809627, 6
# 3809627, 6

rows = cols = 30
cell_size = 20

w = wilsons(randomizer = random, seed = 53801279, rows = rows, columns = cols)

#w.traverse_grid()
w.traverse_grid((0,0),(w.rows - 1, w.columns - 1))

#mv = wilson_print(w)
#mv.print_steps(sleep=0.3)
# mv.dump_paths(top=1, type=0)
# mv.dump_paths(top=1, type=1)

m = maze(w, cell_size)

m.carve(clock_tick=60, save_frames=False)
#m.instant_carve(save_frames=False)
#m.scout(clock_tick=10, save_frames=False)

#save_gif(f"", "",50)