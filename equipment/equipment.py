from screens import GameScreen

import arcade


class Equipment(arcade.BasicSprite):
    def __init__(self, game_screen: GameScreen, **kwargs):
        super().__init__(**kwargs)

        self.game_view: GameScreen = game_screen

    def on_use(self):
        pass

