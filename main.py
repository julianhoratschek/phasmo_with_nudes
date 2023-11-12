import arcade
from characters import Player, Direction, Ghost
from characters.ghost import GhostState
from util.ldtk import TileMap

from arcade.experimental import Shadertoy
from random import choice

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

        self.ghost: Ghost = Ghost(favourite_room=choice(self.map.room_names))
        self.ghost.set_animation("walk")
        self.scene.add_sprite(name="ghost", sprite=self.ghost)

        window_size = self.window.get_size()

        self.shadertoy = Shadertoy.create_from_file(size=window_size, path="shaders/flashlight.glsl")
        self.channel_0 = self.shadertoy.ctx.framebuffer(color_attachments=[self.shadertoy.ctx.texture(size=window_size,
                                                                                                      components=4)])
        self.channel_1 = self.shadertoy.ctx.framebuffer(color_attachments=[self.shadertoy.ctx.texture(size=window_size,
                                                                                                      components=4)])
        self.shadertoy.channel_0 = self.channel_0.color_attachments[0]
        self.shadertoy.channel_1 = self.channel_1.color_attachments[0]

        self.mouse_position: tuple[float, float] = (0.0, 0.0)
        self.elapsed_time: float = 0.0

    def on_draw(self):
        # Draw Shader

        # Draw Light collisions: Walls and furniture
        self.channel_0.use()
        self.channel_0.clear()

        self.map.draw_opaque()

        # Draw floor
        self.channel_1.use()
        self.channel_1.clear()

        self.map.draw_floor()
        self.map.draw_opaque()

        # Blip Framebuffer onto window

        self.window.use()

        self.cam.use()
        self.clear()

        self.shadertoy.render(mouse_position=self.mouse_position, time=self.elapsed_time)

        self.scene.draw(pixelated=True)

        # self.player.draw_hit_box(color=arcade.color.RED)

    def on_update(self, delta_time):
        if self.ghost.is_active():
            pass
        elif self.ghost.can_spawn():
            spawn_tile = self.map.get_free_tile(self.ghost.favourite_room)
            match self.ghost.spawn(self.map.tile_to_pixel(spawn_tile)):
                case GhostState.Roaming:
                    self.ghost.path = self.map.astar_path(spawn_tile, self.map.random_free_tile())[1:]

                case GhostState.Hunting:
                    pass

                case GhostState.HuntingSearch:
                    pass

                case GhostState.Standing:
                    pass

        self.scene.update_animation(delta_time)
        self.scene.on_update(delta_time)

        # Use Generator-expression with any
        if any(self.map.wall_collision(position) for position in self.player.get_next_positions()):
            self.player.stop()

        #for next_position in self.player.get_next_positions():
        #    if self.map.wall_collision(next_position):
        #        self.player.on_collision()
        #        break

        self.scene.update()
        self.follow_player()

        self.elapsed_time += delta_time

    def follow_player(self):
        self.cam.move_to((self.player.center_x - (self.cam.viewport_width * self.cam.zoom / 2),
                          self.player.center_y - (self.cam.viewport_height * self.cam.zoom / 2)))

    def on_key_press(self, symbol: int, modifiers: int):
        # TODO Running?
        # TODO Crouching?
        # TODO Menu?
        # TODO Interaction? Taking Items? Place Items?
        # TODO Toggle Scrolling

        if symbol in GameView.DirectionKeys:
            self.player.direction |= GameView.DirectionKeys[symbol]

    def on_key_release(self, symbol: int, modifiers: int):
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
        # TODO End actions
        pass

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        # TODO Highlight items to interact with?
        self.mouse_position = (x, y)

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

