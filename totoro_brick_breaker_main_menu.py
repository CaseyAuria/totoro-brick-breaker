import arcade
import random
import arcade.gui

BRICK_IMAGES = [
    "brick_blue.png",
    "brick_brown.png",
    "brick_green.png",
    "brick_pink.png",
    "brick_yellow.png",
    "brick_unbreakable.png"
]

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Totoro Brick Breaker"

PADDLE_SPEED = 6
BALL_SPEED = 4

BRICK_WIDTH = 60
BRICK_HEIGHT = 20
BRICK_MARGIN = 5
BRICK_COLUMNS = SCREEN_WIDTH // (BRICK_WIDTH + BRICK_MARGIN)
BRICK_ROWS = 5
BRICK_TOP_OFFSET = 100


class Brick(arcade.Sprite):
    def __init__(self, image, x, y, hp=1):
        super().__init__(image, 1)
        self.center_x = x
        self.center_y = y
        self.hp = hp


class MainMenuView(arcade.View):
    
    def __init__(self):
        super().__init__()
        self.background = None

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.background = arcade.Sprite("totoro_background.png", 1)
        self.background.center_x = SCREEN_WIDTH // 2
        self.background.center_y = SCREEN_HEIGHT // 2

    def on_draw(self):
        self.clear()
        if self.background:
            self.background.draw()
        arcade.draw_text("Totoro Brick Breaker", SCREEN_WIDTH // 2, 400,
                         arcade.color.WHITE, 40, anchor_x="center")
        arcade.draw_text("Press ENTER to Start", SCREEN_WIDTH // 2, 300,
                         arcade.color.WHITE, 20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game = TotoroBrickBreakerGame()
            game.setup()
            self.window.show_view(game)


class GameOverView(arcade.View):
    def __init__(self, win):
        super().__init__()
        self.win = win

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text("YOU WIN!" if self.win else "GAME OVER",
                         SCREEN_WIDTH // 2, 350,
                         arcade.color.WHITE, 40, anchor_x="center")
        arcade.draw_text("Press ENTER for Main Menu", SCREEN_WIDTH // 2, 250,
                         arcade.color.WHITE, 20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            menu = MainMenuView()
            self.window.show_view(menu)


class TotoroBrickBreakerGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.all_sprites = arcade.SpriteList()
        self.brick_list = arcade.SpriteList()
        self.powerup_list = arcade.SpriteList()
        self.ball_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.acorn_projectiles = arcade.SpriteList()
        self.paddle = None
        self.score = 0
        self.lives = 3
        self.move_left = False
        self.move_right = False
        self.can_fire_acorn = False
        self.damage_multiplier = 1
        self.level = 1

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.level = 1
        self.lives = 3
        self.damage_multiplier = 1
        self.setup_level(self.level)

    def setup_level(self, level):
        self.all_sprites = arcade.SpriteList()
        self.brick_list = arcade.SpriteList()
        self.powerup_list = arcade.SpriteList()
        self.ball_list = arcade.SpriteList()
        self.acorn_projectiles = arcade.SpriteList()
        self.background_list = arcade.SpriteList()

        bg = arcade.Sprite("totoro_background.png", 1)
        bg.center_x = SCREEN_WIDTH // 2
        bg.center_y = SCREEN_HEIGHT // 2
        bg.width = SCREEN_WIDTH
        bg.height = SCREEN_HEIGHT
        self.background_list.append(bg)

        self.paddle = arcade.Sprite("cat_bus_paddle.png", 1)
        self.paddle.center_x = SCREEN_WIDTH // 2
        self.paddle.center_y = 20
        self.all_sprites.append(self.paddle)

        ball = arcade.Sprite("soot_sprite_ball.png", 1)
        ball.center_x = self.paddle.center_x
        ball.center_y = self.paddle.center_y + 10
        ball.change_x = BALL_SPEED
        ball.change_y = BALL_SPEED
        self.ball_list.append(ball)
        self.all_sprites.append(ball)

        def get_hp(image):
            if level == 1:
                return 1
            elif level == 2:
                if image == "brick_blue.png":
                    return 5
                elif image == "brick_brown.png":
                    return 4
                elif image == "brick_green.png":
                    return 3
                elif image == "brick_pink.png":
                    return 2
                elif image == "brick_yellow.png":
                    return 1
            elif level == 3:
                if image == "brick_unbreakable.png":
                    return 999999
                if image == "brick_blue.png":
                    return 5
                elif image == "brick_brown.png":
                    return 4
                elif image == "brick_green.png":
                    return 3
                elif image == "brick_pink.png":
                    return 2
                elif image == "brick_yellow.png":
                    return 1
            return 1

        for row in range(BRICK_ROWS):
            for column in range(BRICK_COLUMNS):
                if level == 3:
                    if column == BRICK_COLUMNS // 2:
                        brick_image = "brick_unbreakable.png"
                    else:
                        brick_image = BRICK_IMAGES[row % len(BRICK_IMAGES)]
                else:
                    brick_image = BRICK_IMAGES[row % len(BRICK_IMAGES)]

                x = BRICK_MARGIN + BRICK_WIDTH / 2 + column * (BRICK_WIDTH + BRICK_MARGIN)
                y = SCREEN_HEIGHT - BRICK_TOP_OFFSET - row * (BRICK_HEIGHT + BRICK_MARGIN)

                hp = get_hp(brick_image)
                brick = Brick(brick_image, x, y, hp=hp)
                self.brick_list.append(brick)
                self.all_sprites.append(brick)

        self.score = 0
        self.can_fire_acorn = False

    def on_draw(self):
        self.clear()
        self.background_list.draw()
        self.all_sprites.draw()
        self.powerup_list.draw()
        self.acorn_projectiles.draw()
        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 30,
                         arcade.color.WHITE, 20)
        arcade.draw_text(f"Lives: {self.lives}", SCREEN_WIDTH - 120,
                         SCREEN_HEIGHT - 30, arcade.color.WHITE, 20)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.move_left = True
        elif key == arcade.key.RIGHT:
            self.move_right = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.move_left = False
        elif key == arcade.key.RIGHT:
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

        for ball in list(self.ball_list):
            ball.center_x += ball.change_x
            ball.center_y += ball.change_y

            if ball.left < 0:
                ball.left = 0
                ball.change_x *= -1
            if ball.right > SCREEN_WIDTH:
                ball.right = SCREEN_WIDTH
                ball.change_x *= -1
            if ball.top > SCREEN_HEIGHT:
                ball.top = SCREEN_HEIGHT
                ball.change_y *= -1

            if ball.bottom < 0:
                self.lives -= 1
                ball.center_x = self.paddle.center_x
                ball.center_y = self.paddle.center_y + 10
                ball.change_x = BALL_SPEED
                ball.change_y = BALL_SPEED

            if arcade.check_for_collision(ball, self.paddle):
                offset = (ball.center_x - self.paddle.center_x) / (self.paddle.width / 2)
                ball.change_x = BALL_SPEED * offset
                ball.change_y = abs(ball.change_y)

            hit_list = arcade.check_for_collision_with_list(ball, self.brick_list)
            for brick in hit_list:
                brick.hp -= 1 * self.damage_multiplier
                if brick.hp <= 0:
                    brick.remove_from_sprite_lists()
                    self.score += 10

        if self.lives <= 0:
            view = GameOverView(False)
            self.window.show_view(view)

        if len(self.brick_list) == 0:
            view = GameOverView(True)
            self.window.show_view(view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu = MainMenuView()
    window.show_view(menu)
    arcade.run()


if __name__ == "__main__":
    main()

