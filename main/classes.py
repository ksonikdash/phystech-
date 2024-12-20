import turtle
import random

cell_size = 20
field_height = 600
field_width = 600
border_width = 40
cells_height = field_height // cell_size
cells_width = field_width // cell_size


def screen_coords(x, y):
    return x * cell_size - (field_height // 2), y * cell_size - (field_width // 2)


class Entity:
    turtle_body = None
    coord_x = 0
    coord_y = 0

    def __init__(self, x, y):
        super().__init__()
        self.coord_x = x
        self.coord_y = y
        self.is_empty = True

    def create_turtle(self):
        self.turtle_body = turtle.Turtle()
        self.turtle_body.speed(0)
        self.turtle_body.penup()
        self.is_empty = False

    def on_collision(self, entity):
        pass

    def spawn(self):
        cells_gird[self.coord_x][self.coord_y] = self
        if self.turtle_body is None:
            self.create_turtle()
        self.turtle_body.goto(screen_coords(self.coord_x, self.coord_y))
        self.turtle_body.st()
        self.is_empty = False

    def despawn(self):
        if not self.is_empty:
            cells_gird[self.coord_x][self.coord_y] = Entity(self.coord_x, self.coord_y)
            self.turtle_body.ht()
            self.is_empty = True

    def random_spawn(self):
        self.is_empty = False
        x = random.randint(0, cells_width - 1)
        y = random.randint(0, cells_height - 1)
        while not cells_gird[x][y].is_empty:
            x = random.randint(0, cells_width - 1)
            y = random.randint(0, cells_height - 1)
        self.coord_x = x
        self.coord_y = y
        self.spawn()


cells_gird = [[Entity(j, i) for i in range(field_width // cell_size)] for j in range(field_height // cell_size)]
game_going = True


class Coin(Entity):
    def on_collision(self, entity):
        self.collect(entity)

    def create_turtle(self):
        super().create_turtle()
        self.turtle_body.shape("circle")
        self.turtle_body.color("gold")

    def collect(self, entity):
        entity.coins_cnt += 1
        entity.print_info()
        self.despawn()
        self.random_spawn()


class Food(Entity):
    def on_collision(self, entity):
        self.collect(entity)

    def create_turtle(self):
        super().create_turtle()
        self.turtle_body.shape("circle")
        self.turtle_body.color("red")

    def collect(self, entity):
        entity.print_info()
        entity.on_eating()
        self.despawn()
        self.random_spawn()


class PlayerTail(Entity):
    def on_collision(self, entity):
        global game_going
        game_going = False

    def spawn(self):
        super().spawn()
        self.turtle_body.shape("circle")
        self.turtle_body.color("green")


class Playerhead(Entity):
    def __init__(self, x, y):
        self.angle = 0
        self.coins_cnt = 0
        self.food_cnt = 0
        super().__init__(x, y)
        self.body = [PlayerTail(self.coord_x - 1, self.coord_y)]

    @staticmethod
    def print_info():
        print(f"Счёт: {pl.coins_cnt}")
        print(f"Сытость: {pl.food_cnt}")

    def spawn(self):
        super().spawn()
        self.turtle_body.shape("turtle")
        self.turtle_body.color("green")
        for i in self.body:
            i.spawn()

    def on_eating(self):
        self.food_cnt += 1
        last_tail = self.body[-1]
        new_tail = PlayerTail(last_tail.coord_x, last_tail.coord_y)
        new_tail.spawn()
        self.body.append(new_tail)

    def check_moving_ability(self, x, y):
        return 0 <= self.coord_y + y < cells_height and 0 <= self.coord_x + x < cells_width

    def move_vector(self, x, y):
        self.despawn()
        if not self.check_moving_ability(x, y):
            global game_going
            game_going = False
            return
        self.coord_x += x
        self.coord_y += y
        cells_gird[self.coord_x][self.coord_y].on_collision(self)
        last_tail = self.body[-1]
        last_tail.despawn()
        self.body.pop()
        self.body.insert(0, last_tail)
        last_tail.coord_x = self.coord_x - x
        last_tail.coord_y = self.coord_y - y
        last_tail.spawn()
        self.spawn()

    def move_up(self):
        wn.onkey(None, 'w')
        self.turtle_body.left(90 - self.angle)
        self.angle = 90
        self.move_vector(0, 1)
        wn.onkey(self.move_up, 'w')
    def move_left(self):
        wn.onkey(None, 'a')
        self.turtle_body.left(180 - self.angle)
        self.angle = 180
        self.move_vector(-1, 0)
        wn.onkey(self.move_left, 'a')

    def move_down(self):
        wn.onkey(None, 's')
        self.turtle_body.left(270 - self.angle)
        self.angle = 270
        self.move_vector(0, -1)
        wn.onkey(self.move_down, 's')

    def move_right(self):
        wn.onkey(None, 'd')
        self.turtle_body.left(0 - self.angle)
        self.angle = 0
        self.move_vector(1, 0)
        wn.onkey(self.move_right, 'd')


def print_hi(name):

    print(f'Привет, {name}')


def print_field():
    drawer = turtle.Turtle()
    drawer.speed(0.001)
    drawer.penup()
    for i in range(cells_height + 1):
        s_x, s_y = screen_coords(-1, i)
        s_y -= cell_size // 2
        drawer.goto(s_x, s_y)
        drawer.pendown()
        f_x, f_y = screen_coords(cells_width, i)
        f_y -= cell_size // 2
        drawer.goto(f_x, f_y)
        drawer.penup()

    for i in range(cells_width + 1):
        s_x, s_y = screen_coords(i, - 1)
        s_x -= cell_size // 2
        drawer.goto(s_x, s_y)
        drawer.pendown()
        f_x, f_y = screen_coords(i, cells_height)
        f_x -= cell_size // 2
        drawer.goto(f_x, f_y)
        drawer.penup()
