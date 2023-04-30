# region imports
from wilsons_generator import wilsons
from print_wilson import wilson_print
import random
# endregion

w = wilsons(randomizer = random, rows = 10, columns = 10)

w.traverse_grid(entrance = (0,0), exit = (w.rows-1, w.columns-1))

mv = wilson_print(w)
# mv.print_steps(sleep=0.3)
mv.dump_carve_paths(top=10)