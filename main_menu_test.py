import arcade
import arcade.gui

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Totoro Brick Breaker"


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
            game_view.setup()
            self.window.show_view(game_view)

        @level_button.event("on_click")
        def on_click_level(event):
            level_view = LevelSelectView()
            level_view.setup()
            self.window.show_view(level_view)

        @exit_button.event("on_click")
        def on_click_exit(event):
            print("Exit clicked!")
            self.window.close()

        button_box = arcade.gui.UIBoxLayout(
            vertical=True,
            space_between=20
        )

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


def main():
    window = arcade.Window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        SCREEN_TITLE,
        resizable=True
    )

    main_view = MainView()
    window.show_view(main_view)

    arcade.run()


if __name__ == "__main__":
    main()

