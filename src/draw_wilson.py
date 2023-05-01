#region imports
import pygame
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
        self.line_size = 2
        self.size = size
        self.font_size = self.size//2

        self.visited = False
        self.carved = False

        # grab directions from generator so it will match
        self.top, self.right, self.bottom, self.left = '↑','→','↓','←'
        self.walls = {self.top : True, self.right: True, self.bottom: True, self.left: True }


    def draw(self):

        # remove wall towards exit direction
        self.walls[self.direction] = False

        t,r,b,l,w =  self.top, self.right, self.bottom, self.left, self.walls
        sz, cw, ls = self.size, self.color_wall, self.line_size
        x = self.x * sz
        y = self.y * sz

        if self.visited:
            pygame.draw.rect(screen, self.color_visited, (x, y, sz, sz))
        elif self.carved:
            pygame.draw.rect(screen, self.color_carved, (x, y, sz, sz))
        else:
            pygame.draw.rect(screen, self.color_default, (x, y, sz, sz))

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


    # draw carving paths
    def carve(self, clock_tick = 30):

        pygame.display.set_caption('Wilsons Walk - Carving')

        running = True
        carved = False

        while running:

            self.__background()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.__display_grid()

            if not carved:
                for p in self.w.paths_to_carve:
                    
                    for i, cell in enumerate(p):
                        self.__display_grid()

                        # grab wilsons coordinates;
                        # get cell from drawing grid;
                        # change state of drawing cell
                        c = cell
                        current = self.__get_grid_cell((c[0],c[1]))
                        current.direction = c[2]
                        current.carved = True
                        current.draw()

                        if i+1 >= len(p):
                            n = p[-1]
                        else:
                            n = p[i+1]

                        # also need next cell to remove walls between current and next
                        next = self.__get_grid_cell((n[0],n[1]))
                        next.direction = n[2]
                        self.__break_wall(current,next)

                        pygame.display.flip()
                        if clock_tick != None:
                            clock.tick(clock_tick)
                carved = True
        pygame.quit()


    # draw the entire carved maze at once
    def instant_carve(self):
        for p in self.w.paths_to_carve:
                for i, cell in enumerate(p):
                    c = cell
                    current = self.__get_grid_cell((c[0],c[1]))
                    current.direction = c[2]
                    current.carved = True
                    current.draw()

                    if i+1 >= len(p):
                        n = p[-1]
                    else:
                        n = p[i+1]

                    next = self.__get_grid_cell((n[0],n[1]))
                    next.direction = n[2]
                    self.__break_wall(current,next)


        pygame.display.set_caption('Wilsons Walk - Carving')

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.__display_grid()
            pygame.display.flip()
            clock.tick(30)
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
    def __get_grid_cell(self, coord):
        y,x = coord
        return self.grid[y][x]

    # flatten 2D list of wilsons cells to a list;
    # we know that in paths_to_carve all cells are in order one after another anyways
    def _flatten_wilsons_grid(self, wilsons_grid):
        flat = []
        for r in wilsons_grid:
            for c in r:
                flat.append(c)
        return flat