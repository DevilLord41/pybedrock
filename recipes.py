from __future__ import annotations
from strenum import StrEnum


class RecipeType(StrEnum):
    FURNACE = "recipe_furnace"
    BREWING_CONTAINER = "recipe_brewing_container"
    BREWING_MIX = "recipe_brewing_mix"
    SHAPED = "recipe_shaped"
    SHAPELESS = "recipe_shapeless"
    SMITHING_TRANSFORM = "recipe_smithing_transform"
    SMITHING_TRIM = "recipe_smithing_trim"


class Recipe:
    def __init__(self, recipe_type: RecipeType | str, identifier: str):
        self.recipe_type = recipe_type
        self.identifier = identifier

        if self.recipe_type == RecipeType.FURNACE:
            self.tags = ["furnace", "smoker", "campfire", "soul_campfire"]
        elif (
            self.recipe_type == RecipeType.BREWING_CONTAINER
            or self.recipe_type == RecipeType.BREWING_MIX
        ):
            self.tags = ["brewing_stand"]
        elif (
            self.recipe_type == RecipeType.SHAPED
            or self.recipe_type == RecipeType.SHAPELESS
        ):
            self.tags = ["crafting_table"]
        elif (
            self.recipe_type == RecipeType.SMITHING_TRANSFORM
            or self.recipe_type == RecipeType.SMITHING_TRIM
        ):
            self.tags = ["smithing_table"]


class FurnaceRecipe(Recipe):
    def __init__(self, identifier: str, input_id: Input, output: str):
        super().__init__(RecipeType.FURNACE, identifier)
        self.input: self.Input = input_id
        self.output: str = output

    class Input:
        def __init__(self, item: str, data: int = None, count: int = 1):
            self.item: str = item
            self.data: int = data
            self.count: int = count


class BrewingContainerRecipe(Recipe):
    def __init__(self, identifier: str, input_id: str, reagent: str, output: str):
        super().__init__(RecipeType.BREWING_CONTAINER, identifier)
        self.input: str = input_id
        self.reagent: str = reagent
        self.output: str = output


class BrewingMixRecipe(Recipe):
    def __init__(self, identifier: str, input_id: str, reagent: str, output: str):
        super().__init__(RecipeType.BREWING_MIX, identifier)
        self.input: str = input_id
        self.reagent: str = reagent
        self.output: str = output


class ShapedRecipe(Recipe):
    def __init__(self, identifier: str, pattern: list, key: dict, result: Result):
        super().__init__(RecipeType.SHAPED, identifier)
        self.pattern: list = pattern
        self.key: dict = key
        self.result: self.Result = result

    class Result:
        def __init__(self, item: str, data: int = None, count: int = None):
            self.item: str = item
            self.data: int = data
            self.count: int = count

    class Key:
        def __init__(self, item: str, data: int = None):
            self.item: str = item
            self.data: int = data


class ShapelessRecipe(Recipe):
    def __init__(
        self, identifier: str, priority: int, ingredients: Ingredient, result: Result
    ):
        super().__init__(RecipeType.SHAPELESS, identifier)
        self.priority: int = priority
        self.ingredients: self.Ingredient = ingredients
        self.result: self.Result = result

    class Ingredient:
        def __init__(self, item: str, data: int = None, count: int = None):
            self.item: str = item
            self.data: int = data
            self.count: int = count

    class Result:
        def __init__(self, item: str, data: int = None, count: int = None):
            self.item: str = item
            self.data: int = data
            self.count: int = count


class SmithingTransformRecipe(Recipe):
    def __init__(
        self, identifier: str, template: str, base: str, addition: str, result: str
    ):
        super().__init__(RecipeType.SMITHING_TRANSFORM, identifier)
        self.template: str = template
        self.base: str = base
        self.addition: str = addition
        self.result: str = result


class SmithingTrimRecipe(Recipe):
    def __init__(self, identifier: str, template: str, base: str, addition: str):
        super().__init__(RecipeType.SMITHING_TRIM, identifier)
        self.template: str = template
        self.base: str = base
        self.addition: str = addition
