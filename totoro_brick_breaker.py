import arcade
import random

BRICK_IMAGES = [
    "brick_blue.png",
    "brick_brown.png",
    "brick_green.png",
    "brick_pink.png",
    "brick_yellow.png"
]

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Totoro Brick Breaker"

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_SPEED = 6

BALL_RADIUS = 8
BALL_SPEED = 4

BRICK_ROWS = 5
BRICK_COLUMNS = 10
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
BRICK_MARGIN = 5
BRICK_TOP_OFFSET = 100


class TotoroBrickBreakerGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.background = arcade.load_texture("totoro_background.png")

        self.all_sprites = arcade.SpriteList()
        self.brick_list = arcade.SpriteList()

        self.paddle = None
        self.ball = None

        self.score = 0

        self.move_left = False
        self.move_right = False

        self.powerup_list = arcade.SpriteList()

        self.has_shield = False
        self.lives = 3

        self.ball_list = arcade.SpriteList()

    def setup(self):
        self.all_sprites = arcade.SpriteList()
        self.brick_list = arcade.SpriteList()
        self.powerup_list = arcade.SpriteList()
        self.ball_list = arcade.SpriteList()

        self.paddle = arcade.Sprite("cat_bus_paddle.png", 1)
        self.paddle.center_x = SCREEN_WIDTH // 2
        self.paddle.center_y = 50
        self.paddle.change_x = 0
        self.all_sprites.append(self.paddle)

        self.ball = arcade.Sprite("soot_sprite_ball.png", 1)
        self.ball.center_x = SCREEN_WIDTH // 2
        self.ball.center_y = 120
        self.ball.change_x = BALL_SPEED
        self.ball.change_y = BALL_SPEED
        self.ball_list.append(self.ball)
        self.all_sprites.append(self.ball)

        for row in range(BRICK_ROWS):
            brick_image = BRICK_IMAGES[row % len(BRICK_IMAGES)]
            for column in range(BRICK_COLUMNS):
                brick = arcade.Sprite(brick_image, 1)
                brick.center_x = (
                    BRICK_MARGIN
                    + BRICK_WIDTH / 2
                    + column * (BRICK_WIDTH + BRICK_MARGIN)
                )
                brick.center_y = (
                    SCREEN_HEIGHT
                    - BRICK_TOP_OFFSET
                    - row * (BRICK_HEIGHT + BRICK_MARGIN)
                )
                self.brick_list.append(brick)
                self.all_sprites.append(brick)

        self.score = 0
        self.has_shield = False
        self.lives = 3

    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            SCREEN_WIDTH,
            SCREEN_HEIGHT
            self.background,
        )

        self.all_sprites.draw()

        if self.has_shield:
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH // 2,
                5,
                SCREEN_WIDTH,
                10,
                arcade.color.LIGHT_GREEN
            )

        arcade.draw_text(
            f"Score: {self.score}",
            10,
            SCREEN_HEIGHT - 30,
            arcade.color.WHITE,
            20
        )

        arcade.draw_text(
            f"Lives: {self.lives}",
            SCREEN_WIDTH - 120,
            SCREEN_HEIGHT - 30,
            arcade.color.WHITE,
            20
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.move_left = True
        if key == arcade.key.RIGHT:
            self.move_right = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.move_left = False
        if key == arcade.key.RIGHT:
            self.move_right = False

    def on_update(self, delta_time):

        if self.move_left:
            self.paddle.center_x -= PADDLE_SPEED
        if self.move_right:
            self.paddle.center_x += PADDLE_SPEED

        if self.paddle.left < 0:
            self.paddle.left = 0
        if self.paddle.right > SCREEN_WIDTH:
            self.paddle.right = SCREEN_WIDTH

        self.ball.center_x += self.ball.change_x
        self.ball.center_y += self.ball.change_y

        if self.ball.left < 0:
            self.ball.left = 0
            self.ball.change_x *= -1

        if self.ball.right > SCREEN_WIDTH:
            self.ball.right = SCREEN_WIDTH
            self.ball.change_x *= -1

        if self.ball.top > SCREEN_HEIGHT:
            self.ball.top = SCREEN_HEIGHT
            self.ball.change_y *= -1

        if self.ball.bottom < 0:
            self.lives -= 1 
            self.ball.center_x = SCREEN_WIDTH // 2
            self.ball.center_y = 120
            self.ball.change_x = BALL_SPEED
            self.ball.change_y = BALL_SPEED

        if arcade.check_for_collision(self.ball, self.paddle):
            self.ball.change_y *= -1

        hit_list = arcade.check_for_collision_with_list(self.ball, self.brick_list)

        for brick in hit_list:
            brick_x = brick.center_x
            brick_y = brick.center_y

            brick.remove_from_sprite_lists()
            self.ball.change_y *= -1
            self.score += 10

            if random.random() < 0.3:
                choice = random.choice(["acorn", "leaf", "soot_sprite"])

                if choice == "acorn":
                    powerup = arcade.Sprite("acorn_powerup.png", 1)
                elif choice == "leaf":
                    powerup = arcade.Sprite("leaf_powerup.png", 1)
                else:
                    powerup = arcade.Sprite("soot_sprite.png", 1)

                powerup.type = choice
                powerup.center_x = brick_x
                powerup.center_y = brick_y
                powerup.change_y = -2

                self.powerup_list.append(powerup)

        for powerup in self.powerup_list:
            powerup.center_y += powerup.change_y

        caught_list = arcade.check_for_collision_with_list(self.paddle, self.powerup_list)

        for powerup in caught_list:

            if powerup.type == "leaf":
                self.has_shield = True

            elif powerup.type == "acorn":
                for brick in self.brick_list:
                    distance = arcade.get_distance_between_sprites(self.ball, brick)
                    if distance < 120:
                        brick.remove_from_sprite_lists()
                        self.score += 10

            elif powerup.type == "soot_sprite":
                for i in range(2):
                    new_ball = arcade.Sprite("soot_sprite_ball.png", 1)
                    new_ball.center_x = self.ball.center_x
                    new_ball.center_y = self.ball.center_y
                    new_ball.change_x = BALL_SPEED * random.choice([-1, 1])
                    new_ball.change_y = BALL_SPEED * random.choice([-1, 1])
                    self.ball_list.append(new_ball)
                    self.all_sprites.append(new_ball)

            powerup.remove_from_sprite_lists()

        if self.lives <= 0:
            arcade.close_window()


def main():
    game = TotoroBrickBreakerGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()


    