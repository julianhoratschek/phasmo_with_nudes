from util import LDtkMap, KeyMap, KeyType
from characters import Player, Ghost
from ui import ItemFrame

import arcade


class GameScreen(arcade.View):
    def __init__(self):
        super().__init__()

        self._placing_item = False          # Indicates if the player currently places an item

        self.scene = arcade.Scene()

        # TODO random Map/selected map Loader
        self.map = LDtkMap("***.json")
        self.map.add_to_scene(self.scene)

        self.keys = KeyMap()

        self.player = Player()
        self.scene.add_sprite("player", self.player)

        # TODO random Ghost selection
        self.ghost = Ghost()
        self.scene.add_sprite("ghost", self.ghost)

        self.ui = arcade.SpriteList(use_spatial_hash=True)
        self.ui.append(ItemFrame())
        self.scene.add_sprite_list("ui", sprite_list=self.ui)

    def on_draw(self):
        # TODO draw item transparent when placed
        # TODO draw currently not visible rooms dark
        # TODO shaders for light and sight?
        self.scene.draw(pixelated=True)

    def on_update(self, delta_time: float):
        # TODO Ghost
        #   - Sound?
        # TODO Environment?
        self.scene.update_animation(delta_time)
        self.scene.on_update(delta_time)
        self.scene.update()

    def on_key_press(self, symbol: int, modifiers: int):
        self.keys.press(symbol, modifiers)

        # Allow for multiple actions through one key
        if KeyType.Movement in self.keys:
            self.player.direction |= self.keys.direction_of(symbol)

        if KeyType.Run in self.keys:
            self.player.running = True

        if KeyType.Crouch in self.keys:
            self.player.crouching = True

        if KeyType.Interact in self.keys:
            # TODO Player interact (doors/books/mirrors/balls)
            #   - Doors can be opened and closed (run in VS open once through keypress VS open via Mousedrag)
            #   - Books can be read
            #   - Balls can be kicked (VS interaction on intersection)
            #   - Some items can be taken (e.g. for puzzles, summoning, replacement)
            #   - use light switch
            #   - use lights
            #   - turn radio/oven etc. on/off
            pass

        if KeyType.Drop in self.keys:
            # TODO drop current item
            pass

        if KeyType.Place in self.keys:
            self._placing_item = True

        if KeyType.Use in self.keys:
            # TODO use current item e.g. equpimpent, cursed item or other item/turn them on
            pass

        if KeyType.Menu in self.keys:
            # TODO open menu
            pass

    def on_key_release(self, symbol: int, modifiers: int):
        self.keys.release(symbol, modifiers)

        if KeyType.Movement in self.keys:
            self.player.direction ^= self.keys.direction_of(symbol)

        if KeyType.Run in self.keys:
            self.player.running = False

        if KeyType.Crouch in self.keys:
            self.player.crouching = False

        if KeyType.Place in self.keys:
            self._placing_item = False

        if KeyType.Use in self.keys:
            # TODO stop using some items/turn them off
            pass

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        if self._placing_item:
            # TODO rotate item while placing it
            pass
        else:
            # TODO turn player/Light
            pass

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        # TODO Interaction (Doors?)
        # TODO Shoot (holy water?)
        pass

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        # TODO scroll through inventory
        pass

