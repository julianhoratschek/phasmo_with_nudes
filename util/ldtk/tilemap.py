import arcade
import json

from enum import IntEnum
from pathlib import Path
from .entity import Furniture
from random import choice


class Collision(IntEnum):
    Floor = 1
    Wall = 2
    Ceiling = 3


class TileMap:
    WorldName: str = "phasmo_world"

    LevelPath: Path = Path(f"res/maps/{WorldName}/simplified")
    TileSize: int = 32

    def __init__(self):
        self.ceilings: arcade.Sprite | None = None
        self.tile_map: arcade.Sprite | None = None
        self.decoration: arcade.Sprite | None = None

        self.collision_grid: list[list[int]] = []

        self.room: dict[str, list[tuple[int, int]]] = dict()
        self.room_names: list[str] = []

        self.furniture: arcade.SpriteList = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=32)

        self.width_half: int = 0
        self.height_half: int = 0

        self.player_pos: tuple[int, int] = (0, 0)

    def random_free_tile(self) -> tuple[int, int]:
        return choice(self.room[choice(list(self.room.keys()))])

    def draw_opaque(self):
        self.ceilings.draw(pixelated=True)
        self.furniture.draw(pixelated=True)

    def draw_floor(self):
        self.tile_map.draw(pixelated=True)
        self.decoration.draw(pixelated=True)
        # self.stairs.draw(pixelated=True)

    def pixel_to_tile(self, position: tuple[int, int]) -> tuple[int, int]:
        return (int((position[0] + self.width_half) / TileMap.TileSize),
                int((self.height_half - position[1]) / TileMap.TileSize))

    def tile_to_pixel(self, position: tuple[int, int]) -> tuple[int, int]:
        return (int(position[0] * TileMap.TileSize - self.width_half),
                int(-position[1] * TileMap.TileSize + self.height_half))

    def wall_collision(self, at_position: tuple[int, int]) -> bool:
        x, y = self.pixel_to_tile(at_position)

        return not (-1 < x < len(self.collision_grid)
                    and -1 < y < len(self.collision_grid[x])
                    and self.collision_grid[x][y] == Collision.Floor)

    def get_free_tile(self, room_name: str) -> tuple[int, int] | None:
        while True:
            tile = choice(self.room[room_name])
            tile_px = self.tile_to_pixel(tile)
            if not arcade.get_sprites_in_rect((tile_px[0] + 2, tile_px[0] + 30, tile_px[1] + 2, tile_px[1] + 30),
                                              self.furniture):
                return tile

    def load_level(self, level_nr: int):
        # TODO Reloadability
        lvl_path = TileMap.LevelPath / f"Level_{level_nr}"
        self.ceilings = arcade.Sprite(arcade.load_texture(lvl_path / "Ceilings.png"))
        self.tile_map = arcade.Sprite(arcade.load_texture(lvl_path / "WallsNFloors.png"))
        self.decoration = arcade.Sprite(arcade.load_texture(lvl_path / "Decoration.png"))

        # Load Collision
        with open(lvl_path / f"Collision.csv", "r") as rooms_file:
            self.collision_grid = [[int(x) for x in line.split(",") if x.isdigit()]
                                   for line in rooms_file.readlines()]

        self.collision_grid = list(map(list, zip(*self.collision_grid)))

        # Load Global Data
        with open(f"res/maps/{TileMap.WorldName}.ldtk", "r") as map_file:
            world_data = json.load(map_file)

        # Load Level Data
        with open(lvl_path / "data.json", "r") as data_file:
            level_data = json.load(data_file)

        self.width_half = int(level_data["width"] / 2)
        self.height_half = int(level_data["height"] / 2)

        player = level_data["entities"]["Player"][0]
        self.player_pos = (player["x"] - self.width_half, self.height_half - player["y"])

        # Load all room names
        room_values = None
        for layer_def in world_data["defs"]["layers"]:
            if layer_def["identifier"] == "Rooms":
                room_values = layer_def["intGridValues"]
                break
        # TODO else:
        self.room_names = [room_def["identifier"] for room_def in room_values]

        # Load Furniture Entities
        furniture_names = [entity_def["identifier"] for entity_def in world_data["defs"]["entities"]
                           if "furniture" in entity_def["tags"]]

        self.furniture.clear()
        for name in furniture_names:
            if name not in level_data["entities"]:
                continue

            for furniture in level_data["entities"][name]:
                # TODO Hitboxes
                new_furniture = Furniture(
                    name=name,
                    center_x=furniture["x"] - self.width_half,
                    center_y=self.height_half - furniture["y"])
                self.furniture.append(new_furniture)

        #load room grid
        with open(lvl_path / "Rooms.csv", "r") as grid_file:
            for row, line in enumerate(grid_file.readlines()):
                for col, room_int in enumerate(map(int, line.split(",")[:-1])):
                    if room_int == 0:
                        continue
                    name = self.room_names[room_int - 1]
                    if name not in self.room:
                        self.room[name] = []
                    self.room[name].append((col, row))

