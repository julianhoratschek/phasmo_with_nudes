import arcade
import json

from enum import IntEnum
from pathlib import Path
from .entity import Furniture
from random import choice

import heapq


class Node:
    def __init__(self, position=(0, 0), g_score=float('inf'), f_score=float('inf'), predecessor=None):
        self.position: tuple[int, int] = position
        self.g_score: float = g_score
        self.predecessor = predecessor
        self.f_score: float = f_score

    def __lt__(self, other):
        return self.f_score < other.f_score


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

    MovementDegrees: tuple[tuple[int, int, float]] = ((-1, -1, 1.5), (-1, 0, 1.0),
                                                      (-1, 1, 1.5), (0, -1, 1.0),
                                                      (0, 1, 1.0), (1, -1, 1.5),
                                                      (1, 0, 1.0), (1, 1, 1.5))

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
        # self.npc_pos: arcade.SpriteList = arcade.SpriteList()

        self.lp = (0, 0)

    def has_line_of_sight(self, observer: tuple[float, float], target: tuple[float, float]) -> bool:
        x0, y0 = int(observer[0]), int(observer[1])
        x1, y1 = int(target[0]), int(target[1])

        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        error = dx + dy

        while True:
            if coll := arcade.get_sprites_at_point((x0, y0), self.furniture):
                print(coll)
                for c in coll:
                    c.color = arcade.color.RED
                self.lp = (x0, y0)
                return False

            if self.wall_collision((x0, y0)):
                print("wall coll")
                self.lp = (x0, y0)
                return False

            if x0 == x1 and y0 == y1:
                break

            # TODO Raylength

            e2 = 2 * error
            if e2 >= dy:
                if x0 == x1:
                    break
                error += dy
                x0 += sx

            if e2 <= dx:
                if y0 == y1:
                    break
                error += dx
                y0 += sy
        self.lp = (x0, y0)
        return True

    def random_free_tile(self) -> tuple[int, int]:
        return choice(self.room[choice(list(self.room.keys()))])

    def neighbours(self, tile_position: tuple[int, int]) -> list[tuple[tuple[int, int], float]]:
        for x_pos, y_pos, cost in TileMap.MovementDegrees:
            x_yield, y_yield = tile_position[0] + x_pos, tile_position[1] + y_pos

            if (-1 < x_yield < len(self.collision_grid)
                    and -1 < y_yield < len(self.collision_grid[x_yield])
                    and self.collision_grid[x_yield][y_yield] == Collision.Floor):
                yield (x_yield, y_yield), cost

    def astar_pixel_path(self, target_node: Node) -> list[tuple[int, int]]:
        result = [self.tile_to_pixel(target_node.position)]
        current_node = target_node.predecessor
        while current_node:
            result.append(self.tile_to_pixel(current_node.position))
            current_node = current_node.predecessor
        return list(reversed(result))

    def astar_path(self, from_tile: tuple[int, int], to_tile: tuple[int, int]) -> list[tuple[int, int]]:
        current_node = Node(position=from_tile, f_score=0.0)
        open_list = [current_node]
        closed_list = set()

        while len(open_list):
            current_node = heapq.heappop(open_list)
            if current_node.position == to_tile:
                return self.astar_pixel_path(current_node)

            closed_list.add(current_node.position)

            for successor_position, cost in self.neighbours(current_node.position):
                if successor_position in closed_list:
                    continue

                tentative_g = current_node.g_score + cost

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

