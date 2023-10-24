from __future__ import annotations
from entities import Event, Component, Filters


class TriggerEvent:
    def __init__(self, event: str, target: str = None):
        self.event: str = event
        self.target: str = target


class TriggerEventFilter:
    def __init__(self, event: str, target: str = None, filters: Filters = None):
        self.event: str = event
        self.target: str = target
        self.filters: str = filters


class EntityType:
    def __init__(
        self,
        filters: Filters = None,
        max_dist: int = None,
        check_if_outnumbered: int = None,
        max_flee: int = None,
        max_height: int = None,
        must_see: bool = None,
        must_see_forget_duration: int = None,
        priority: int = None,
        reevaluate_description: bool = None,
        sprint_speed_multiplier: float = None,
        walk_speed_multiplier: float = None,
    ):
        self.filters: Filters = filters
        self.max_dist: int = max_dist
        self.check_if_outnumbered: int = check_if_outnumbered
        self.max_flee: int = max_flee
        self.max_height: int = max_height
        self.must_see: bool = must_see
        self.must_see_forget_duration: int = must_see_forget_duration
        self.priority: int = priority
        self.reevaluate_description: bool = reevaluate_description
        self.sprint_speed_multiplier: float = sprint_speed_multiplier
        self.walk_speed_multiplier: float = walk_speed_multiplier


class MCPhysics(Component):
    def __init__(self, has_collision: bool = None, has_gravity: bool = None):
        super().__init__("minecraft:physics")
        self.has_collision: bool = has_collision
        self.has_gravity: bool = has_gravity


class MCRideable(Component):
    def __init__(
        self,
        seat_count: int = None,
        family_types: list = None,
        interact_text: str = None,
        controlling_seat: int = None,
        crouching_skip_interact: bool = None,
        pull_in_entities: bool = None,
        rider_can_interact: bool = None,
        passenger_max_width: float = None,
        seats: list = None,
    ):
        super().__init__("minecraft:rideable")
        self.seat_count: int = seat_count
        self.family_types: list = family_types
        self.interact_text: str = interact_text
        self.controlling_seat: int = controlling_seat
        self.crouching_skip_interact: bool = crouching_skip_interact
        self.pull_in_entities: bool = pull_in_entities
        self.rider_can_interact: bool = rider_can_interact
        self.passenger_max_width: float = passenger_max_width
        self.seats: list = seats

        class MCSeats:
            def __init__(self, position: list = []):
                self.position = position
                self.lock_rider_rotation = None
                self.rotate_rider_by = None
                self.max_rider_count = None
                self.min_rider_count = None


class MCInteract(Component):
    def __init__(self):
        super().__init__("minecraft:interact")
        self.interactions: list = []

    def addInteraction(self, interaction: Interaction):
        self.interactions.append(interaction)

    class Interaction:
        def __init__(
            self,
            interact_text: str = None,
            vibration: str = None,
            use_item: bool = None,
            transform_to_item: str = None,
            swing: bool = None,
            hurt_item: int = None,
            spawn_items: dict = None,
            spawn_entities: str = None,
            play_sounds: str = None,
            particle_on_start: MCInteract.MCInteractParticle = None,
            on_interact: MCInteract.MCOnInteract = None,
            equip_item_slot: int = None,
            cooldown_after_being_attacked: float = None,
            cooldown: float = None,
            add_items: dict = None,
        ):
            self.interact_text: str = interact_text
            self.vibration: str = vibration
            self.use_item: bool = use_item
            self.transform_to_item: str = transform_to_item
            self.swing: bool = swing
            self.hurt_item: int = hurt_item
            self.spawn_items: dict = spawn_items
            self.spawn_entities: str = spawn_entities
            self.play_sounds: str = play_sounds
            self.particle_on_start: MCInteract.MCInteractParticle = particle_on_start
            self.on_interact: MCInteract.MCOnInteract = on_interact
            self.equip_item_slot: int = equip_item_slot
            self.cooldown_after_being_attacked: float = cooldown_after_being_attacked
            self.cooldown: float = cooldown
            self.add_items: dict = add_items

    class MCOnInteract:
        def __init__(self, event: str, target: str = None, filters: Filters = None):
            self.event: str = event
            self.target: str = target
            self.filters: Filters = filters

    class MCInteractParticle:
        def __init__(
            self,
            particle_offset_towards_interactor: bool = None,
            particle_type: str = None,
            particle_y_offset: int = None,
        ):
            self.particle_offset_towards_interactor = particle_offset_towards_interactor
            self.particle_type = particle_type
            self.particle_y_offset = particle_y_offset


class MCExplode(Component):
    def __init__(self, power: float):
        super().__init__("minecraft:explode")
        self.break_blocks: bool = None
        self.causes_fire: bool = None
        self.destroy_affected_by_griefing: bool = None
        self.fire_affected_by_griefing: bool = None
        self.fuse_length: list | float = None
        self.fuse_lit: bool = None
        self.power: float = power
        self.max_resistance: bool = None


class MCMovement(Component):
    def __init__(self, value: float, max: float = None):
        super().__init__("minecraft:movement")
        self.max: float = max
        self.value: float = value


class MCFlyingSpeed(Component):
    def __init__(self, value: float):
        super().__init__("minecraft:flying_speed")
        self.value: float = value


class MCFireImmune(Component):
    def __init__(self):
        super().__init__("minecraft:fire_immune")


class MCKnockbackResistance(Component):
    def __init__(self, value: float, max: float = None):
        super().__init__("minecraft:knockback_resistance")
        self.max: float = max
        self.value: float = value


class MCTimer(Component):
    def __init__(
        self, time: float | list, time_down_event: TriggerEvent, looping: bool = None
    ):
        super().__init__("minecraft:timer")
        self.time: float | list = time
        self.looping: bool = looping
        self.time_down_event: TriggerEvent = time_down_event


class MCIsHiddenWhenInvisible(Component):
    def __init__(self):
        super().__init__("minecraft:is_hidden_when_invisible")


class MCExperienceReward(Component):
    def __init__(self, on_death: str = None, on_bred: str = None):
        super().__init__("minecraft:experience_reward")
        self.on_death: str = None
        self.on_bred: str = None


class MCTypeFamily(Component):
    def __init__(self, family: list):
        super().__init__("minecraft:type_family")
        self.family: list = family

class MCLoot(Component):
    def __init__(self, table: str):
        super().__init__("minecraft:loot")
        self.table: str = table


class MCBalloonable(Component):
    def __init__(
        self,
        mass: float = None,
        max_distance: float = None,
        on_ballon: str = None,
        on_unballon: str = None,
        soft_distance: float = None,
    ):
        super().__init__("minecraft:balloonable")
        self.mass: float = mass
        self.max_distance: float = max_distance
        self.on_ballon: str = on_ballon
        self.on_unballon: str = on_unballon
        self.soft_distance: float = soft_distance


class MCLeashable(Component):
    def __init__(
        self,
        soft_distance: float = None,
        hard_distance: float = None,
        max_distance: float = None,
        can_be_stolen: bool = None,
        on_leash: TriggerEvent = None,
        on_unleash: TriggerEvent = None,
    ):
        super().__init__("minecraft:leashable")
        self.soft_distance: float = soft_distance
        self.hard_distance: float = hard_distance
        self.max_distance: float = max_distance
        self.can_be_stolen: bool = can_be_stolen
        self.on_leash: TriggerEvent = on_leash
        self.on_unleash: TriggerEvent = on_unleash


class MCBreathable(Component):
    def __init__(
        self,
        total_supply: float = None,
        suffocate_time: float = None,
        breathe_blocks: list = None,
        breathes_air: bool = None,
        breathes_lava: bool = None,
        breathes_solids: bool = None,
        breathes_water: bool = None,
        generates_bubbles: bool = None,
        inhale_time: float = None,
        non_breathe_blocks: list = None,
    ):
        super().__init__("minecraft:breathable")
        self.total_supply: float = total_supply
        self.suffocate_time: float = suffocate_time
        self.breathe_blocks: list = breathe_blocks
        self.breathes_air: bool = breathes_air
        self.breathes_lava: bool = breathes_lava
        self.breathes_solids: bool = breathes_solids
        self.breathes_water: bool = breathes_water
        self.generates_bubbles: bool = generates_bubbles
        self.inhale_time: float = inhale_time
        self.non_breathe_blocks: list = non_breathe_blocks


class MCNameable(Component):
    def __init__(self, allow_name_tag_renaming: bool = None, always_show: bool = None):
        super().__init__("minecraft:nameable")
        self.always_show: bool = None
        self.allow_name_tag_renaming: bool = None
        self.default_trigger: TriggerEvent = None
        self.name_actions: list = None

        class NameAction:
            def __init__(self, name_filter: str = None, on_named: TriggerEvent = None):
                self.name_filter = name_filter
                self.on_named = on_named


class MCCollisionBox(Component):
    def __init__(self, width: float, height: float):
        super().__init__("minecraft:collision_box")
        self.width = width
        self.height = height


class MCCustomHitTest(Component):
    def __init__(self, hitboxes: list):
        super().__init__("minecraft:custom_hit_test")
        self.hitboxes = hitboxes

    class Hitbox:
        def __init__(self, width: float, height: float, pivot: list):
            self.width = width
            self.height = height
            self.pivot = pivot


class MCFollowRange(Component):
    def __init__(self, value: float, max: float = None):
        super().__init__("minecraft:follow_range")
        self.value = value
        self.max = max


class MCHealth(Component):
    def __init__(self, value: float, min: float = None, max: float = None):
        super().__init__("minecraft:health")
        self.value = value
        self.min = min
        self.max = max


class NCAmbientSoundInterval(Component):
    def __init__(
        self,
        value: float = None,
        range: float = None,
        event_name: float = None,
        event_names: list = None,
    ):
        super().__init__("minecraft:ambient_sound_interval")
        self.value: float = value
        self.range: float = range
        self.event_name: float = event_name
        self.event_names: list = event_names


class MCAttack(Component):
    def __init__(
        self, damage: float, effect_duration: float = None, effect_name: str = None
    ):
        super().__init__("minecraft:attack")
        self.damage = damage
        self.effect_name = effect_name
        self.effect_duration = effect_duration


class MCDamageSensor(Component):
    def __init__(self):
        super().__init__("minecraft:damage_sensor")
        self.triggers: list = None

    def addTrigger(self, trigger: DamageSensor):
        if self.triggers is None:
            self.triggers = []

        self.triggers.append(trigger)

    class OnDamage:
        def __init__(self, filters: Filters, event: str = None, target: str = None):
            self.filters: Filters = filters
            self.event: str = event
            self.target: str = target

    class DamageSensor:
        def __init__(
            self,
            on_damage: MCDamageSensor.OnDamage = None,
            cause: str = None,
            deals_damage: bool = None,
            damage_modifier: float = None,
            damage_multiplier: float = None,
            on_damage_event_sound: str = None,
        ):
            self.on_damage: MCDamageSensor.OnDamage = on_damage
            self.cause: str = cause
            self.deals_damage: bool = deals_damage
            self.damage_modifier: float = damage_modifier
            self.damage_multiplier: float = damage_multiplier
            self.on_damage_event_sound: str = on_damage_event_sound


class MCTargetNearbySensor(Component):
    def __init__(
        self,
        inside_range: float = None,
        outside_range: float = None,
        must_see: bool = None,
        on_inside_range: TriggerEvent = None,
        on_outside_range: TriggerEvent = None,
        on_vision_lost_inside_range: TriggerEvent = None,
    ):
        super().__init__("minecraft:target_nearby_sensor")
        self.inside_range: float = inside_range
        self.outside_range: float = outside_range
        self.must_see: bool = must_see
        self.on_inside_range: TriggerEvent = on_inside_range
        self.on_outside_range: TriggerEvent = on_outside_range
        self.on_vision_lost_inside_range: TriggerEvent = on_vision_lost_inside_range


class MCOnTargetEscape(Component):
    def __init__(
        self,
        event: str = None,
        target: str = None,
        filters: Filters = None,
    ):
        super().__init__("minecraft:on_target_escape")
        self.event: str = event
        self.target: str = target
        self.filters: Filters = filters

    def addFilter(self, filter: Filters):
        self.filters = filter


class MCDespawn(Component):
    def __init__(
        self,
        despawn_from_distance: dict = None,
        despawn_from_chance: bool = None,
        despawn_from_inactivity: bool = None,
        despawn_from_simulation_edge: bool = None,
        min_range_inactivity_timer: float = None,
        min_range_random_chance: int = None,
        remove_child_entities: bool = None,
        filters: Filters = None,
    ):
        super().__init__("minecraft:despawn")
        self.despawn_from_distance: dict = despawn_from_distance
        self.despawn_from_chance: bool = despawn_from_chance
        self.despawn_from_inactivity: bool = despawn_from_inactivity
        self.despawn_from_simulation_edge: bool = despawn_from_simulation_edge
        self.min_range_inactivity_timer: float = min_range_inactivity_timer
        self.min_range_random_chance: int = min_range_random_chance
        self.remove_child_entities: bool = remove_child_entities
        self.filters: Filters = filters


class MCPushable(Component):
    def __init__(self, is_pushable: bool = None, is_pushable_by_piston: bool = None):
        super().__init__("minecraft:pushable")
        self.is_pushable: bool = is_pushable
        self.is_pushable_by_piston: bool = is_pushable_by_piston


class MCConditionalBandwidthOptimization(Component):
    def __init__(self):
        super().__init__("minecraft:conditional_bandwidth_optimization")


class MCIsCharged(Component):
    def __init__(self):
        super().__init__("minecraft:is_charged")


class MCIsIllagerCaptain(Component):
    def __init__(self):
        super().__init__("minecraft:is_illager_captain")


class MCIsShaking(Component):
    def __init__(self):
        super().__init__("minecraft:is_shaking")


class MCIsSheared(Component):
    def __init__(self):
        super().__init__("minecraft:is_sheared")


class MCInstantDespawn(Component):
    def __init__(self, remove_child_entities: bool = None):
        super().__init__("minecraft:instant_despawn")
        self.remove_child_entities: bool = remove_child_entities


class MCCanFly(Component):
    def __init__(self):
        super().__init__("minecraft:can_fly")


class MCVibrationListener(Component):
    def __init__(self):
        super().__init__("minecraft:vibration_listener")


class MCGameEventMovementTracking(Component):
    def __init__(
        self, emit_flap: bool = None, emit_move: bool = None, emit_swim: bool = None
    ):
        super().__init__("minecraft:game_event_movement_tracking")
        self.emit_flap: bool = emit_flap
        self.emit_move: bool = emit_move
        self.emit_swim: bool = emit_swim


class MCScale(Component):
    def __init__(self, scale: float):
        super().__init__("minecraft:scale")
        self.scale: float = scale


class MCBehaviorNearestAttackableTarget(Component):
    def __init__(
        self,
        priority: int = None,
        must_see: bool = None,
        attack_interval: float = None,
        attack_interval_min: float = None,
        attack_owner: bool = None,
        must_reach: bool = None,
        persist_time: float = None,
        reselect_targets: bool = None,
        scan_interval: int = None,
        set_persistent: bool = None,
        target_invisible_multiplier: float = None,
        target_search_height: int = None,
        target_sneak_visibility_multiplier: float = None,
        within_radius: float = None,
        must_see_forget_duration: float = None,
        entity_types: list = None,
    ):
        super().__init__("minecraft:behavior.nearest_attackable_target")
        self.priority: int = priority
        self.must_see: bool = must_see
        self.attack_interval: float = attack_interval
        self.attack_interval_min: float = attack_interval_min
        self.attack_owner: bool = attack_owner
        self.must_reach: bool = must_reach
        self.persist_time: float = persist_time
        self.reselect_targets: bool = reselect_targets
        self.scan_interval: int = scan_interval
        self.set_persistent: bool = set_persistent
        self.target_invisible_multiplier: float = target_invisible_multiplier
        self.target_search_height: int = target_search_height
        self.target_sneak_visibility_multiplier: float = (
            target_sneak_visibility_multiplier
        )
        self.within_radius: float = within_radius
        self.must_see_forget_duration: float = must_see_forget_duration
        self.entity_types: list = entity_types

    def addEntityType(self, entity_type: EntityType):
        if self.entity_types is None:
            self.entity_types = []
        self.entity_types(entity_type)


class MCNavigationWalk(Component):
    def __init__(
        self,
        can_path_over_water: bool = None,
        avoid_damage_blocks: bool = None,
        avoid_portals: bool = None,
        avoid_sun: bool = None,
        avoid_water: bool = None,
        can_breach: bool = None,
        can_break_doors: bool = None,
        can_float: bool = None,
        can_jump: bool = None,
        can_open_doors: bool = None,
        can_open_iron_doors: bool = None,
        can_pass_doors: bool = None,
        can_path_from_air: bool = None,
        can_path_over_lava: bool = None,
        can_sink: bool = None,
        can_swim: bool = None,
        can_walk: bool = None,
        can_walk_in_lava: bool = None,
        is_amphibious: bool = None,
        blocks_to_avoid: list = None,
    ):
        super().__init__("minecraft:navigation.walk")
        self.can_path_over_water: bool = can_path_over_water
        self.avoid_damage_blocks: bool = avoid_damage_blocks
        self.avoid_portals: bool = avoid_portals
        self.avoid_sun: bool = avoid_sun
        self.avoid_water: bool = avoid_water
        self.can_breach: bool = can_breach
        self.can_break_doors: bool = can_break_doors
        self.can_float: bool = can_float
        self.can_jump: bool = can_jump
        self.can_open_doors: bool = can_open_doors
        self.can_open_iron_doors: bool = can_open_iron_doors
        self.can_pass_doors: bool = can_pass_doors
        self.can_path_from_air: bool = can_path_from_air
        self.can_path_over_lava: bool = can_path_over_lava
        self.can_sink: bool = can_sink
        self.can_swim: bool = can_swim
        self.can_walk: bool = can_walk
        self.can_walk_in_lava: bool = can_walk_in_lava
        self.is_amphibious: bool = is_amphibious
        self.blocks_to_avoid: list = blocks_to_avoid


class MCNavigationHover(Component):
    def __init__(
        self,
        can_path_over_water: bool = None,
        avoid_damage_blocks: bool = None,
        avoid_portals: bool = None,
        avoid_sun: bool = None,
        avoid_water: bool = None,
        can_breach: bool = None,
        can_break_doors: bool = None,
        can_jump: bool = None,
        can_open_doors: bool = None,
        can_open_iron_doors: bool = None,
        can_pass_doors: bool = None,
        can_path_from_air: bool = None,
        can_path_over_lava: bool = None,
        can_sink: bool = None,
        can_swim: bool = None,
        can_walk: bool = None,
        can_walk_in_lava: bool = None,
        is_amphibious: bool = None,
        blocks_to_avoid: list = None,
    ):
        super().__init__("minecraft:navigation.hover")
        self.can_path_over_water: bool = can_path_over_water
        self.avoid_damage_blocks: bool = avoid_damage_blocks
        self.avoid_portals: bool = avoid_portals
        self.avoid_sun: bool = avoid_sun
        self.avoid_water: bool = avoid_water
        self.can_breach: bool = can_breach
        self.can_break_doors: bool = can_break_doors
        self.can_jump: bool = can_jump
        self.can_open_doors: bool = can_open_doors
        self.can_open_iron_doors: bool = can_open_iron_doors
        self.can_pass_doors: bool = can_pass_doors
        self.can_path_from_air: bool = can_path_from_air
        self.can_path_over_lava: bool = can_path_over_lava
        self.can_sink: bool = can_sink
        self.can_swim: bool = can_swim
        self.can_walk: bool = can_walk
        self.can_walk_in_lava: bool = can_walk_in_lava
        self.is_amphibious: bool = is_amphibious
        self.blocks_to_avoid: list = blocks_to_avoid


class MCMovementBasic(Component):
    def __init__(self, max_turn: int = None):
        super().__init__("minecraft:movement.basic")
        self.max_turn: int = max_turn


class MCMovementHover(Component):
    def __init__(self, max_turn: int = None):
        super().__init__("minecraft:movement.hover")
        self.max_turn: int = max_turn


class MCJumpStatic(Component):
    def __init__(self, jump_power: float = None):
        super().__init__("minecraft:jump.static")
        self.jump_power: float = jump_power


class MCCanClimb(Component):
    def __init__(self):
        super().__init__("minecraft:can_climb")


class MCHurtOnCondition(Component):
    def __init__(self, damage_conditions: list = []):
        super().__init__("minecraft:hurt_on_condition")
        self.damage_conditions: list = damage_conditions

    def addDamageCondition(self, condition: HurtCondition):
        self.damage_conditions.append(condition)

    class HurtCondition:
        def __init__(
            self,
            filters: Filters = None,
            cause: str = None,
            damage_per_tick: int = None,
        ):
            self.filters: Filters = filters
            self.cause: str = cause
            self.damage_per_tick: int = damage_per_tick

        def addFilter(self, filter: Filters):
            self.filters = filter


class MCBehaviorFloat(Component):
    def __init__(self, priority: int):
        super().__init__("minecraft:behavior.float")
        self.priority: float = priority


class MCBehaviorSwell(Component):
    def __init__(
        self, priority: int, start_distance: float = None, stop_distance: float = None
    ):
        super().__init__("minecraft:behavior.swell")
        self.priority: int = priority
        self.start_distance: float = start_distance
        self.stop_distance: float = stop_distance


class MCBehaviorMeleeAttack(Component):
    def __init__(
        self,
        priority: int = None,
        speed_multiplier: float = None,
        track_target: bool = None,
        reach_multiplier: float = None,
        attack_once: bool = None,
        attack_types: str = None,
        cooldown_time: int = None,
        inner_boundary_time_increase: float = None,
        max_dist: float = None,
        max_path_time: float = None,
        melee_fov: int = None,
        min_path_time: float = None,
        outer_boundary_time_increase: float = None,
        path_fail_time_increase: float = None,
        path_inner_boundary: int = None,
        path_outer_boundary: int = None,
        random_stop_interval: int = None,
        y_max_head_rotation: int = None,
        x_max_rotation: int = None,
        target_dist: float = None,
        set_persistent: bool = None,
        require_complete_path: bool = None,
        on_kill: TriggerEvent = None,
        on_attack: TriggerEventFilter = None,
    ):
        super().__init__("minecraft:behavior.melee_attack")
        self.priority: int = priority
        self.speed_multiplier: float = speed_multiplier
        self.track_target: bool = track_target
        self.reach_multiplier: float = reach_multiplier
        self.attack_once: bool = attack_once
        self.attack_types: str = attack_types
        self.cooldown_time: int = cooldown_time
        self.inner_boundary_time_increase: float = inner_boundary_time_increase
        self.max_dist: float = max_dist
        self.max_path_time: float = max_path_time
        self.melee_fov: int = melee_fov
        self.min_path_time: float = min_path_time
        self.outer_boundary_time_increase: float = outer_boundary_time_increase
        self.path_fail_time_increase: float = path_fail_time_increase
        self.path_inner_boundary: int = path_inner_boundary
        self.path_outer_boundary: int = path_outer_boundary
        self.random_stop_interval: int = random_stop_interval
        self.y_max_head_rotation: int = y_max_head_rotation
        self.x_max_rotation: int = x_max_rotation
        self.target_dist: float = target_dist
        self.set_persistent: bool = set_persistent
        self.require_complete_path: bool = require_complete_path
        self.on_kill: TriggerEvent = on_kill
        self.on_attack: TriggerEventFilter = on_attack


class MCBehaviorAvoidMobType(Component):
    def __init__(
        self,
        priority: int = None,
        avoid_mob_sound: str = None,
        avoid_target_xz: int = None,
        avoid_target_y: int = None,
        ignore_visibility: bool = None,
        max_dist: int = None,
        max_flee: int = None,
        probability_per_strength: int = None,
        remove_target: bool = None,
        sound_interval: list = None,
        sprint_distance: int = None,
        sprint_speed_multiplier: float = None,
        walk_speed_multiplier: float = None,
        on_escape_event: TriggerEvent = None,
        entity_types: list = None,
    ):
        super().__init__("minecraft:behavior.avoid_mob_type")
        self.priority: int = priority
        self.avoid_mob_sound: str = avoid_mob_sound
        self.avoid_target_xz: int = avoid_target_xz
        self.avoid_target_y: int = avoid_target_y
        self.ignore_visibility: bool = ignore_visibility
        self.max_dist: int = max_dist
        self.max_flee: int = max_flee
        self.probability_per_strength: int = probability_per_strength
        self.remove_target: bool = remove_target
        self.sound_interval: list = sound_interval
        self.sprint_distance: int = sprint_distance
        self.sprint_speed_multiplier: float = sprint_speed_multiplier
        self.walk_speed_multiplier: float = walk_speed_multiplier
        self.entity_types: list = entity_types
        self.on_escape_event: TriggerEvent = on_escape_event

    def addEntityType(self, entity_type: EntityType):
        if self.entity_types is None:
            self.entity_types = []

        self.entity_types(entity_type)


class MCBehaviorRandomStroll(Component):
    def __init__(
        self,
        priority: int = None,
        speed_multiplier: float = None,
        interval: int = None,
        xz_dist: int = None,
        y_dist: int = None,
    ):
        super().__init__("minecraft:behavior.random_stroll")
        self.priority: int = priority
        self.speed_multiplier: float = speed_multiplier
        self.interval: int = interval
        self.xz_dist: int = xz_dist
        self.y_dist: int = y_dist


class MCBehaviorRandomHover(Component):
    def __init__(
        self,
        priority: int = None,
        speed_multiplier: float = None,
        interval: int = None,
        xz_dist: int = None,
        y_dist: int = None,
        y_offset: int = None,
        hover_height: list = None,
    ):
        super().__init__("minecraft:behavior.random_hover")
        self.priority: int = priority
        self.speed_multiplier: float = speed_multiplier
        self.interval: int = interval
        self.xz_dist: int = xz_dist
        self.y_dist: int = y_dist
        self.y_offset: int = y_offset
        self.hover_height: list = hover_height


class MCBehaviorPickupItems(Component):
    def __init__(
        self,
        priority: int = None,
        max_dist: int = None,
        goal_radius: int = None,
        search_height: int = None,
        speed_multiplier: float = None,
        cooldown_after_being_attacked: int = None,
        can_pickup_any_item: bool = None,
        can_pickup_to_hand_or_equipment: bool = None,
        pickup_based_on_chance: bool = None,
        pickup_same_items_as_in_hand: bool = None,
        excluded_items: list = None,
    ):
        super().__init__("minecraft:behavior.pickup_items")
        self.priority: int = priority
        self.max_dist: int = max_dist
        self.goal_radius: int = goal_radius
        self.search_height: int = search_height
        self.speed_multiplier: float = speed_multiplier
        self.cooldown_after_being_attacked: int = cooldown_after_being_attacked
        self.can_pickup_any_item: bool = can_pickup_any_item
        self.can_pickup_to_hand_or_equipment: bool = can_pickup_to_hand_or_equipment
        self.pickup_based_on_chance: bool = pickup_based_on_chance
        self.pickup_same_items_as_in_hand: bool = pickup_same_items_as_in_hand
        self.excluded_items: list = excluded_items


class MCBehaviorPanic(Component):
    def __init__(
        self,
        priority: int = None,
        speed_multiplier: float = None,
        damage_sources: list = None,
        force: bool = None,
        ignore_mob_damage: bool = None,
        prefer_water: bool = None,
        panic_sound: str = None,
        sound_interval: str = None,
    ):
        super().__init__("minecraft:behavior.panic")
        self.priority: int = priority
        self.speed_multiplier: float = speed_multiplier
        self.damage_sources: list = damage_sources
        self.force: bool = force
        self.ignore_mob_damage: bool = ignore_mob_damage
        self.prefer_water: bool = prefer_water
        self.panic_sound: str = panic_sound
        self.sound_interval: str = sound_interval


class MCBehaviorLookAtPlayer(Component):
    def __init__(
        self,
        priority: int = None,
        target_distance: float = None,
        probability: float = None,
        look_distance: float = None,
        angle_of_view_horizontal: int = None,
        angle_of_view_vertical: int = None,
        look_time: list = None,
    ):
        super().__init__("minecraft:behavior.look_at_player")
        self.priority: int = priority
        self.look_distance: float = look_distance
        self.probability: float = probability
        self.angle_of_view_horizontal: int = angle_of_view_horizontal
        self.angle_of_view_vertical: int = angle_of_view_vertical
        self.look_time: list = look_time
        self.target_distance: int = target_distance


class MCBehaviorRandomLookAround(Component):
    def __init__(
        self,
        priority: int = None,
        look_time: list = None,
        max_angle_of_view_horizontal: int = None,
        min_angle_of_view_horizontal: int = None,
    ):
        super().__init__("minecraft:behavior.random_look_around")
        priority: int = (priority,)
        look_time: list = (look_time,)
        max_angle_of_view_horizontal: int = max_angle_of_view_horizontal
        min_angle_of_view_horizontal: int = min_angle_of_view_horizontal


class MCBehaviorHurtByTarget(Component):
    def __init__(
        self,
        priority: int = None,
        alert_same_type: bool = None,
        hurt_owner: bool = None,
        entity_types: list = None,
    ):
        super().__init__("minecraft:behavior.hurt_by_target")
        self.priority: int = priority
        self.alert_same_type: bool = alert_same_type
        self.hurt_owner: bool = hurt_owner
        self.entity_types: list = entity_types

    def addEntityType(self, entity_type: EntityType):
        if self.entity_types is None:
            self.entity_types = []

        self.entity_types(entity_type)


class MCBehaviorGoAndGiveItemsToNoteblock(Component):
    def __init__(
        self,
        priority: int = None,
        run_speed: int = None,
        listen_time: float = None,
        reach_block_distance: float = None,
        throw_force: float = None,
        vertical_throw_mul: float = None,
        throw_sound: str = None,
        on_item_throw: list = None,
    ):
        super().__init__("minecraft:behavior.go_and_give_items_to_noteblock")
        self.priority: int = priority
        self.run_speed: int = run_speed
        self.listen_time: float = listen_time
        self.reach_block_distance: float = reach_block_distance
        self.throw_force: float = throw_force
        self.vertical_throw_mul: float = vertical_throw_mul
        self.throw_sound: str = throw_sound
        self.on_item_throw: list = on_item_throw


class MCBehaviorStayNearNoteblock(Component):
    def __init__(
        self,
        priority: int = None,
        speed: int = None,
        start_distance: int = None,
        stop_distance: int = None,
        can_teleport: bool = None,
        ignore_vibration: bool = None,
    ):
        super().__init__("minecraft:behavior.stay_near_noteblock")
        self.priority: int = priority
        self.speed: int = speed
        self.start_distance: int = start_distance
        self.stop_distance: int = stop_distance
        self.can_teleport: bool = can_teleport
        self.ignore_vibration: bool = ignore_vibration
