import arcade


# TODO GameWindow/GameView


from enum import Flag, auto


class Direction(Flag):
    Idle = 0
    Up = auto()     # 0b0001
    Down = auto()   # 0b0010
    Left = auto()   # 0b0100
    Right = auto()  # 0b1000 0b0111


class Player(arcade.Sprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.direction: Direction = Direction.Idle
        self.speed: float = 10.0

    def on_update(self, delta_time: float = 1/60):
        self.change_x, self.change_y = 0.0, 0.0

        if Direction.Up in self.direction:
            self.change_y += self.speed

        if Direction.Down in self.direction:
            self.change_y -= self.speed

        if Direction.Right in self.direction:
            self.change_x += self.speed

        if Direction.Left in self.direction:
            self.change_x -= self.speed


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

        self.player = Player(path_or_texture="res/sprites/star.png")
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
        if symbol in [arcade.key.W, arcade.key.S]:
            self.player.change_y = 0
        if symbol in [arcade.key.A, arcade.key.D]:
            self.player.change_x = 0

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

