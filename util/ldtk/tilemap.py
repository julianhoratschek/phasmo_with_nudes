import arcade
import json

from pathlib import Path
from .entity import Furniture, Stairs


class TileMap:
    LevelPath: Path = Path("res/maps/MapLayout/simplified")

    def __init__(self):
        self.tile_map: arcade.Sprite | None = None
        self.room_grid: list[list[int]] = []
        self.room_names: list[str] = []

        self.stairs: arcade.SpriteList = arcade.SpriteList()
        self.furniture: arcade.SpriteList = arcade.SpriteList()

        # TODO why Spritelists?
        # self.player_pos: arcade.SpriteList = arcade.SpriteList()
        # self.npc_pos: arcade.SpriteList = arcade.SpriteList()

    def draw_level(self):
        self.tile_map.draw(pixelated=True)
        self.furniture.draw(pixelated=True)
        self.stairs.draw(pixelated=True)

    def load_level(self, level_nr: int):
        lvl_path = TileMap.LevelPath / f"Level_{level_nr}"
        self.tile_map = arcade.Sprite(arcade.load_texture(lvl_path / "_composite.png"))

        with open(lvl_path / "Rooms.csv", "r") as rooms_file:
            for line in rooms_file.readlines():
                self.room_grid.append([int(x) for x in line.split(",") if x.isdigit()])

        with open("res/maps/MapLayout.ldtk", "r") as map_file:
            json_data = json.load(map_file)

        for layer in json_data["defs"]["layers"]:
            if layer["identifier"] == "Rooms":
                for room_name in layer["intGridValues"]:
                    self.room_names.append(room_name["identifier"])
                break

        with open(lvl_path / "data.json", "r") as entity_file:
            entity_json = json.load(entity_file)

        #for furniture in entity_json["entities"]["Furniture"]:
        #    new_furniture = Furniture(
        #        iid=furniture["iid"],
        #        center_x=furniture["x"],
        #        center_y=furniture["y"])
        #    new_furniture.can_interact = furniture["customFields"]["Interactable"]
        #    self.furniture.append(new_furniture)

        #stairs_dict: dict[str:tuple[Stairs, str]] = dict()

        #for stairs in entity_json["entities"]["Stair"]:
        #    stairs_dict[stairs["iid"]] = (Stairs(iid=stairs["iid"], center_x=stairs["x"], center_y=stairs["y"]),
        #                                  stairs["customFields"]["Destination"]["entityIid"])

        # TODO Warp Points for Stairs
        #for stair_obj, dest in stairs_dict.values():
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
        #
        # # TODO: Do we need a Player-Entity?
        # #  Why in a Spritelist? How may Player-entities are possible per map?
        # #  We have a Player-Class. What Information do we need from ldtk?
        # player = entity_json["entities"]["Player"][0]
        # self.player_pos.append(Entity(
        #     iid=player["iid"],
        #     center_x=player["x"],
        #     center_y=player["y"]))




