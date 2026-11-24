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

UNBREAKABLE_HP = 999999
POWERUP_DROP_CHANCE = 0.25

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


class PowerUp(arcade.Sprite):
    def __init__(self, image, x, y, powerup_type):
        super().__init__(image, 1)
        self.center_x = x
        self.center_y = y
        self.change_y = -2
        self.type = powerup_type

class MainView(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.title_texture = arcade.load_texture("Title.png")
        self.bus_stop_texture = arcade.load_texture("bus_stop_sign.png")
        self.umbrella_texture = arcade.load_texture("Studio_ghibli_umbrella.png")

        self.rain_frames = [
            arcade.load_texture("rain_01.png"),
            arcade.load_texture("rain_02.png"),
            arcade.load_texture("rain_03.png"),
            arcade.load_texture("rain_04.png"),
            arcade.load_texture("rain_05.png"),
            arcade.load_texture("rain_06.png"),
        ]

        self.current_frame = 0
        self.animation_timer = 0

        play_button = arcade.gui.UITextureButton(
            texture=arcade.load_texture("play_button.png")
        )

        concept_art_button = arcade.gui.UITextureButton(
            texture=arcade.load_texture("concept_art_button.png")
        )

        exit_button = arcade.gui.UITextureButton(
            texture=arcade.load_texture("exit_button.png")
        )

        @play_button.event("on_click")
        def on_click_play(event):
            game_view = TotoroBrickBreakerGame()
            game_view.setup()
            self.window.show_view(game_view)

        @concept_art_button.event("on_click")
        def on_click_concept_art(event):
            art_book = ArtBookView()
            self.window.show_view(art_book)

        @exit_button.event("on_click")
        def on_click_exit(event):
            print("Exit clicked!")
            self.window.close()

        button_box = arcade.gui.UIBoxLayout(
            vertical=True,
            space_between=20
        )

        button_box.add(play_button)
        button_box.add(concept_art_button)
        button_box.add(exit_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                child=button_box,
                anchor_x="center",
                anchor_y="center"
            )
        )

    def on_update(self, delta_time):

        self.animation_timer += delta_time

        if self.animation_timer >= 0.1:
            self.current_frame += 1
            self.current_frame %= len(self.rain_frames)
            self.animation_timer = 0

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_JUNGLE_GREEN)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rectangle(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            self.rain_frames[self.current_frame]
        )

        arcade.draw_texture_rectangle(
            SCREEN_WIDTH // 2,
            540,
            512,
            101,
            self.title_texture
        )

        arcade.draw_texture_rectangle(
            180,
            220,
            100,
            275,
            self.bus_stop_texture
        )

        arcade.draw_texture_rectangle(
            620,
            220,
            180,
            180,
            self.umbrella_texture
        )

        self.manager.draw()

class ArtBookView(arcade.View):
    def __init__(self):
        super().__init__()

        self.current_slide = 0 

        self.slides = [
            "title_art.png",
            "buttons_art.png",
            "totoro_art.png",
            "cat_bus_art.png",
            "mixed_art.png",
            "main_menu_art.png",
            "power_up_art.png"
        ]

        self.back_button = arcade.load_texture(
            "back_button.png"
        )

        self.next_button = arcade.load_texture(
            "next_button.png"
        )

    def on_show_view(self):
        arcade.set_background_color(
            arcade.color.DARK_JUNGLE_GREEN
        )

    def on_draw(self):
        self.clear()

        slide = arcade.load_texture(
            self.slides[self.current_slide]
        )

        arcade.draw_texture_rectangle(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 30,
            650,
            450,
            slide
        )

        arcade.draw_text(
            f"{self.current_slide +1}/{len(self.slides)}", 
            SCREEN_WIDTH // 2,
            20,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )
        
        arcade.draw_texture_rectangle(
            80,
            40,
            110,
            50,
            self.back_button
        )

        arcade.draw_texture_rectangle(
            720,
            40,
            110,
            50,
            self.next_button
        )

        arcade.draw_text(
            "ESC = Return to Menu",
            SCREEN_WIDTH // 2,
             570,
             arcade.color.LIGHT_GRAY,
             14,
            anchor_x="center"
        )
    
    def on_mouse_press(
        self,
        x,
        y,
        button,
        modifiers
    ):

        if 25 <= x <= 135 and 15 <= y <= 65:

            if self.current_slide > 0:
                self.current_slide -= 1

        elif 665 <= x <= 775 and 15 <= y <= 65:

            if self.current_slide < len(self.slides) - 1:
                self.current_slide += 1

    def on_key_press(self, key, modifiers):

        if key == arcade.key.ESCAPE:
            self.window.show_view(MainView()) 

class GameOverView(arcade.View):
    def __init__(self, win=False, level=1):
        super().__init__()
        self.win = win
        self.level = level

        self.try_again_texture = arcade.load_texture(
            "try_again_button.png"
        )

        self.main_menu_texture = arcade.load_texture(
            "main_menu_button.png"
        )

    def on_draw(self):
        self.clear()
    
        message = "YOU WIN!" if self.win else "GAME OVER"

        arcade.draw_text(
            message,
            SCREEN_WIDTH // 2,
            420,
            arcade.color.WHITE,
            40,
            anchor_x="center"
        )

        arcade.draw_texture_rectangle(
            SCREEN_WIDTH // 2,
            300,
            270,
            70,
            self.try_again_texture
        )

        arcade.draw_texture_rectangle(
            SCREEN_WIDTH // 2,
            220,
            270,
            70,
            self.main_menu_texture
        )

    def on_mouse_press(self, x, y, button, modifiers):

        if 265 <= x <= 535 and 265 <= y <= 335:
            print("TRY AGAIN CLICKED")
            game_view = TotoroBrickBreakerGame()
            game_view.setup()
            self.window.show_view(game_view)

        elif 265 <= x <= 535 and 185 <= y <= 255:
            self.window.show_view(MainView())

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
        self.game_over = False
        self.win = False
        self.move_left = False
        self.move_right = False
        self.can_fire_acorn = False
        self.damage_multiplier = 1
        self.level = 1

    def setup(self):
        self.level = 1
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
                    return UNBREAKABLE_HP
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
        self.game_over = False
        self.win = False

    def on_draw(self):
        self.clear()
        self.background_list.draw()
        self.all_sprites.draw()
        self.powerup_list.draw()
        self.acorn_projectiles.draw()
        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 20)
        arcade.draw_text(f"Lives: {self.lives}", SCREEN_WIDTH - 120, SCREEN_HEIGHT - 30, arcade.color.WHITE, 20)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.move_left = True
        elif key == arcade.key.RIGHT:
            self.move_right = True
        elif key == arcade.key.UP and self.can_fire_acorn:
            acorn = arcade.Sprite("acorn_powerup.png", 1)
            acorn.center_x = self.paddle.center_x
            acorn.center_y = self.paddle.center_y + 20
            acorn.change_y = 8
            self.acorn_projectiles.append(acorn)
            self.all_sprites.append(acorn)
            self.can_fire_acorn = False

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
                if ball is self.ball_list[0] and len(self.ball_list) == 1:
                    self.lives -= 1
                    ball.center_x = self.paddle.center_x
                    ball.center_y = self.paddle.center_y + 10
                    ball.change_x = BALL_SPEED
                    ball.change_y = BALL_SPEED
                else:
                    ball.remove_from_sprite_lists()
                    continue

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
                    if random.random() < POWERUP_DROP_CHANCE:
                        choice = random.choice(["acorn", "leaf", "soot_sprite"])
                        if choice == "acorn":
                            image = "acorn_powerup.png"
                        elif choice == "leaf":
                            image = "leaf_powerup.png"
                        else:
                            image = "soot_sprite_powerup.png"
                        powerup = PowerUp(image, brick.center_x, brick.center_y, choice)
                        self.powerup_list.append(powerup)
                        self.all_sprites.append(powerup)

                if abs(ball.change_y) > 0:
                    ball.change_y *= -1
                else:
                    ball.change_x *= -1

        for acorn in list(self.acorn_projectiles):
            acorn.center_y += acorn.change_y

            if acorn.top > SCREEN_HEIGHT:
                for brick in list(self.brick_list):
                    distance = arcade.get_distance_between_sprites(acorn, brick)
                    if distance < 60:
                        brick.hp -= 1 * self.damage_multiplier
                        if brick.hp <= 0:
                            brick.remove_from_sprite_lists()
                            self.score += 10
                            if random.random() < POWERUP_DROP_CHANCE:
                                choice = random.choice(["acorn", "leaf", "soot_sprite"])
                                if choice == "acorn":
                                    image = "acorn_powerup.png"
                                elif choice == "leaf":
                                    image = "leaf_powerup.png"
                                else:
                                    image = "soot_sprite_powerup.png"
                                powerup = PowerUp(image, brick.center_x, brick.center_y, choice)
                                self.powerup_list.append(powerup)
                                self.all_sprites.append(powerup)
                acorn.remove_from_sprite_lists()
                continue

            hit_list = arcade.check_for_collision_with_list(acorn, self.brick_list)
            if hit_list:
                for brick in hit_list:
                    brick.hp -= 1 * self.damage_multiplier
                    if brick.hp <= 0:
                        brick.remove_from_sprite_lists()
                        self.score += 10
                        if random.random() < POWERUP_DROP_CHANCE:
                            choice = random.choice(["acorn", "leaf", "soot_sprite"])
                            if choice == "acorn":
                                image = "acorn_powerup.png"
                            elif choice == "leaf":
                                image = "leaf_powerup.png"
                            else:
                                image = "soot_sprite_powerup.png"
                            powerup = PowerUp(image, brick.center_x, brick.center_y, choice)
                            self.powerup_list.append(powerup)
                            self.all_sprites.append(powerup)
                acorn.remove_from_sprite_lists()

        for powerup in list(self.powerup_list):
            powerup.center_y += powerup.change_y
            if powerup.bottom < 0:
                powerup.remove_from_sprite_lists()
                continue

        caught_list = arcade.check_for_collision_with_list(self.paddle, self.powerup_list)
        for powerup in caught_list:
            if powerup.type == "leaf":
                self.damage_multiplier = 2
            elif powerup.type == "acorn":
                self.can_fire_acorn = True
            elif powerup.type == "soot_sprite":
                for i in range(2):
                    new_ball = arcade.Sprite("soot_sprite_ball.png", 1)
                    new_ball.center_x = self.paddle.center_x
                    new_ball.center_y = self.paddle.center_y + 10
                    new_ball.change_x = BALL_SPEED * random.choice([-1, 1])
                    new_ball.change_y = BALL_SPEED
                    self.ball_list.append(new_ball)
                    self.all_sprites.append(new_ball)
            powerup.remove_from_sprite_lists()

        if self.lives <= 0:
            game_over = GameOverView(
                win=False,
                level=self.level
            )
            self.window.show_view(game_over)
            return 

        if not any(brick.hp < UNBREAKABLE_HP for brick in self.brick_list):
            self.level += 1
            if self.level > 3:
                game_over = GameOverView(
                    win=True,
                    level=1 
                )
                self.window.show_view(game_over)
                return

            else:
                self.damage_multiplier = 1
                self.setup_level(self.level)


def main():
    window = arcade.Window(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_TITLE
    )

    menu_view = MainView()
    window.show_view(menu_view)

    arcade.run()


if __name__ == "__main__":
    main()