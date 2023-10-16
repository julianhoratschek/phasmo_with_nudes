import arcade

# TODO GameWindow/GameView


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.scene = arcade.Scene()

        self.ui_layer = arcade.SpriteList()
        self.scene.add_sprite_list(name="ui_layer", sprite_list=self.ui_layer)

        # TODO UI-Layer (Spritelist)
        # TODO Veil-Layer
        # TODO Layers for Environment (Floor, Decorations, Walls)
        #   - Walls -> check collision, Furniture -> check collision
        # TODO Interactable Layer
        # TODO Player, Ghost, NPC

    def on_draw(self):
        # TODO Draw everything
        self.scene.draw()

    def on_update(self, delta_time):
        # TODO Update Animations etc.

        # TODO Ghost movement, Interactions, hunts
        # TODO NPC Interactions
        # TODO Player do move
        # TODO Camera movement
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        # TODO Player Movement
        # TODO Running?
        # TODO Crouching?
        # TODO Menu?
        # TODO Interaction? Taking Items? Place Items?
        # TODO Toggle Scrolling
        pass

    def on_key_release(self, symbol: int, modifiers: int):
        # TODO Not running forever
        # TODO stop placing Items?
        pass

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


