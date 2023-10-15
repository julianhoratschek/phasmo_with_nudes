from util import LDtkMap, KeyMap
from characters import Player, Ghost

import arcade


class GameScreen(arcade.View):
    def __int__(self):
        super().__init__()

        self.scene = arcade.Scene()

        self.map = LDtkMap("***.json")
        self.map.add_to_scene(self.scene)

        self.keys = KeyMap()

        self.player = Player()
        self.scene.add_sprite("player", self.player)

        self.ghost = Ghost("***.json")
        self.scene.add_sprite("ghost", self.ghost)

    def on_draw(self):
        self.scene.draw(pixelated=True)

    def on_update(self, delta_time: float):
        # TODO Player
        #   - Move
        #   - Collide
        # TODO Ghost
        #   - Move
        #   - Change Room
        #   - Evidence
        #   - Hunt?
        #   - Sound?
        # TODO Environment?
        self.scene.update_animation(delta_time)
        self.scene.on_update(delta_time)
        self.scene.update()

    def on_key_press(self, symbol: int, modifiers: int):
        # TODO Player move WASD
        # TODO React to user Keybindings
        # TODO Player run
        # TODO Player crouch/hide
        # TODO Player interact (doors/books/mirrors/balls)
        #   - Doors can be opened and closed (run in VS open once through keypress VS open via Mousedrag)
        #   - Books can be read
        #   - Balls can be kicked (VS interaction on intersection)
        #   - Some items can be taken (e.g. for puzzles, summoning, replacement)
        #   - use light switch
        #   - use lights
        #   - turn radio/oven etc. on/off
        # TODO Player drop item
        # TODO Player Use selected Item
        # TODO Call Menu
        pass

    def on_key_release(self, _symbol: int, _modifiers: int):
        # TODO stop movement in one direction
        # TODO stop running
        # TODO stop hiding
        # TODO stop using some items
        pass

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        # TODO turn player/Light
        pass

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        # TODO Interaction (Doors?)
        # TODO Shoot (holy water?)
        pass

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        # TODO scroll through inventory
        pass

