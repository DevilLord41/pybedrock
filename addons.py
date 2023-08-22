from pybedrock import Addons
from entities import Entities, Event, Component, ComponentGroup
from entities import AnimationController, Animation, RenderController
from entities import Filters
from entity_components import *

addons = Addons("PY Bedrock Test Pack")
addons.namespace = "pyb"

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

creeper.events = [
    start_exploding_forced_event,
    stop_exploding_event,
    become_charged_event,
]

addons.addEntities(creeper)
addons.generate()
