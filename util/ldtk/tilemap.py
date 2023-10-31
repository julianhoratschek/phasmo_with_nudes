import arcade
import json

from enum import IntEnum
from pathlib import Path
from .entity import Furniture


## Readable Collision
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

        self.room_grid: list[list[int]] = []
        self.room_names: list[str] = []

        # self.stairs: arcade.SpriteList = arcade.SpriteList()
        self.furniture: arcade.SpriteList = arcade.SpriteList()

        self.width_half: int = 0
        self.height_half: int = 0

        self.player_pos: tuple[int, int] = (0, 0)
        # self.npc_pos: arcade.SpriteList = arcade.SpriteList()

    def draw_opaque(self):
        ## Draw Opaque for shaders
        self.ceilings.draw(pixelated=True)
        self.furniture.draw(pixelated=True)

    def draw_floor(self):
        self.tile_map.draw(pixelated=True)
        # self.stairs.draw(pixelated=True)

    def pixel_to_tile(self, position: tuple[int, int]) -> tuple[int, int]:
        return (int((position[0] + self.width_half) / TileMap.TileSize),
                int((self.height_half - position[1]) / TileMap.TileSize))

    def wall_collision(self, at_position: tuple[int, int]) -> bool:
        x, y = self.pixel_to_tile(at_position)
        return self.room_grid[y][x] != Collision.Floor

    def load_level(self, level_nr: int):
        lvl_path = TileMap.LevelPath / f"Level_{level_nr}"
        self.ceilings = arcade.Sprite(arcade.load_texture(lvl_path / "Ceilings.png"))
        self.tile_map = arcade.Sprite(arcade.load_texture(lvl_path / "Walls.png"))

        with open(lvl_path / f"Collision.csv", "r") as rooms_file:
            for line in rooms_file.readlines():
                self.room_grid.append([int(x) for x in line.split(",") if x.isdigit()])

        # with open(f"res/maps/{TileMap.WorldName}.ldtk", "r") as map_file:
        #    json_data = json.load(map_file)

        # for layer in json_data["defs"]["layers"]:
        #    if layer["identifier"] == "Rooms":
        #        for room_name in layer["intGridValues"]:
        #            self.room_names.append(room_name["identifier"])
        #        break

        ## Dynamic Loading of Furniture names by tag "furniture"
        with open(f"res/maps/{TileMap.WorldName}.ldtk", "r") as map_file:
            world_data = json.load(map_file)

        furniture_names = [entity_def["identifier"] for entity_def in world_data["defs"]["entities"]
                           if "furniture" in entity_def["tags"]]

        with open(lvl_path / "data.json", "r") as data_file:
            level_data = json.load(data_file)

        self.width_half = int(level_data["width"] / 2)
        self.height_half = int(level_data["height"] / 2)

        player = level_data["entities"]["Player"][0]
        self.player_pos = (player["x"] - self.width_half, self.height_half - player["y"])

        for name in furniture_names:
            if name not in level_data["entities"]:
                continue

            for furniture in level_data["entities"][name]:
                new_furniture = Furniture(
                    name=name,
                    center_x=furniture["x"] - self.width_half,
                    center_y=self.height_half - furniture["y"])
                self.furniture.append(new_furniture)

        # stairs_dict: dict[str:tuple[Stairs, str]] = dict()

        # for stairs in entity_json["entities"]["Stair"]:
        #    stairs_dict[stairs["iid"]] = (Stairs(iid=stairs["iid"], center_x=stairs["x"], center_y=stairs["y"]),
        #                                  stairs["customFields"]["Destination"]["entityIid"])

        # TODO Warp Points for Stairs
        # for stair_obj, dest in stairs_dict.values():
        #    stair_obj.destination = stairs_dict[dest][0]
        #    self.stairs.append(stair_obj)

        # for npc in entity_json["entities"]["NPC"]:
        #     # TODO Which NPC stands where? Part of Backstory-Class?
        #     #   if in Backstory: Do we need more than a position?
        #     #   if yes: why Entity and not a subclass of Entity?
        #     self.npc_pos.append(Entity(
        #         iid=npc["iid"],
        #         center_x=npc["x"],
        #         center_y=npc["y"]))
