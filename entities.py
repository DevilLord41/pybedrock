from __future__ import annotations


# good for now, only components port now..
class AnimationController:
    def __init__(self, id, name, group):
        self.id = id
        self.group = group
        self.name = name
        self.states = []

    class States:
        def __init__(self, name):
            self.name = name
            self.on_entry = None
            self.animations = None
            self.transitions = None
            self.on_exit = None

    def addStates(self, state: States):
        self.states.append(state)


class RenderController:
    def __init__(self, id, name, group):
        self.id = id
        self.group = group
        self.name = name
        self.geometry = "Geometry.default"
        self.materials = {}
        self.textures = []
        self.part_visibility = {}
        self.arrays = self.Arrays
        self.color = {}
        self.ignore_lighting = False
        self.is_hurt_color = {}
        self.on_fire_color = {}
        self.overlay_color = {}

    class Arrays:
        def __init__(self):
            self.geometries = {}
            self.textures = {}
            self.materials = {}

        def addGeo(self, name, geo: list):
            self.geometries[name] = geo

        def addGeo(self, name, geo: str):
            self.geometries[name].append(geo)

        def addGeoFromEntities(self, name, entities: Entities):
            self.geometries[name] = []
            for geo in entities.geometry.keys:
                self.geometries[name].append(f"Geometry.{geo}")

        def addTextures(self, name, textures: list):
            pass

    def setColor(self, r, g, b, a):
        self.color["r"] = r
        self.color["g"] = g
        self.color["b"] = b
        self.color["a"] = a

    def setHurtColor(self, r, g, b, a):
        self.is_hurt_color["r"] = r
        self.is_hurt_color["g"] = g
        self.is_hurt_color["b"] = b
        self.is_hurt_color["a"] = a

    def setFireColor(self, r, g, b, a):
        self.on_fire_color["r"] = r
        self.on_fire_color["g"] = g
        self.on_fire_color["b"] = b
        self.on_fire_color["a"] = a

    def overlay_color(self, r, g, b, a):
        self.setOverlayColor["r"] = r
        self.setOverlayColor["g"] = g
        self.setOverlayColor["b"] = b
        self.setOverlayColor["a"] = a


class Animation:
    def __init__(self, id, name, group):
        self.id = id
        self.group = group
        self.name = name
        self.loop = None
        self.length = None
        self.timeline = None

    def addTimeline(self, time: str, cmd: list):
        if self.timeline is None:
            self.timeline = {}

        self.timeline[time] = cmd


class Properties:
    def __init__(self, name, type, client_sync, default):
        self.name = name
        self.type = type
        self.client_sync = client_sync
        self.default = default


class BoolProperties(Properties):
    def __init__(self, name, client_sync=None, default=None):
        super().__init__(name, "bool", client_sync, default)


class FloatProperties(Properties):
    def __init__(self, name, client_sync=None, default=None, range=None):
        super().__init__(name, "float", client_sync, default)
        self.range = range


class IntProperties(Properties):
    def __init__(self, name, client_sync=None, default=None, range=None):
        super().__init__(name, "int", client_sync, default)
        self.range = range


class EnumProperties(Properties):
    def __init__(self, name, client_sync=None, default=None, values=None):
        super().__init__(name, "enum", client_sync, default)
        self.values = values


class Entities:
    def __init__(self, id, summonable, spawnable, name=""):
        self.format_version = "1.20.0"
        self.id = id
        self.name = name
        self.summonable = summonable
        self.spawnable = spawnable
        self.runtime_identifier = None

        # RP
        self.rp_ac = []
        self.materials = {}
        self.spawn_egg = None
        self.textures = {}
        self.geometry = {}
        self.animations = {}
        self.scale = None
        self.initialize = None
        self.pre_animation = None
        self.animate = None
        self.render_controllers = []
        self.enable_attachables = False

        # BP
        self.bp_anim = []
        self.bp_ac = []
        self.bp_animations = None
        self.bp_animate = None
        self.component_groups = []
        self.components = []
        self.events = []
        self.properties = []

    def addTexture(self, name, path):
        self.textures[name] = path

    def addGeo(self, name, id):
        self.geometry[name] = id

    def addMaterial(self, name, mat):
        self.materials[name] = mat

    def addInitializeVariable(self, name, value):
        if self.initialize is None:
            self.initialize = []
        self.initialize.append(f"v.{name} = {value}")

    def addPreAnimVariable(self, name, value):
        if self.pre_animation is None:
            self.pre_animation = []
        self.pre_animation.append(f"v.{name} = {value}")

    def addRenderController(self, rctrl: str | RenderController, condition=None):
        prefix = "controller.render."
        if isinstance(rctrl, (RenderController, str)):
            rctrl_id = rctrl.id if isinstance(rctrl, RenderController) else rctrl
            render_ctrl_ref = (
                f"{prefix}{rctrl_id}"
                if condition is None
                else {f"{prefix}{rctrl_id}": condition}
            )
            self.render_controllers.append(render_ctrl_ref)
        else:
            print("Invalid render controller type.")

    def addAnimate(self, name, condition=None):
        if self.animate is None:
            self.animate = []
        if condition is None:
            self.animate.append(name)
        else:
            self.animate.append({name: condition})

    def animateBP(self, anim: Animation, condition=None):
        if condition == None:
            self.bp_animate.append(anim.name)
        else:
            self.animate.append({anim.name: condition})

        self.bp_anim.append(anim)

    def addAnimation(self, anim: str | AnimationController, id=None):
        if isinstance(anim, AnimationController):
            self.animations[anim.id] = f"animation.{anim.name}"
            self.rp_ac.append(anim)
        else:
            self.animations[id] = anim

    def addBPAnimation(self, anim: AnimationController | Animation):
        self.bp_animations[anim.id] = f"animation.{anim.name}"
        if isinstance(anim, AnimationController):
            self.bp_ac.append(anim)
        elif isinstance(anim, Animation):
            self.bp_anim.append(anim)

    def addComponentGroup(self, componentGroup: ComponentGroup):
        self.component_groups.append(componentGroup)

    def addComponent(self, component: Component):
        self.components.append(component)

    def addEvent(self, event: Event):
        self.events.append(event)

    def addProperties(self, properties: Properties):
        self.properties.append(properties)


class Component:
    def __init__(self, name: str = None):
        self.name = name


class ComponentGroup:
    def __init__(self, name):
        self.name = name
        self.components = []

    def addComponent(self, component: Component | list):
        if isinstance(component, list):
            self.components.extend(component)
        elif isinstance(component, Component):
            self.components.append(component)


class Event:
    def __init__(
        self,
        name,
        add: list = None,
        remove: list = None,
        trigger: str = None,
    ):
        self.name = name
        self.add: list = add
        self.remove: list = remove
        self.trigger: str = trigger
        self.randomize = None
        self.sequence = None
        self.set_property = None

    class Sequence:
        def __init__(
            self,
            filters: Filters,
            add: list = None,
            remove: list = None,
            trigger: str = None,
        ):
            if filters is not None:
                self.filters: Filters = filters
            if add is not None:
                self.add: dict = {"component_groups": add}
            if remove is not None:
                self.remove: dict = {"component_groups": remove}
            if trigger is not None:
                self.trigger: str = trigger

    class Randomize:
        def __init__(
            self,
            weight: float,
            add: list = None,
            remove: list = None,
            trigger: str = None,
        ):
            self.weight: float = weight
            self.add: dict = {"component_groups": add}
            self.remove: dict = {"component_groups": remove}
            self.trigger: str = trigger


class Filters:
    class Test:
        def __init__(
            self,
            test: str = "",
            subject: str = None,
            operator: str = None,
            domain: str = None,
            value=None,
        ):
            self.test = test
            self.subject = subject
            self.operator = operator
            self.domain = domain
            self.value = value

    class AllOf:
        def __init__(self, test: list = None):
            self.all_of: list = test

    class AnyOf:
        def __init__(self, test: list = None):
            self.any_of: list = test

    class NoneOf:
        def __init__(self, test: list = None):
            self.none_of: list = test
