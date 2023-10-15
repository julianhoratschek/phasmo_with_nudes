import arcade

from screens import MenuScreen, GameScreen


class GameWindow(arcade.Window):
    def __int__(self):
        super().__init__()

        self.show_view(GameScreen())


if __name__ == "__main__":
    window = GameWindow()
    window.run()

