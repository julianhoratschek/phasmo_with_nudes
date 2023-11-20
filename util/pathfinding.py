import arcade

from .ldtk.tilemap import TileMap, Collision
import heapq


class AStarNode:
    def __init__(self, position=(0, 0), g_score=float('inf'), f_score=float('inf'), predecessor=None):
        self.position: tuple[int, int] = position
        self.g_score: float = g_score
        self.predecessor = predecessor
        self.f_score: float = f_score

    def __lt__(self, other):
        return self.f_score < other.f_score


class TileMapPath:
    MovementDegrees: tuple[tuple[int, int, float]] = ((-1, -1, 1.5), (-1, 0, 1.0),
                                                      (-1, 1, 1.5), (0, -1, 1.0),
                                                      (0, 1, 1.0), (1, -1, 1.5),
                                                      (1, 0, 1.0), (1, 1, 1.5))

    def __init__(self, tile_map: TileMap):
        self.tile_map: TileMap = tile_map

    def __reconstruct_pixel_path(self, target_node: AStarNode) -> list[tuple[int, int]]:
        result = [self.tile_map.tile_to_pixel(target_node.position)]
        current_node = target_node.predecessor
        while current_node:
            result.append(self.tile_map.tile_to_pixel(current_node.position))
            current_node = current_node.predecessor
        return list(reversed(result))

    def __neighbours(self, tile_position: tuple[int, int]) -> list[tuple[tuple[int, int], float]]:
        for x_pos, y_pos, cost in TileMapPath.MovementDegrees:
            x_yield, y_yield = tile_position[0] + x_pos, tile_position[1] + y_pos

            if (-1 < x_yield < len(self.tile_map.collision_grid)
                    and -1 < y_yield < len(self.tile_map.collision_grid[x_yield])
                    and self.tile_map.collision_grid[x_yield][y_yield] == Collision.Floor):
                yield (x_yield, y_yield), cost

    def has_line_of_sight(self, observer: tuple[float, float], target: tuple[float, float]) -> bool:
        x0, y0 = int(observer[0]), int(observer[1])
        x1, y1 = int(target[0]), int(target[1])

        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        error = dx + dy

        while True:
            # TODO optimize
            if (self.tile_map.wall_collision((x0, y0))
                    or arcade.get_sprites_at_point((x0, y0), self.tile_map.furniture)):
                return False

            if x0 == x1 and y0 == y1:
                break

            # TODO Raylength aa

            e2 = 2 * error
            if e2 > dy:
                if x0 == x1:
                    break
                error += dy
                x0 += sx

            if e2 < dx:
                if y0 == y1:
                    break
                error += dx
                y0 += sy

        return True

    def heuristic(self, from_tile, to_tile):
        return (from_tile[0] - to_tile[0]) ** 2 + (from_tile[1] - to_tile[1]) ** 2

    def get_path(self, from_tile: tuple[int, int], to_tile: tuple[int, int]) -> list[tuple[int, int]]:
        current_node = AStarNode(position=from_tile, f_score=0.0)
        open_list = [current_node]
        closed_list = set()

        while len(open_list):
            current_node = heapq.heappop(open_list)
            if current_node.position == to_tile:
                return self.__reconstruct_pixel_path(current_node)

            closed_list.add(current_node.position)

            for successor_position, cost in self.__neighbours(current_node.position):
                if successor_position in closed_list:
                    continue

                tentative_g = current_node.g_score + cost

                successor = None
                for listed in open_list:
                    if successor_position == listed.position:
                        successor = listed
                        break

                f_score = tentative_g + self.heuristic(successor_position, to_tile)
                if successor:
                    if tentative_g >= successor.g_score:
                        continue

                    successor.f_score = f_score
                    heapq.heapify(open_list)
                else:
                    successor = AStarNode(position=successor_position,
                                          g_score=tentative_g,
                                          f_score=f_score,
                                          predecessor=current_node)
                    heapq.heappush(open_list, successor)
        return []

