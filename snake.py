import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25
WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def draw():
    global snake, snake_body, food, game_over, score
    move()
    canvas.delete("all")  # clears canvas for next snake move
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="red")  # draw food
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="lime green")  # draw snake
    for tile in snake_body:  # draw snake's body
        canvas.create_rectangle(tile.x, tile.y, tile.x+TILE_SIZE, tile.y+TILE_SIZE, fill="lime green")

    window.after(100, draw)  # 100 ms, or 1/10 of a second

    if game_over:
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font="Arial 20", text=f"Game Over: {score}", fill="white")
        canvas.create_text(WINDOW_WIDTH / 2, 2*WINDOW_HEIGHT / 3.5, font="Arial 20", text="Space to restart",
                           fill="white")
    else:
        canvas.create_text(30, 20, font="Arial 10", text=f"Score: {score}", fill="white")


def change_direction(e):  # e = event
    # print(e)
    global velocity_x, velocity_y, game_over
    if game_over:
        if e.keysym == "space":
            reset_game()
        return

    if (e.keysym == "Up" or e.keysym == "w") and velocity_y != 1:
        velocity_x = 0
        velocity_y = -1
    elif (e.keysym == "Down" or e.keysym == "s") and velocity_y != -1:
        velocity_x = 0
        velocity_y = 1
    elif (e.keysym == "Left" or e.keysym == "a") and velocity_x != 1:
        velocity_x = -1
        velocity_y = 0
    elif (e.keysym == "Right" or e.keysym == "d") and velocity_x != -1:
        velocity_x = 1
        velocity_y = 0


def move():
    global snake, snake_body, food, game_over, score
    if game_over:
        return

    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        return

    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return

    # collision
    if snake.x == food.x and snake.y == food.y:
        snake_body.append(Tile(food.x, food.y))
        place_food()
        score += 1

    # update snake body
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if i == 0:
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocity_x*TILE_SIZE
    snake.y += velocity_y*TILE_SIZE


def is_food_on_snake():
    global snake, snake_body, food, velocity_x, velocity_y, game_over, score
    if snake.x == food.x and snake.y == food.y:
        return True
    for tile in snake_body:
        if tile.x == food.x and tile.y == food.y:
            return True
    return False


def place_food():
    global snake, snake_body, food, velocity_x, velocity_y, game_over, score
    while True:
        food.x = random.randint(0, COLS-1)*TILE_SIZE
        food.y = random.randint(0, ROWS-1)*TILE_SIZE
        if not is_food_on_snake():
            break


def reset_game():
    global snake, snake_body, food, velocity_x, velocity_y, game_over, score
    snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
    food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)
    snake_body = []  # multiple snake objects (Tile)
    velocity_x = 0
    velocity_y = 0
    game_over = False
    score = 0


# game window settings
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)
canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0,
                        highlightthickness=0)
canvas.pack()
window.update()

# center window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# initialize game
snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)
snake_body = []  # multiple snake objects (Tile)
velocity_x = 0
velocity_y = 0
game_over = False
score = 0

draw()

window.bind("<KeyRelease>", change_direction)
window.mainloop()
