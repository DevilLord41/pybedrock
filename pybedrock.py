from entities import Entities
from items import Item
from recipes import Recipe

import rapidjson
import uuid
import os


class Addons:
    def __init__(self, name):
        self.name = name
        self.namespace = ""
        self.min_engine_version = [1, 20, 15]
        self.entity_format_version = "1.20.0"
        self.item_format_version = "1.20.30"
        self.recipe_format_version = "1.12.0"

        # BP
        self.entities = []
        self.items = []
        self.functions = []
        self.loot_tables = []
        self.recipes = []

        self.bp_uuid = str(uuid.uuid4())
        self.bp_modules_uuid = str(uuid.uuid4())
        self.rp_uuid = str(uuid.uuid4())
        self.rp_modules_uuid = str(uuid.uuid4())
        self.dev_bp = f"{os.path.join(os.environ['LOCALAPPDATA'])}\\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang\\development_behavior_packs\\{self.name} BP"
        self.dev_rp = f"{os.path.join(os.environ['LOCALAPPDATA'])}\\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang\\development_resource_packs\\{self.name} RP"

    def addEntities(self, entity: Entities):
        self.entities.append(entity)

    def addItem(self, item: Item):
        self.items.append(item)

    def AddRecipe(self, recipe: Recipe):
        self.recipes.append(recipe)

    def checkForExist(self):
        return os.path.exists(f"{self.dev_bp}") or os.path.exists(f"{self.dev_rp}")

    def isFileExist(self, path):
        return os.path.exists(path)

    def createFolder(self):
        if self.checkForExist():
            print("Addons found, overwriting!")
            return

        print("Creating new addons!")
        os.mkdir(f"{self.dev_bp}")
        os.mkdir(f"{self.dev_rp}")

        os.mkdir(f"{self.dev_bp}\\animation_controllers")
        os.mkdir(f"{self.dev_bp}\\animations")
        os.mkdir(f"{self.dev_bp}\\entities")
        os.mkdir(f"{self.dev_bp}\\functions")
        os.mkdir(f"{self.dev_bp}\\items")
        os.mkdir(f"{self.dev_bp}\\loot_tables")
        os.mkdir(f"{self.dev_bp}\\recipes")
        os.mkdir(f"{self.dev_bp}\\structures")
        os.mkdir(f"{self.dev_bp}\\texts")

        os.mkdir(f"{self.dev_rp}\\animation_controllers")
        os.mkdir(f"{self.dev_rp}\\animations")
        os.mkdir(f"{self.dev_rp}\\entity")
        os.mkdir(f"{self.dev_rp}\\font")
        os.mkdir(f"{self.dev_rp}\\items")
        os.mkdir(f"{self.dev_rp}\\models")
        os.mkdir(f"{self.dev_rp}\\models\\entity")
        os.mkdir(f"{self.dev_rp}\\particles")
        os.mkdir(f"{self.dev_rp}\\render_controllers")
        os.mkdir(f"{self.dev_rp}\\sounds")
        os.mkdir(f"{self.dev_rp}\\texts")
        os.mkdir(f"{self.dev_rp}\\textures")

        self.createManifest()

    def formatManifest(self, dev_path, uuid, modules_uuid, min_engine_version, modules):
        manifest = {
            "format_version": 2,
            "header": {
                "name": "pack.name",
                "description": "pack.description",
                "uuid": uuid,
                "version": [1, 0, 0],
                "min_engine_version": min_engine_version,
            },
            "modules": [{"type": modules, "uuid": modules_uuid, "version": [1, 0, 0]}],
            "dependencies": [{"uuid": uuid, "version": [1, 0, 0]}],
        }

        manifest_json = rapidjson.dumps(manifest, indent=2)
        manifest_path = dev_path + "\\manifest.json"

        with open(manifest_path, "w") as manifest_file:
            manifest_file.write(manifest_json)

    def createManifest(self):
        print("Generating manifest...")
        self.formatManifest(
            self.dev_bp,
            self.bp_uuid,
            self.bp_modules_uuid,
            self.min_engine_version,
            "data",
        )
        self.formatManifest(
            self.dev_rp,
            self.rp_uuid,
            self.bp_modules_uuid,
            self.min_engine_version,
            "resources",
        )

    def flattenObject(self, k):
        if k is None:
            return None

        result = {}
        if isinstance(k, dict):
            result = {
                attr_k: attr_v
                if isinstance(attr_v, (str, int, float, bool))
                else self.flattenObject(attr_v)
                for attr_k, attr_v in k.items()
                if attr_v is not None
            }

        elif isinstance(k, list):
            result = [
                value
                if isinstance(value, (str, int, float, bool))
                else self.flattenObject(value)
                for value in k
                if value is not None
            ]

        else:
            for attr_k, attr_v in vars(k).items():
                if attr_k != "name" and "__" not in attr_k and attr_v is not None:
                    result[attr_k] = (
                        attr_v
                        if isinstance(attr_v, (str, int, float, bool))
                        else self.flattenObject(attr_v)
                    )

        return result

    def parseAnimationControllers(self, entity, ac_type):
        for ac in getattr(entity, f"{ac_type}_ac"):
            group = ac.group
            name = f"controller.animation.{group}.{ac.name}"
            ac_type_path = getattr(self, f"dev_{ac_type}")
            file_path = f"{ac_type_path}\\animation_controllers\\{group}.{'animation_controllers' if ac_type == 'rp' else 'controllers'}.json"

            ac_data = {"format_version": "1.10.0", "animation_controllers": {}}

            if self.isFileExist(file_path):
                with open(file_path, "r") as json_file:
                    ac_data = rapidjson.load(json_file)

            if name not in ac_data["animation_controllers"]:
                ac_data["animation_controllers"][name] = {"states": {}}

            for state in ac.states:
                state_data = {}
                if state.on_entry is not None:
                    state_data["on_entry"] = state.on_entry
                if state.on_exit is not None:
                    state_data["on_exit"] = state.on_exit
                if state.transitions is not None:
                    state_data["transitions"] = state.transitions
                if state.animations is not None:
                    state_data["animations"] = state.animations

                ac_data["animation_controllers"][name]["states"][
                    state.name
                ] = state_data

            with open(file_path, "w") as json_file:
                rapidjson.dump(ac_data, json_file, indent=2)

    def generateEntities(self):
        print("Generating entities...")
        bp_entities_path = self.dev_bp + "\\entities\\"
        rp_entities_path = self.dev_rp + "\\entity\\"
        for entity in self.entities:
            json_entity = {
                "format_version": f"{self.entity_format_version}",
                "minecraft:entity": {
                    "description": {
                        "identifier": f"{self.namespace}:{entity.id}",
                        "is_spawnable": entity.spawnable,
                        "is_summonable": entity.summonable,
                        "is_experimental": False,
                    }
                },
            }

            entity_description = json_entity["minecraft:entity"]["description"]

            if entity.runtime_identifier is not None:
                entity_description["runtime_identifier"] = entity.runtime_identifier

            if entity.bp_animations is not None:
                entity_description["animations"] = entity.bp_animations

            if entity.bp_animate is not None:
                entity_description["script"] = {}
                entity_description["script"]["animate"] = entity.bp_animate

            entity_bp = json_entity["minecraft:entity"]
            entity_bp["component_groups"] = {}
            entity_bp["components"] = {}
            entity_bp["events"] = {}
            component_groups = entity_bp["component_groups"]
            components = entity_bp["components"]
            events = entity_bp["events"]

            for cg in entity.component_groups:
                component_group = component_groups[cg.name] = {}
                for component in cg.components:
                    component_data = component_group[component.name] = {}
                    for k, v in vars(component).items():
                        if k == "name" or v is None:
                            continue
                        if isinstance(v, (str, int, float, bool)) or v is None:
                            component_data[k] = v
                        else:
                            component_data[k] = self.flattenObject(v)

            for c in entity.components:
                component = components[c.name] = {}
                for k, v in vars(c).items():
                    if k == "name" or v is None:
                        continue
                    if isinstance(v, (str, int, float, bool)) or v is None:
                        component[k] = v
                    else:
                        component[k] = self.flattenObject(v)

            for p in entity.properties:
                if "properties" not in entity_description:
                    entity_description["properties"] = {}
                properties = entity_description["properties"][
                    f"{self.namespace}:{p.name}"
                ] = {}
                for k, v in vars(p).items():
                    if k == "name" or v is None:
                        continue
                    if isinstance(v, (str, int, float, bool)) or v is None:
                        properties[k] = v
                    else:
                        properties[k] = self.flattenObject(v)

            for e in entity.events:
                event = events[e.name] = {}
                if e.add is not None:
                    event["add"] = {"component_groups": e.add}
                if e.remove is not None:
                    event["remove"] = {"component_groups": e.remove}
                if e.sequence is not None:
                    event["sequence"] = self.flattenObject(e.sequence)
                if e.randomize is not None:
                    event["randomize"] = self.flattenObject(e.randomize)
                if e.set_property is not None:
                    event["set_property"] = e.set_property

            json = rapidjson.dumps(json_entity, indent=2)
            filepath = bp_entities_path + "\\" + entity.id + ".json"
            with open(filepath, "w") as file:
                file.write(json)

            # print(rapidjson.dumps(json_entity, indent=2))

            self.parseAnimationControllers(entity, "rp")
            self.parseAnimationControllers(entity, "bp")

            for anim in entity.bp_anim:
                name = f"animation.{anim.group}.{anim.name}"
                file_path = f"{self.dev_bp}\\animations\\{anim.group}.tl.json"
                anim_data = {"format_version": "1.10.0", "animations": {}}

                if self.isFileExist(file_path):
                    with open(file_path, "r") as json_file:
                        anim_data = rapidjson.load(json_file)

                if name not in anim_data["animations"]:
                    anim_data["animations"][name] = {}

                if anim.loop is not None:
                    anim_data["animations"][name]["loop"] = anim.loop

                if anim.length is not None:
                    anim_data["animations"][name]["animation_length"] = anim.length

                if anim.timeline is not None:
                    anim_data["animations"][name]["timeline"] = anim.timeline

                with open(file_path, "w") as json_file:
                    rapidjson.dump(anim_data, json_file, indent=2)

            file_path = f"{self.dev_rp}\\entity\\{entity.id}.entity.json"
            json_entity = {
                "format_version": "1.10.0",
                "minecraft:client_entity": {
                    "description": {
                        "identifier": f"{self.namespace}:{entity.id}",
                        "materials": {k: v for k, v in entity.materials.items()},
                        "textures": {k: v for k, v in entity.textures.items()},
                        "geometry": {k: v for k, v in entity.geometry.items()},
                        "animations": {k: v for k, v in entity.animations.items()},
                        "render_controllers": entity.render_controllers,
                        "enable_attachables": entity.enable_attachables,
                    }
                },
            }
            if entity.spawn_egg is not None:
                json_entity["minecraft:client_entity"]["description"][
                    "spawn_egg"
                ] = entity.spawn_egg
            if any(
                (entity.scale, entity.initialize, entity.pre_animation, entity.animate)
            ):
                script_data = {}

                if entity.scale is not None:
                    script_data["scale"] = entity.scale

                if entity.initialize is not None:
                    script_data["initialize"] = entity.initialize

                if entity.pre_animation is not None:
                    script_data["pre_animation"] = entity.pre_animation

                if entity.animate is not None:
                    script_data["animate"] = entity.animate

                json_entity["minecraft:client_entity"]["description"][
                    "scripts"
                ] = script_data

            # print(rapidjson.dumps(json_entity, indent=2))
            with open(file_path, "w") as json_file:
                rapidjson.dump(json_entity, json_file, indent=2)

    def generateItems(self):
        print("Generating items...")
        bp_items_path = self.dev_bp + "\\items\\"
        for item in self.items:
            json = {
                "format_version": f"{self.item_format_version}",
                "minecraft:item": {
                    "description": {"identifier": f"{self.namespace}:{item.id}"},
                    "components": {},
                },
            }

            item_json = json["minecraft:item"]
            if item.menu_category is not None:
                item_json["menu_category"] = item.menu_category

            components = item_json["components"]
            for c in item.components:
                component = components[c.name] = {}
                for k, v in vars(c).items():
                    if k == "name" or v is None:
                        continue
                    if isinstance(v, (str, int, float, bool)) or v is None:
                        component[k] = v
                    else:
                        component[k] = self.flattenObject(v)

            json = rapidjson.dumps(json, indent=2)
            filepath = bp_items_path + "\\" + item.id + ".json"

            with open(filepath, "w") as file:
                file.write(json)

    def generateFunction(self):
        print("Generating function...")

    def generateLootTables(self):
        print("Generating loot tables...")

    def generateRecipes(self):
        print("Generating recipes...")
        bp_recipes_path = self.dev_bp + "\\recipes\\"
        for recipe in self.recipes:
            recipe_type = f"minecraft:{recipe.recipe_type}"
            json = {
                "format_version": f"{self.recipe_format_version}",
                recipe_type: {
                    "description": {"identifier": f"{self.namespace}:{recipe.identifier}"},
                },
            }

            recipe_json = json[recipe_type]

            for k, v in vars(recipe).items():
              if k == "recipe_type" or k == "identifier" or v is None:
                  continue
              if isinstance(v, (str, int, float, bool)) or v is None:
                  recipe_json[k] = v
              else:
                  recipe_json[k] = self.flattenObject(v)

            json = rapidjson.dumps(json, indent=2)
            filepath = bp_recipes_path + "\\" + recipe.identifier + ".json"

            with open(filepath, "w") as file:
                file.write(json)

    def generateText(self):
        print("Generating lang file ...")

    def generate(self):
        self.createFolder()
        self.generateEntities()
        self.generateItems()
        self.generateFunction()
        self.generateLootTables()
        self.generateRecipes()
        print("Generating addons done.")
