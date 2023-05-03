#region imports
import pygame
import os
from datetime import datetime
#endregion

clock = pygame.time.Clock()
pygame.init()
screen = None


class colors():
    white = (255,255,255)
    black = (0, 0, 0)
    red = (255, 0,0)
    green = (0, 255, 0)
    yellow = (255,255,0)
    blue = (0, 0, 255)
    darkgrey = (90,90,90)
    lightgrey = (166,166,166)


# cell to draw
class cell:

    def __init__(self, x, y, direction, size):
        self.x, self.y,self.direction = x, y, direction
        self.color_default = colors.darkgrey
        self.color_visited = colors.lightgrey
        self.color_carved = colors.white
        self.color_wall = colors.black
        self.color_direction = colors.red
        self.line_size = 2
        self.size = size
        self.font_size = self.size//2
        self.font = pygame.font.SysFont('arial', self.font_size)
        self.visited = False
        self.carved = False

        self.draw_direction = False

        self.is_start = False
        self.is_finish = False

        # grab directions from generator so it will match
        self.top, self.right, self.bottom, self.left = '↑','→','↓','←'
        self.walls = {self.top : True, self.right: True, self.bottom: True, self.left: True }


    def draw(self):

        # remove wall towards exit direction
        if not self.draw_direction:
            self.walls[self.direction] = False

        t,r,b,l,w =  self.top, self.right, self.bottom, self.left, self.walls
        sz, cw, cd, ls = self.size, self.color_wall, self.color_direction, self.line_size
        x = self.x * sz
        y = self.y * sz

        # fill in cell background
        if self.visited:
            pygame.draw.rect(screen, self.color_visited, (x, y, sz, sz))
        elif self.carved:
            pygame.draw.rect(screen, self.color_carved, (x, y, sz, sz))
        else:
            pygame.draw.rect(screen, self.color_default, (x, y, sz, sz))

        # draw directional arrow
        if self.draw_direction:
            text = self.font.render(self.direction, True, cd)
            text_rect = text.get_rect()
            text_rect.center = ((x + sz // 2), (y + sz // 2))
            screen.blit(text, text_rect)
        
        if self.is_start:
            cw = colors.red
        elif self.is_finish:
            cw = colors.blue

        # draw walls
        if w[t]:
            pygame.draw.line(screen, cw, (x, y), (x + sz, y), ls)
        if w[r]:
            pygame.draw.line(screen, cw, (x + sz, y), (x + sz, y + sz), ls)
        if w[b]:
            pygame.draw.line(screen, cw, (x + sz, y + sz), (x, y + sz), ls)
        if w[l]:
            pygame.draw.line(screen, cw, (x, y + sz), (x, y), ls)


# runner for pygame
class maze():

    def __init__(self, wilson, cell_size):
        self.w = wilson
        self.cell_size = cell_size

        # build grid of cells to draw on screen
        self.grid = [[cell(col, row, None, self.cell_size) for col in range(self.w.columns)] for row in range(self.w.rows)]

        self.display_size = [self.w.rows*self.cell_size + 2, self.w.columns*self.cell_size + 2]

        global screen
        screen = pygame.display.set_mode(self.display_size)

    # fill background with color and draw grid of horizontal and vertical lines
    def __background(self):
        screen_color = colors.darkgrey
        line_color = colors.black
        line_width = 2
        screen.fill(screen_color)
        for row in range(self.w.rows+1):
            pygame.draw.line(screen, line_color, (0, row * self.cell_size), (self.w.columns*self.cell_size, row * self.cell_size), line_width)
            for col in range(self.w.columns+1):
                pygame.draw.line(screen, colors.darkgrey, (col * self.cell_size, 0), (col * self.cell_size, self.w.columns * self.cell_size), line_width)


    # visualize carving paths
    def carve(self, clock_tick = 30, save_frames = False):
        name = 'carving'

        folder = self.__get_work_folder(name) if save_frames else None

        pygame.display.set_caption(f'Wilsons Walk - {name}')

        running = True
        carved = False

        while running:

            self.__background()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.__display_grid()

            image_num = 0
            if not carved:
                for p in self.w.paths_to_carve:
                    for i, c in enumerate(p):
                        self.__display_grid()

                        # grab wilsons coordinates;
                        # get cell from drawing grid;
                        # change state of drawing cell
                        current = self.__get_grid_cell(c)
                        current.direction = c[2]
                        current.carved = True
                        current.draw()

                        if i+1 >= len(p):
                            n = p[-1]
                        else:
                            n = p[i+1]

                        # also need next cell to remove walls between current and next
                        next = self.__get_grid_cell(n)
                        next.direction = n[2]
                        self.__break_wall(current,next)

                        pygame.display.flip()
                        
                        if clock_tick != None:
                            if save_frames:
                                image_path = f'{folder}{str(image_num).zfill(5)}_{name}.png'
                                pygame.image.save(screen, image_path)
                                image_num+=1
                            clock.tick(clock_tick)
                carved = True

        pygame.quit()


    # draw the entire carved maze at once
    def instant_carve(self, save_frames = False):
        
        name = 'maze'

        folder = self.__get_work_folder(name) if save_frames else None

        pygame.display.set_caption(f'Wilsons Walk - {name}')

        for p in self.w.paths_to_carve:
                for i, c in enumerate(p):
                    current = self.__get_grid_cell(c)
                    current.direction = c[2]
                    current.carved = True
                    current.draw()

                    if i+1 >= len(p):
                        n = p[-1]
                    else:
                        n = p[i+1]

                    next = self.__get_grid_cell(n)
                    next.direction = n[2]
                    self.__break_wall(current,next)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.__display_grid()
            pygame.display.flip()
            clock.tick(30)

        if save_frames:
            image_path = f'{folder}{name}.png'
            pygame.image.save(screen, image_path)

        pygame.quit()


    # visualize scouting process
    def scout(self, clock_tick = 5, save_frames = False):

        name = "scouting"

        pygame.display.set_caption(f'Wilsons Walk - {name}')

        folder = self.__get_work_folder(name) if save_frames else None

        running = True
        scouted = False

        while running:

            self.__background()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.__display_grid()

            image_num = 0
            if not scouted:
                for i, p in enumerate(self.w.all_paths):
                    start = self.__get_grid_cell(p[0])
                    finish = self.__get_grid_cell(p[-1])
                    start.is_start = True
                    finish.is_finish = True
                    for c in p:
                        self.__display_grid()

                        current = self.__get_grid_cell(c)
                        current.direction = c[2]
                        current.visited = True
                        current.draw_direction = True
                        current.draw()

                        start.draw()
                        finish.draw()

                        # track current cell with yellow rectangle
                        outline = cell(c[1], c[0], c[2], self.cell_size)
                        outline.color_wall = colors.yellow
                        outline.visited = True
                        outline.draw_direction = True
                        outline.draw()

                        pygame.display.flip()
                        if clock_tick != None:
                            if save_frames:
                                image_path = f'{folder}{str(image_num).zfill(5)}_{name}.png'
                                pygame.image.save(screen, image_path)
                                image_num+=1
                            clock.tick(clock_tick)

                    self.__reset_scouted_cells(i)
                    start.is_start = False
                    finish.is_finish = False
                    self.__display_grid()
                    pygame.display.flip()

                    pygame.time.delay(1500)
                scouted = True

        pygame.quit()


    # redraw all cells
    def __display_grid(self):
        for row in self.grid:
            for cell in row:
                cell.draw()


    # set wall to False for this cell and next cell according to exit direction
    def __break_wall(self, current, next):
        if current == next:
            return
        d = current.direction
        rd = self.w.reverse_direction[d]
        current.walls[d] = False
        next.walls[rd] = False

    # get drawing cell by coordinates
    def __get_grid_cell(self, wilson_cell):
        y,x,_ = wilson_cell
        return self.grid[y][x]

    # flatten 2D list of wilsons cells to a list;
    # we know that in paths_to_carve all cells are in order one after another anyways
    def _flatten_wilsons_grid(self, wilsons_grid):
        flat = []
        for r in wilsons_grid:
            for c in r:
                flat.append(c)
        return flat


    # revert scouted cells which are not a part of carved path
    def __reset_scouted_cells(self, path_id):
        carved_coords = {(c[1],c[0]):c[2] for c in self.w.paths_to_carve[path_id]}
        for row in self.grid:
            for cell in row:
                cell.visited = False
                if (cell.x, cell.y) not in carved_coords:
                    cell.color_direction = colors.darkgrey
                else:
                    cell.color_direction = colors.red
                    cell.carved = True
                    cell.direction = carved_coords[(cell.x, cell.y)]


    # get folder to save frames in
    def __get_work_folder(self, name):
        cwd = os.getcwd()
        now = datetime.now().strftime("%d_%m_%Y_%H_%M")
        wf = f'{cwd}\\frames\\{name}_{now}\\'
        if not os.path.exists(wf):
            os.makedirs(wf)
        return wf