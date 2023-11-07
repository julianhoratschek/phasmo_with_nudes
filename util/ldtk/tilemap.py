import arcade
import json

from enum import IntEnum
from pathlib import Path
from .entity import Furniture
from random import choice

import heapq
from dataclasses import dataclass, field


@dataclass
class Node:
    position: tuple[int, int] = field(default=(0, 0), compare=False)
    g_score: float = field(default=float('inf'), compare=False)
    predecessor: "Node" = field(default=None, compare=False)
    f_score: float = float('inf')


class Collision(IntEnum):
    Floor = 1
    Wall = 2
    Ceiling = 3


def astar_heuristic(from_tile, to_tile):
    return (from_tile[0] - to_tile[0]) ** 2 + (from_tile[1] - to_tile[1]) ** 2


class TileMap:
    WorldName: str = "phasmo_world"

    LevelPath: Path = Path(f"res/maps/{WorldName}/simplified")
    TileSize: int = 32

    MovementDegrees: tuple[tuple[int, int]] = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

    def __init__(self):
        self.ceilings: arcade.Sprite | None = None
        self.tile_map: arcade.Sprite | None = None

        self.collision_grid: list[list[int]] = []

        self.room: dict[str, list[tuple[int, int]]] = dict()
        self.room_names: list[str] = []

        # self.stairs: arcade.SpriteList = arcade.SpriteList()
        self.furniture: arcade.SpriteList = arcade.SpriteList()

        self.width_half: int = 0
        self.height_half: int = 0

        self.player_pos: tuple[int, int] = (0, 0)
        # self.npc_pos: arcade.SpriteList = arcade.SpriteList()

    def neighbours(self, tile_position):
        return [(x_pos, y_pos) for x_pos, y_pos in map(lambda p: (tile_position[0] + p[0], tile_position[1] + p[1]),
                                                       TileMap.MovementDegrees)
                if (-1 < x_pos < len(self.collision_grid) and
                    -1 < y_pos < len(self.collision_grid[x_pos]) and
                    self.collision_grid[x_pos][y_pos] == Collision.Floor)
                ]

    def astar_pixel_path(self, target_node) -> list[tuple[int, int]]:
        result = [self.tile_to_pixel(target_node.position)]
        current_node = target_node.predecessor
        while current_node:
            result.append(self.tile_to_pixel(current_node.position))
            current_node = current_node.predecessor
        return list(reversed(result))

    def astar_path(self, from_tile, to_tile) -> list[tuple[int, int]]:
        current_node = Node(position=from_tile, f_score=0.0)
        open_list = [current_node]
        closed_list = set()

        while len(open_list):
            current_node = heapq.heappop(open_list)
            if current_node.position == to_tile:
                return self.astar_pixel_path(current_node)

            closed_list.add(current_node.position)

            for successor_position in self.neighbours(current_node.position):
                if successor_position in closed_list:
                    continue

                tentative_g = current_node.g_score + 1.0

                successor = None
                for listed in open_list:
                    if successor_position == listed.position:
                        successor = listed
                        break

                f_score = tentative_g + astar_heuristic(successor_position, to_tile)
                if successor:
                    if tentative_g >= successor.g_score:
                        continue

                    successor.f_score = f_score
                    heapq.heapify(open_list)
                else:
                    successor = Node(position=successor_position,
                                     g_score=tentative_g,
                                     f_score=f_score,
                                     predecessor=current_node)
                    heapq.heappush(open_list, successor)
        return []

    def draw_opaque(self):
        self.ceilings.draw(pixelated=True)
        self.furniture.draw(pixelated=True)

    def draw_floor(self):
        self.tile_map.draw(pixelated=True)
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

    def set_on_free_tile(self, sprite: arcade.Sprite, room: str):
        while True:
            sprite.position = self.tile_to_pixel(choice(self.room[room]))
            if not sprite.collides_with_list(self.furniture):
                break

    def load_level(self, level_nr: int):
        lvl_path = TileMap.LevelPath / f"Level_{level_nr}"
        self.ceilings = arcade.Sprite(arcade.load_texture(lvl_path / "Ceilings.png"))
        self.tile_map = arcade.Sprite(arcade.load_texture(lvl_path / "WallsNFloors.png"))

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

        for name in furniture_names:
            if name not in level_data["entities"]:
                continue

            for furniture in level_data["entities"][name]:
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

