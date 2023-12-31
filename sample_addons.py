from pybedrock import Addons
from entities import Entities, Event, ComponentGroup
from entities import Filters, IntProperties, FloatProperties, BoolProperties
from entity_components import *
from items import *
from recipes import *

addons = Addons("PY Bedrock Test Pack")
addons.namespace = "pyb"

# Sample vanilla creeper
creeper = Entities("creeper", True, True)
creeper.addMaterial("default", "creeper")
creeper.addMaterial("charged", "charged_creeper")

creeper.addTexture("default", "textures/entity/creeper/creeper")
creeper.addTexture("charged", "textures/entity/creeper/creeper_armor")

creeper.addGeo("default", "geometry.creeper")
creeper.addGeo("charged", "geometry.creeper.charged")

creeper.addPreAnimVariable(
    "wobble", "Math.sin(query.swell_amount * 5730) * query.swell_amount * 0.01 + 1.0;"
)
creeper.addPreAnimVariable(
    "swelling_scale1",
    "(Math.pow(Math.clamp(query.swell_amount, 0.0, 1.0), 4.0) * 0.4 + 1.0) * variable.wobble;",
)
creeper.addPreAnimVariable(
    "swelling_scale2",
    "(Math.pow(Math.clamp(query.swell_amount, 0.0, 1.0), 4.0) * 0.1 + 1.0) / variable.wobble;",
)
creeper.addPreAnimVariable(
    "leg_rot",
    "Math.cos(query.modified_distance_moved * 38.17326) * 80.22 * query.modified_move_speed;",
)
creeper.addPreAnimVariable(
    "flash", "Math.mod(Math.Round(query.swell_amount * 10.0), 2.0);"
)

creeper.addAnimation(id="creeper_head", anim="animation.common.look_at_target")
creeper.addAnimation(id="creeper_legs", anim="animation.creeper.legs")
creeper.addAnimation(id="creeper_swelling", anim="animation.creeper.swelling")

creeper.addRenderController("creeper")
creeper.addAnimate("creeper_head")
creeper.addAnimate("creeper_legs")
creeper.addAnimate("creeper_swelling")

creeper.spawn_egg = {"texture": "spawn_egg", "texture_index": 6}

explodingCG = ComponentGroup("minecraft:exploding")

explodeComp = MCExplode(3)
explodeComp.fuse_length = 1.5
explodeComp.fuse_lit = True
explodeComp.causes_fire = False
explodeComp.destroy_affected_by_griefing = True

explodingCG.addComponent(explodeComp)

chargedCreeperCG = ComponentGroup("minecraft:charged_creeper")
chargedCreeperCG.addComponent(MCIsCharged())

chargedExplodingCG = ComponentGroup("minecraft:charged_exploding")
explodeComp.power = 6
chargedExplodingCG.addComponent(explodeComp)

forcedExplodingCG = ComponentGroup("minecraft:forced_exploding")
explodeComp.power = 3
forcedExplodingCG.addComponent(MCTargetNearbySensor())
forcedExplodingCG.addComponent(MCOnTargetEscape())
forcedExplodingCG.addComponent(explodeComp)

forcedChargedExplodingCG = ComponentGroup("minecraft:forced_charged_exploding")
explodeComp.power = 6
forcedChargedExplodingCG.addComponent(MCTargetNearbySensor())
forcedChargedExplodingCG.addComponent(MCOnTargetEscape())
forcedChargedExplodingCG.addComponent(explodeComp)

creeper.addComponentGroup(explodingCG)
creeper.addComponentGroup(chargedCreeperCG)
creeper.addComponentGroup(chargedExplodingCG)
creeper.addComponentGroup(forcedExplodingCG)
creeper.addComponentGroup(forcedChargedExplodingCG)

creeper.addComponent(MCIsHiddenWhenInvisible())
creeper.addComponent(MCExperienceReward("q.last_hit_by_player ? 5 : 0"))
creeper.addComponent(MCTypeFamily(["creeper", "monster", "mob"]))
creeper.addComponent(MCBreathable(total_supply=15, suffocate_time=0))
creeper.addComponent(MCNameable())
creeper.addComponent(MCCollisionBox(0.6, 0.8))
creeper.addComponent(MCMovement(value=0.2))
creeper.addComponent(MCNavigationWalk(can_path_over_water=True))
creeper.addComponent(MCMovementBasic())
creeper.addComponent(MCJumpStatic())
creeper.addComponent(MCCanClimb())
creeper.addComponent(MCHealth(value=20, max=20))
hurtCondition = MCHurtOnCondition()
condition = MCHurtOnCondition.HurtCondition()
condition.cause = "lava"
condition.damage_per_tick = 4
condition.addFilter(Filters.Test("in_lava", "self", "==", value=True))
hurtCondition.addDamageCondition(condition)
creeper.addComponent(hurtCondition)
creeper.addComponent(MCAttack(3))

damageSensor = MCDamageSensor()
damageSensor.addTrigger(
    MCDamageSensor.DamageSensor(
        MCDamageSensor.OnDamage(
            Filters.Test("is_family", "other", value="lightning"),
            "minecraft:become_charged",
        ),
        deals_damage=False,
    )
)
creeper.addComponent(damageSensor)

creeper.addComponent(
    MCTargetNearbySensor(
        2.5,
        6.0,
        True,
        TriggerEvent("minecraft:start_exploding", "self"),
        TriggerEvent("minecraft:stop_exploding", "self"),
        TriggerEvent("minecraft:stop_exploding", "self"),
    )
)
interact = MCInteract()
interaction = MCInteract.Interaction("action.interact.creeper")
interaction.swing = True
interaction.hurt_item = 1
interaction.play_sounds = "ignite"
on_interact = MCInteract.MCOnInteract()
on_interact.filters = Filters.AllOf(
    [
        Filters.Test("is_family", "other", value="player"),
        Filters.Test("has_equipment", "other", domain="hand", value="flint_and_steel"),
        Filters.Test("has_component", operator="!=", value="minecraft:explode"),
    ]
)
on_interact.event = "minecraft:start_exploding_forced"
on_interact.target = "self"
interaction.on_interact = on_interact
interact.addInteraction(interaction)
creeper.addComponent(interact)

creeper.addComponent(MCDespawn(despawn_from_distance={}))
creeper.addComponent(MCBehaviorFloat(0))
creeper.addComponent(MCBehaviorSwell(2, 2.5, 6.0))
creeper.addComponent(MCBehaviorMeleeAttack(4, 1.25, False, 0.0))
creeper.addComponent(
    MCBehaviorAvoidMobType(
        3,
        entity_types=[
            EntityType(
                max_dist=6,
                sprint_speed_multiplier=1.2,
                filters=Filters.AnyOf(
                    [
                        Filters.Test("is_family", "other", value="ocelot"),
                        Filters.Test("is_family", "other", value="cat"),
                    ]
                ),
            )
        ],
    )
)
creeper.addComponent(MCBehaviorRandomStroll(5, 1))
creeper.addComponent(MCBehaviorLookAtPlayer(6, 8))
creeper.addComponent(
    MCBehaviorNearestAttackableTarget(
        priority=1,
        must_see=True,
        must_see_forget_duration=3.0,
        entity_types=[
            EntityType(
                max_dist=16, filters=Filters.Test("is_family", "other", value="player")
            )
        ],
    )
)
creeper.addComponent(MCBehaviorHurtByTarget(2))
creeper.addComponent(MCPhysics())
creeper.addComponent(MCPushable(True, True))
creeper.addComponent(MCOnTargetEscape("minecraft:stop_exploding", "self"))
creeper.addComponent(MCConditionalBandwidthOptimization())

start_exploding_forced_event = Event("minecraft:start_exploding_forced")
start_exploding_forced_event.sequence = [
    Event.Sequence(
        Filters.Test("has_component", operator="!=", value="minecraft:is_charged"),
        add=["minecraft:forced_exploding"],
    ),
    Event.Sequence(
        Filters.Test("has_component", value="minecraft:is_charged"),
        add=["minecraft:charged_exploding"],
    ),
]
stop_exploding_event = Event("minecraft:stop_exploding")
stop_exploding_event.remove = ["minecraft:exploding"]

become_charged_event = Event("minecraft:become_charged")
become_charged_event.remove = ["minecraft:exploding"]
become_charged_event.add = ["minecraft:charged_creeper"]

creeper.addProperties(IntProperties("variant_num", True, 0, [0, 100]))
creeper.addProperties(BoolProperties("is_exploding", False, False))
creeper.addProperties(FloatProperties("swell_mult", True, 0, [0.0, 1.7]))

change_properties = Event("change_properties")
change_properties.set_property = {
    f"{addons.namespace}:variant_num": 5,
    f"{addons.namespace}:is_exploding": True,
}

creeper.events = [
    start_exploding_forced_event,
    stop_exploding_event,
    become_charged_event,
    change_properties,
]

arrow_turret_placer = Item("arrow_turret_placer")
arrow_turret_placer.addComponent(MCItemIcon("tut_arrow_turret"))
arrow_turret_placer.addComponent(
    MCItemDigger(
        [
            MCItemDigger.Block("minecraft:purple_wool", -100),
            MCItemDigger.Block("minecraft:red_wool", -100),
            MCItemDigger.Block("minecraft:yellow_wool", -100),
            MCItemDigger.Block("minecraft:lime_wool", -100),
        ],
    )
)
arrow_turret_placer.addComponent(MCItemMaxStackSize(1))
arrow_turret_placer.addComponent(
    MCItemEntityPlacer("res:tutorial_arrow_turret", use_on=["minecraft:purple_wool"])
)

furnace_recipe = FurnaceRecipe(
    "furnace_beef", FurnaceRecipe.Input("minecraft:beef", 0, 4), "minecraft:cooked_beef"
)
brewing_container_recipe = BrewingContainerRecipe(
    "brew_potion_sulphur",
    "minecraft:potion",
    "minecraft:gunpowder",
    "minecraft:splash_potion",
)
brewing_mix_recipe = BrewingMixRecipe(
    "brewing_awkward_blaze_powder",
    "minecraft:potion_type_awkward",
    "minecraft:blaze_powder",
    "minecraft:potion_type:strength",
)
shaped_recipe = ShapedRecipe(
    "acacia_boat",
    ["#P#", "###"],
    {
        "P": ShapedRecipe.Key("minecraft:wooden_shovel"),
        "#": ShapedRecipe.Key("minecraft:planks", 4),
    },
    ShapedRecipe.Result("minecraft:boat", 4),
)

shapeless_recipe = ShapelessRecipe(
    "firecharge_coal_sulphur",
    0,
    ShapelessRecipe.Ingredient("minecraft:fireball", 0, 4),
    ShapedRecipe.Result("minecraft:blaze_pwoder", 4),
)

smithing_transform_recipe = SmithingTransformRecipe(
    "smithing_netherite_boots",
    "minecraft:netherite_upgrade_smithing_template",
    "minecraft:diamond_boots",
    "minecraft:netherite_ingot",
    "minecraft:netherite_boots",
)

smithing_trim_recipe = SmithingTrimRecipe(
    "smithing_diamond_boots_jungle_quartz_trim",
    "minecraft:jungle_temple_smithing_template",
    "minecraft:diamond_boots",
    "minecraft:quartz"
)

addons.AddRecipe(furnace_recipe)
addons.AddRecipe(brewing_container_recipe)
addons.AddRecipe(brewing_mix_recipe)
addons.AddRecipe(shaped_recipe)
addons.AddRecipe(shapeless_recipe)
addons.AddRecipe(smithing_transform_recipe)
addons.AddRecipe(smithing_trim_recipe)
addons.addItem(arrow_turret_placer)
addons.addEntities(creeper)
addons.generate()
