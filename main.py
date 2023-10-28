import arcade
from characters import Player, Direction
from util.ldtk import TileMap

from arcade.experimental import Shadertoy

# TODO: Spawns on Integer Grid
# TODO: Ghost selects goal/lifetime
# TODO: Ghost Backstory, different backstories "patched"a

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

        self.scene: arcade.Scene = arcade.Scene()

        self.ui_layer: arcade.SpriteList = arcade.SpriteList()
        self.scene.add_sprite_list(name="ui_layer", sprite_list=self.ui_layer)

        self.map = TileMap()
        self.map.load_level(level_nr=0)

        self.cam = arcade.Camera()
        self.cam.zoom = 0.7

        self.player: Player = Player()
        self.player.position = self.map.player_pos
        self.scene.add_sprite(name="player", sprite=self.player)

        window_size = self.window.get_size()

        self.shadertoy = Shadertoy.create_from_file(size=window_size, path="shaders/test.glsl")
        self.channel_0 = self.shadertoy.ctx.framebuffer(color_attachments=[self.shadertoy.ctx.texture(size=window_size,
                                                                                                      components=4)])
        self.shadertoy.channel_0 = self.channel_0.color_attachments[0]

    def on_draw(self):
        # TODO Draw everything
        self.channel_0.use()
        self.channel_0.clear()

        self.map.draw_level()

        self.window.use()
        self.cam.use()
        self.clear()

        # self.shadertoy.program['playerPosition'] = self.player.position
        self.shadertoy.render()

        self.scene.draw(pixelated=True)

        self.player.draw_hit_box(color=arcade.color.RED)

        # TODO UI Cam

    def on_update(self, delta_time):
        # TODO Update Animations etc.

        # TODO Ghost movement, Interactions, hunts
        # TODO NPC Interactions
        # TODO Player do move
        # TODO Camera movement
        self.scene.update_animation(delta_time)
        self.scene.on_update(delta_time)

        for next_position in self.player.get_next_positions():
            if self.map.wall_collision(next_position):
                self.player.on_collision()
                break

        self.scene.update()
        self.follow_player()

    def follow_player(self):
        self.cam.move_to((self.player.center_x - (self.cam.viewport_width * self.cam.zoom / 2),
                          self.player.center_y - (self.cam.viewport_height * self.cam.zoom / 2)))

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
        if scroll_y > 0:
            self.cam.zoom -= 0.1
        elif scroll_y < 0:
            self.cam.zoom += 0.1


if __name__ == "__main__":
    window = arcade.Window()
    window.show_view(GameView())
    window.run()

