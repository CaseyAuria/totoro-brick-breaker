import arcade
import arcade.gui
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Totoro Brick Breaker"

BRICK_IMAGES = [
    "brick_blue.png",
    "brick_brown.png",
    "brick_green.png",
    "brick_pink.png",
    "brick_yellow.png",
    "brick_unbreakable.png"
]

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
        level_button = arcade.gui.UITextureButton(
            texture=arcade.load_texture("level_button.png")
        )
        exit_button = arcade.gui.UITextureButton(
            texture=arcade.load_texture("exit_button.png")
        )

        @play_button.event("on_click")
        def on_click_play(event):
            game_view = TotoroBrickBreakerGame()
            game_view.setup(start_level=1)
            self.window.show_view(game_view)

        @level_button.event("on_click")
        def on_click_level(event):
            level_view = LevelSelectView()
            self.window.show_view(level_view)

        @exit_button.event("on_click")
        def on_click_exit(event):
            self.window.close()

        button_box = arcade.gui.UIBoxLayout(vertical=True, space_between=20)
        button_box.add(play_button)
        button_box.add(level_button)
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
            self.current_frame = (self.current_frame + 1) % len(self.rain_frames)
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


class LevelSelectView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        v_box = arcade.gui.UIBoxLayout(vertical=True, space_between=20)

        for lvl in range(1, 4):
            btn = arcade.gui.UIFlatButton(text=f"Level {lvl}", width=200)

            @btn.event("on_click")
            def on_click_lvl(event, selected_level=lvl):
                game_view = TotoroBrickBreakerGame()
                game_view.setup(start_level = selected_level)
                self.window.show_view(game_view)

            v_box.add(btn)

        back_btn = arcade.gui.UIFlatButton(text="Back to Menu", width=200)

        @back_btn.event("on_click")
        def on_click_back(event):
            self.window.show_view(MainView())

        v_box.add(back_btn)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                child=v_box,
                anchor_x="center",
                anchor_y="center"
            )
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_JUNGLE_GREEN)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Select a Level",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 100,
            arcade.color.WHITE,
            36,
            anchor_x="center"
        )
        self.manager.draw()

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
        self.game_over = False
        self.win = False
        self.damage_multiplier = 1
        self.level = 1

    def setup(self, start_level=1):
        self.level = start_level
        self.lives = 3
        self.score = 0
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
            elif level in (2, 3):
                if image == "brick_unbreakable.png" and level == 3:
                    return 999999
                elif image == "brick_blue.png":
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
                if level == 3 and column == BRICK_COLUMNS // 2:
                    brick_image = "brick_unbreakable.png"
                else:
                    brick_image = BRICK_IMAGES[row % len(BRICK_IMAGES)]

                x = BRICK_MARGIN + BRICK_WIDTH / 2 + column * (BRICK_WIDTH + BRICK_MARGIN)
                y = SCREEN_HEIGHT - BRICK_TOP_OFFSET - row * (BRICK_HEIGHT + BRICK_MARGIN)

                hp = get_hp(brick_image)
                brick = Brick(brick_image, x, y, hp=hp)
                self.brick_list.append(brick)
                self.all_sprites.append(brick)

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
        arcade.draw_text(f"Level: {self.level}", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30, arcade.color.WHITE, 20, anchor_x="center")
        arcade.draw_text(f"Lives: {self.lives}", SCREEN_WIDTH - 120, SCREEN_HEIGHT - 30, arcade.color.WHITE, 20)

        if self.game_over:
            title = "YOU WIN!" if self.win else "GAME OVER"
            arcade.draw_text(
                title,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 20,
                arcade.color.WHITE,
                50,
                anchor_x="center",
                anchor_y="center"
            )
            arcade.draw_text(
                "Press SPACE to Restart or ESC for Menu",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 35,
                arcade.color.WHITE,
                18,
                anchor_x="center",
                anchor_y="center")

main_view = MainView()
window.show_view(main_view)
arcade.run()
if __name__ == "__main__":
    main()
