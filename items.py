from __future__ import annotations
from entities import Component
from strenum import StrEnum


class Item:
    def __init__(self, id, name = None):
        self.id = id
        self.name = name
        self.components = []
        self.menu_category = None

    def addComponent(self, component: Component):
        self.components.append(component)

    def setCategory(self, category):
        if self.menu_category == None:
            self.menu_category = {}

        self.menu_category["category"] = category

    def setGroup(self, group):
        if self.menu_category == None:
            self.menu_category = {}

        self.menu_category["group"] = group

    def setHiddenInCommand(self, hidden):
        if self.menu_category == None:
            self.menu_category = {}

        self.menu_category["is_hidden_in_commands"] = hidden


class MCItemEnchantable(Component):
    def __init__(self, slot: str, value: float):
        super().__init__("minecraft:enchantable")
        self.slot: str = slot
        self.value: float = value

    class Type(StrEnum):
        HELMET = "armor_head"
        CHESTPLATE = "armor_torso"
        LEGGINGS = "armor_legs"
        BOOTS = "armor_feet"
        AXE = "axe"
        BOW = "bow"
        COSMETIC_HEAD = "cosmetic_head"
        CROSSBOW = "crossbow"
        ELYTRA = "elytra"
        FISHING_ROD = "fishing_rod"
        FLINTSTEEL = "flintsteel"
        HOE = "hoe"
        PICKAXE = "pickaxe"
        SHEARS = "shears"
        SHIELD = "shield"
        SHOVEL = "shovel"
        SWORD = "sword"
        ALL = "all"


class MCItemDisplayName(Component):
    def __init__(self, value: str):
        super().__init__("minecraft:display_name")
        self.value: str = value


class MCItemHoverTextColor(Component):
    def __init__(self, value: str):
        super().__init__("minecraft:hover_text_color")
        self.value: str = value


class MCItemHandEquipped(Component):
    def __init__(self, value: bool):
        super().__init__("minecraft:hand_equipped")
        self.value: bool = value

class MCItemLiquidClipped(Component):
    def __init__(self, value: bool):
        super().__init__("minecraft:liquid_clipped")
        self.value: bool = value


class MCItemGlint(Component):
    def __init__(self, value: bool):
        super().__init__("minecraft:glint")
        self.value: bool = value


class MCItemFuel(Component):
    def __init__(self, duration: float):
        super().__init__("minecraft:fuel")
        self.duration: float = duration


class MCItemDamage(Component):
    def __init__(self, value: float):
        super().__init__("minecraft:damage")
        self.value: float = value


class MCItemAllowOffHand(Component):
    def __init__(self, value: bool):
        super().__init__("minecraft:allow_off_hand")
        self.value: bool = value


class MCItemIcon(Component):
    def __init__(self, texture: str):
        super().__init__("minecraft:icon")
        self.texture: str = texture


class MCItemMaxStackSize(Component):
    def __init__(self, value: int):
        super().__init__("minecraft:max_stack_size")
        self.value: int = value


class MCItemUseDuration(Component):
    def __init__(self, value: float):
        super().__init__("minecraft:use_duration")
        self.value: float = value


class MCItemUseAnimation(Component):
    def __init__(self, value: str):
        super().__init__("minecraft:use_animation")
        self.value: str = value


class MCItemStackedBydata(Component):
    def __init__(self, value: bool):
        super().__init__("minecraft:stacked_by_data")
        self.value: bool = value


class MCItemShouldDespawn(Component):
    def __init__(self, value: bool):
        super().__init__("minecraft:should_despawn")
        self.value: bool = value


class MCItemCooldown(Component):
    def __init__(self, category: str, duration: float):
        super().__init__("minecraft:cooldown")
        self.category: str = category
        self.duration: float = duration


class MCItemCanDestroyInCreative(Component):
    def __init__(self, value: bool):
        super().__init__("minecraft:can_destroy_in_creative")
        self.value: bool = value


class MCItemBlockPlacer(Component):
    def __init__(self, block: str, use_on: list):
        super().__init__("minecraft:block_placer")
        self.block: str = block
        self.use_on: list = use_on


class MCItemWearable(Component):
    def __init__(self, slot: str, protection: int):
        super().__init__("minecraft:wearable")
        self.slot: str = slot
        self.protection: int = protection

    class Type(StrEnum):
        HELMET = "slot.armor.head"
        CHESTPLATE = "slot.armor.chest"
        LEGGINGS = "slot.armor.legs"
        BOOTS = "slot.armor.feet"
        OFFHAND = "slot.weapon.offhand"


class MCItemDurability(Component):
    def __init__(self, damage_chance: dict, max_durability: int):
        super().__init__("minecraft:wearable")
        self.damage_chance: dict = damage_chance
        self.max_durability: int = max_durability

class MCItemProjectile(Component):
    def __init__(self, minimum_critical_power: float, projectile_entity: str):
        super().__init__("minecraft:projectile")
        self.minimum_critical_power: float = minimum_critical_power
        self.projectile_entity: str = projectile_entity

class MCItemRecord(Component):
    def __init__(self, sound_event: str, duration: int, comparator_signal: int):
        super().__init__("minecraft:record")
        self.sound_event: str = sound_event
        self.duration: int = duration
        self.comparator_signal: int = comparator_signal


class MCItemDigger(Component):
    def __init__(self, destroy_speeds: list, use_efficiency: bool = None):
        super().__init__("minecraft:digger")
        self.destroy_speeds: list = destroy_speeds
        self.use_efficiency: bool = use_efficiency

    class Block:
        def __init__(self, block: str, speed: int):
            self.block: str = block
            self.speed: int = speed


class MCItemEntityPlacer(Component):
    def __init__(self, entity: str, dispense_on: list = None, use_on: list = None):
        super().__init__("minecraft:entity_placer")
        self.entity: str = entity
        self.dispense_on: list = dispense_on
        self.use_on: list = use_on


class MCItemFood(Component):
    def __init__(
        self,
        can_always_eat: bool,
        nutrition: int,
        saturation_modifier: float,
        using_converts_to: str,
        effects: list = None,
    ):
        super().__init__("minecraft:food")
        self.can_always_eat: bool = can_always_eat
        self.nutrition: int = nutrition
        self.saturation_modifier: float = saturation_modifier
        self.using_converts_to: str = using_converts_to
        self.effects: list = effects

    class Effect:
        def __init__(self, name: str, chance: float, duration: int, amplifier: int):
            self.name: str = name
            self.chance: float = chance
            self.duration: int = duration
            self.amplifier: int = amplifier


class MCItemThrowable(Component):
    def __init__(
        self,
        do_swing_animation: bool,
        launch_power_scale: float,
        max_draw_duration: float,
        max_launch_power: float,
        min_draw_duration: float,
        scale_power_by_draw_duration: bool,
    ):
        super().__init__("minecraft:throwable")
        self.do_swing_animation: bool = do_swing_animation
        self.launch_power_scale: float = launch_power_scale
        self.max_draw_duration: float = max_draw_duration
        self.max_launch_power: float = max_launch_power
        self.min_draw_duration: float = min_draw_duration
        self.scale_power_by_draw_duration: bool = scale_power_by_draw_duration


class MCItemShooter(Component):
    def __init__(
        self,
        ammunition: list,
        charge_on_draw: bool,
        scale_power_by_draw_duration: bool,
        max_draw_duration: bool,
    ):
        super().__init__("minecraft:wearable")
        self.ammunition: list = ammunition
        self.charge_on_draw: bool = charge_on_draw
        self.scale_power_by_draw_duration: bool = scale_power_by_draw_duration
        self.max_draw_duration: bool = max_draw_duration

    class Ammunition:
        def __init__(
            self,
            item: str,
            use_offhand: bool,
            search_inventory: bool,
            use_in_creative: bool,
        ):
            self.item: str = item
            self.use_offhand: bool = use_offhand
            self.search_inventory: bool = search_inventory
            self.use_in_creative: bool = use_in_creative


class MCItemRepairable(Component):
    def __init__(self, repair_items: list):
        super().__init__("minecraft:repairable")
        self.repair_items: list = repair_items

    class RepairItem:
        def __init__(self, items: list, repair_amount: float):
            self.items = items
            self.repair_amount = repair_amount
