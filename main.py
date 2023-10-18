import arcade
from characters import Player, Direction

# TODO: Spawns on Integer Grid
# TODO: Ghost selects goal/lifetime
# TODO: Ghost Backstory, different backstories "patched"

# TODO Furniture: Inventory, spawning backstory, more furniture

class GameView(arcade.View):
    DirectionKeys = {arcade.key.W: Direction.Up,
                     arcade.key.S: Direction.Down,
                     arcade.key.A: Direction.Left,
                     arcade.key.D: Direction.Right}

    def __init__(self):
        super().__init__()

        # TODO UI-Layer (Spritelist)
        # TODO Veil-Layer
        # TODO Layers for Environment (Floor, Decorations, Walls)
        #   - Walls -> check collision, Furniture -> check collision
        # TODO Interactable Layer
        # TODO Player, Ghost, NPC

        self.scene = arcade.Scene()

        self.ui_layer = arcade.SpriteList()
        self.scene.add_sprite_list(name="ui_layer", sprite_list=self.ui_layer)

        self.player = Player(scale=4)
        self.scene.add_sprite(name="player", sprite=self.player)

    def on_draw(self):
        # TODO Draw everything
        self.clear()
        self.scene.draw(pixelated=True)

    def on_update(self, delta_time):
        # TODO Update Animations etc.

        # TODO Ghost movement, Interactions, hunts
        # TODO NPC Interactions
        # TODO Player do move
        # TODO Camera movement
        self.scene.update_animation(delta_time)
        self.scene.on_update(delta_time)
        self.scene.update()

    def on_key_press(self, symbol: int, modifiers: int):
        # TODO Player Movement
        # TODO Running?
        # TODO Crouching?
        # TODO Menu?
        # TODO Interaction? Taking Items? Place Items?
        # TODO Toggle Scrolling

        if symbol in GameView.DirectionKeys:
            self.player.direction |= GameView.DirectionKeys[symbol]

    def on_key_release(self, symbol: int, modifiers: int):
        # TODO Not running forever
        # TODO stop placing Items?
        if symbol in GameView.DirectionKeys:
            self.player.direction &= ~GameView.DirectionKeys[symbol]

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        # TODO Interactions?
        # TODO Swing open Doors?
        # TODO Toggle Equipment
        # TODO shoot?
        pass

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        # TODO End things
        pass

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        # TODO Highlight items to interact with?
        # TODO turn player/FOV?
        pass

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        # TODO Scroll inventory?
        # TODO Zoom in and out (strg + scroll?)
        pass


if __name__ == "__main__":
    window = arcade.Window()
    window.show_view(GameView())
    window.run()

