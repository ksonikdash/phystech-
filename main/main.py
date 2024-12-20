from classes import *


# P.
if __name__ == '__main__':
    print_hi('игрок, здесь ты можешь увидеть свой счет')

wn = turtle.Screen()
wn.title("Собери монеты!")
wn.bgcolor("lightblue")
wn.setup(width=field_width + border_width * 2, height=field_height + border_width * 2)

print_field()

pl = Playerhead(cells_width // 2, cells_height // 2)
pl.spawn()

food = Food(0, 0)
food.random_spawn()

coin = Coin(0, 0)
coin.random_spawn()

food2 = Food(0, 0)
food2.random_spawn()

coin2 = Coin(0, 0)
coin2.random_spawn()

wn.listen()
wn.onkey(pl.move_up, "w")
wn.onkey(pl.move_down, "s")
wn.onkey(pl.move_left, "a")
wn.onkey(pl.move_right, "d")

while game_going:
    wn.update()
