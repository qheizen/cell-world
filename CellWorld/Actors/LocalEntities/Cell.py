import CellWorld.Constants.Constants as const
import CellWorld.Constants.InGameConst as gconst
import CellWorld.Tools.StaticLib as static
import CellWorld.Tools.Logger.loggers as lg
import CellWorld.Actors.LocalEntities.ActorClass as actor
import random
import pygame
import copy
from pygame import Vector2

_logger = lg.get_module_logger("CellType")

class Cell(actor.Actor):
    
    def __init__(self) -> None:
        super().__init__()
        self.visual_distance: float = const.TEMPLATE_FOV
        self._death_color: tuple = None
        
        self.is_movable: bool = False
        self.is_mortal: bool = False
        self._drag_factor: float = const.TEMPLATE_DRAG
        
        self.is_gravitate: bool = False
        self._mass: float = const.TEMPLATE_MASS
        self._speed_min: float = 0.0
        self._speed_max: float = const.TEMPLATE_SPEED
        self._strength: float = 0.0
        
        self.is_metabolism: bool = False
        self._metabolism: float = 0.0
        self._hunger_trigger: float = 0.0
        self._hunt_radius: float = 0.0
        self._lifetime: float = 0.0
        self._food: list = []
        
        self._spawn_cell_names: list = []
        self._spawn_start_speed: Vector2 = Vector2(0, 0)
        self._spawn_delay: float = 0.0
        self._spawn_left: int = 0
        self._spawn_directions: list = []
        self._spawn_mutation_rate: float = 0.0
        self._spawn_mutation_chance: float = 0.0
        
        self._relationship: list = []
        self._attached_offsets: list = []
        self._friendship: list = []
        
        self._actions: list = []
        
        self._hunger: float = 0.0
        self._attached_to: Cell = None
        self._hunting_at: Cell = None
        self._is_hungerred: bool = False
        
        self._friendly_cells = []
    
    def serialize_class(self, transfer_object: dict) -> None:
        credentials_link: dict = {
            "name": "_name",
            "color": "_color",
            "size": "_size",
            "visual_distance": "visual_distance",
            "draw_text_table": "_draw_text_table",
            "draw_lines": "_draw_lines",
            "death_color": "_death_color"
        }
        
        physical_link: dict = {
            "cell_mass": "_mass",
            "cell_min_speed": "_speed_min",
            "cell_max_speed": "_speed_max",
            "strength": "_strength",
            "drag_factor": "_drag_factor",
            "is_movable": "is_movable",
            "is_gravitate": "is_gravitate"
        }
        
        life_link: dict = {
            "metabolism_rate": "_metabolism",
            "hunger_border": "_hunger_trigger",
            "eat_radius": "_hunt_radius",
            "lifetime": "_lifetime",
            "is_mortal": "is_mortal",
            "is_metabolism": "is_metabolism",
            "food": "_food"
        }
        
        spawn_link: dict = {
            "spawn_cell_types": "_spawn_cell_names",
            "spawned_start_speed": "_spawn_start_speed",
            "spawn_delay": "_spawn_delay",
            "spawn_directions": "_spawn_directions",
            "max_spawn_number": "_spawn_left",
            "mutation_rate": "_spawn_mutation_rate",
            "crossover_rate": "_spawn_mutation_chance"
        }
        
        community_link: dict = {
            "attached_offsets": "_attached_offsets",
            "relationship": "_relationship",
            "friendship": "_friendship"
        }
        
        actions_link: dict = {
            "actions": "_actions"
        }
        
        options_link: dict = {
            "credentials": credentials_link,
            "physical": physical_link,
            "life": life_link,
            "spawner": spawn_link,
            "community": community_link,
            "actions": actions_link
        }
        
        for key, values_dict in transfer_object.items():
            link_dict = options_link.get(key)
            if link_dict:
                self._serialize_attr_from_dict(link_dict, values_dict)
                continue
            _logger.warning(f"Serialization - cant find tag: {key}")
        _logger.info(f"Serialization - cell was created with name: {self._name}")
        
    def init_spawn(self, global_manager, hunger = None, spawn_cords = None):
        super().init_spawn(global_manager, spawn_cords)
        self._object_state = gconst.OBJECT_STATES["alive"]
        self._hunger = hunger or float(random.randint(1, const.TEMPLATE_HUNG))
        self._last_spawn_time = 0.0
        
    def draw(self, surface):
        super().draw(surface)
        if not self._get_option("debug_draw"):
            return
        
        scale_factor = 3 
        end_point = (int(self._vec_position.x + self._vec_velocity.x * scale_factor), 
                    int(self._vec_position.y + self._vec_velocity.y * scale_factor))

        pygame.draw.line(surface, const.COLORS["red"], 
                        (int(self._vec_position.x), int(self._vec_position.y)),
                        end_point, width=2)
        
        if self._draw_lines:
            for friend in self._friendly_cells:
                if friend != self._hunting_at:
                    pygame.draw.line(surface, const.COLORS["white"], (int(self._vec_position.x), int(self._vec_position.y)), (int(friend.x), int(friend.y)))
            self._friendly_cells = []
            
            if self._hunting_at:
                pygame.draw.line(surface, const.COLORS["red"], (int(self._vec_position.x), int(self._vec_position.y)),
                                (int(self._hunting_at._vec_position.x), int(self._hunting_at._vec_position.y)))
        
        if self._draw_text_table:
            text_to_draw = f"n: {self._name} h: {self._hunger:.2f} t: {self._local_timer:.2f} s: {self._object_state}"
            static.draw_text_table(surface, text_to_draw, self._vec_position.x + const.TEXT_OFFSET, self._vec_position.y + const.TEXT_OFFSET, const.COLORS["gray"])
            
    def console_print(self):
        _logger.warning(
            f"TYPE: {self._name}, HUNG: {self._hunger:.2f}, "
            f"TIMER: {self._local_timer:.2f}, STATUS: {self._object_state},"
            f"VEL: {self._vec_velocity}, POS: {self._vec_position}"
        )
        
    def update(self, other_cells: list) -> None:
        if (self._hunting_at and self._hunting_at._object_state != gconst.OBJECT_STATES["alive"]) or not self._is_hungerred:
            self._hunting_at = None
        
        self._metabolize_tick()
        
        result_force = Vector2(0, 0)
        for other in other_cells:
            if other is self or not isinstance(other, Cell) or not self.is_movable:
                continue
            
            vec_to_other = other._vec_position - self._vec_position
            dist = vec_to_other.length()
            if dist >= self.visual_distance or dist < const.OVERLAP_DIST:
                dist = 5
            
            result_force += self._gravitation_tick(other, vec_to_other)
            result_force += self._relationship_tick(other, vec_to_other)
        
        result_force += self._attaching_tick()
        result_force += self._inscreen_tick()
        self._handle_spawning()
        self._check_death()
        self._add_movable(result_force)
        self._local_timer += 1 / self._get_fps()
    
    def _add_movable(self, res_force: Vector2):
        if not self.is_movable:
            return
        
        speed = self._vec_velocity.length()
        if self._is_hungerred:
            speed_max = self._speed_max * 1.3
        else:
            speed_max = self._speed_max
            
        if speed < speed_max:
            self.add_velocity(res_force / self._get_fps())
        
        if speed < self._speed_min:
            self.add_velocity(self._speed_min / self._get_fps())
            
        self.add_position(self._vec_velocity)
        self._vec_velocity *= self._drag_factor
        return

    def _handle_spawning(self):
        if not self._spawn_cell_names or self._spawn_left <= 0 or not self._world_manager:
            return
        if self._spawn_delay <= 0 and self._last_spawn_time == 0.0:
            self.init_spawner_ability()
            return

        if self._local_timer >= self._last_spawn_time + self._spawn_delay:
            self.init_spawner_ability()
        
    def init_spawner_ability(self):
        if self._object_state == "dead":
            return
        
        target_name = random.choice(self._spawn_cell_names)
        prototype = self.get_cell_prototype_with_name(target_name)
        if not prototype:
            _logger.critical(f"Cant find cell with name {target_name}")
            return
        
        new_cell: Cell = prototype.clone()
        new_cell.init_spawn(self._world_manager)
        new_cell.set_position(self._vec_position)
        if self._spawn_directions:
            try:
                dir_vector = Vector2(self._spawn_directions[0])
                new_cell.add_position(dir_vector)
            except Exception:
                new_cell.add_position(static.random_vector(-1, 1))
        else:
            new_cell.add_position(static.random_vector(-1, 1))
        new_cell.set_velocity(static.convert_to_vec(self._spawn_start_speed))
        
        self._spawn_to_world([new_cell])
        self._spawn_left -= 1
        self._last_spawn_time = self._local_timer
    
    def _check_death(self):
        if self.is_mortal and self._is_hungerred and self._hunger <= 0:
            self.init_death()
        
        if self.is_mortal and self._lifetime > 0 and self._local_timer >= self._lifetime:
            self.init_death()   
        
    def _inscreen_tick(self):
        margin = self._get_option("board_margin")
        strength = self._get_option("board_strength")
        window_size = self._get_option("window_size")
        
        fx = 0.0
        fy = 0.0
        
        if self._vec_position.x < margin:
            fx = strength / max(self._vec_position.x, 1)
        elif self._vec_position.x > window_size[0] - margin:
            fx = -strength / max(window_size[0] - self._vec_position.x, 1) 

        if self._vec_position.y < margin:
            fy = strength / max(self._vec_position.y, 1) 
        elif self._vec_position.y > window_size[1] - margin:
            fy = -strength / max(window_size[1] - self._vec_position.y, 1) 
        return Vector2(fx, fy)
    
    def _gravitation_tick(self, other: "Cell", vec_to_other: Vector2) -> Vector2:
        if not self.is_gravitate:
            return Vector2(0, 0)
        
        min_distance = (self._size + other._size) * 1.1
        distance = max(vec_to_other.length(), min_distance)
        
        if distance <= (self._size + other._size):
            return Vector2(0, 0)
        
        try:
            force_dir = vec_to_other.normalize()
        except ValueError:
            return Vector2(0, 0)
        
        g = self._get_option("constants").get("g", const.CONST_G)
        acceleration_magnitude = (g * other._mass) / (distance)
        
        return force_dir * acceleration_magnitude
        

    def _metabolize_tick(self):
        if self._object_state != gconst.OBJECT_STATES["alive"] or not self.is_metabolism:
            return

        self._hunger -= self._metabolism / self._get_fps()
        self._is_hungerred = (self._hunger <= self._hunger_trigger)
    
    def _attaching_tick(self):
        if not self._attached_to or self._attached_to._object_state == gconst.OBJECT_STATES["dead"]:
            return Vector2(0, 0)
        
        vec_to_other = self._attached_to._vec_position - self._vec_position
        force_to_return = Vector2(0, 0)
        
        dist = vec_to_other.length()
        unit = vec_to_other / dist
        if self._object_state == gconst.OBJECT_STATES["dead"] and self._attached_to:
            for offset in self._attached_offsets:
                if offset["cell_type_name"] == self._attached_to._name:
                    attached_offset = offset.get("offset", 2)
                    if dist > attached_offset:
                        force_to_return += unit * self._strength
                    elif dist < attached_offset:
                        force_to_return -= unit * self._strength

        return force_to_return
            
    
    def _relationship_tick(self, other: "Cell", vec_to_other: Vector2) -> Vector2:
        if self._object_state != gconst.OBJECT_STATES["alive"] or other._object_state != gconst.OBJECT_STATES["alive"]:
            return Vector2(0, 0)
        
        force_to_return = Vector2(0, 0)
        
        dist = max(vec_to_other.length(), const.OVERLAP_SAFE_DIST)
        for friendly_type in self._friendship:
            if other._name == friendly_type["cell_type_name"]:
                if dist < friendly_type["friend_distance"] and friendly_type["is_line_need"]:
                    self._friendly_cells.append(other._vec_position)
        
        unit = vec_to_other / dist
        
        for relate_type in self._relationship:
            if other._name == relate_type["cell_type_name"]:
                if self._is_hungerred == False:
                    force_to_return += unit * self._strength * relate_type["relation"] / dist
                else:
                    force_to_return += unit * self._strength * abs(relate_type["relation"]) 
                
                target_distance = "hunger_distance" if self._is_hungerred else "preferred_distance"
                if other == self._hunting_at and self._is_hungerred:
                    continue
                
                if dist > relate_type[target_distance]:
                    force_to_return += unit * self._strength / dist
                elif dist < relate_type[target_distance]:
                    force_to_return -= unit * self._strength
                    
        if self._hunting_at and self._hunting_at._object_state == gconst.OBJECT_STATES["alive"]:
            force_to_return += unit * self._strength
        else:
            self._hunting_at = None
            
        for food_type in self._food:
            if other._name == food_type["cell_type_name"]:
                if not self._hunting_at or dist <= (self._vec_position - self._hunting_at._vec_position).length():
                    self._hunting_at = other
                
                if dist <= self._hunt_radius and other.is_mortal:
                    other.attach_to(self)
                    self._hunger += other._hunger * food_type["stats_multiplier"]
        return force_to_return
    
    def attach_to(self, other):
        self._attached_to = other
        self.init_death()
    
    def init_death(self):
        if self.is_mortal:
            super().init_death()
            self._hunting_at = None
            self._color = self._death_color or const.COLORS["gray"]
        
    def clone(self) -> "Cell":
        new = Cell()
        
        new._name = self._name
        new._color = tuple(self._color) if self._color is not None else const.TEMPLATE_COL
        new._death_color = tuple(self._death_color) if self._color is not None else const.TEMPLATE_COL
        new._size = int(self._size)
        new.visual_distance = float(self.visual_distance)
        
        new._mass = self._get_mutated_value(self._mass)
        new._speed_min = self._speed_min
        new._speed_max = self._get_mutated_value(self._speed_max)
        new._strength = self._get_mutated_value(self._strength)
        new.is_movable = self.is_movable
        new.is_gravitate = self.is_gravitate
        new._drag_factor = self._drag_factor
        new._draw_text_table = self._draw_text_table
        new._draw_lines = self._draw_lines
        
        new._metabolism = self._get_mutated_value(self._metabolism)
        new._hunger_trigger = self._hunger_trigger
        new._hunt_radius = self._hunt_radius
        new._lifetime = self._lifetime
        new.is_mortal = self.is_mortal
        new.is_metabolism = self.is_metabolism
        
        new._food = copy.deepcopy(self._food)
        new._spawn_cell_names = self._spawn_cell_names
        new._spawn_start_speed = static.convert_to_vec(self._spawn_start_speed)
        new._spawn_delay = self._spawn_delay
        new._spawn_left = self._spawn_left
        new._spawn_directions = copy.deepcopy(self._spawn_directions)
        new._spawn_mutation_rate = self._get_mutated_value(self._spawn_mutation_rate)
        new._spawn_mutation_chance = self._get_mutated_value(self._spawn_mutation_chance)
        
        new._relationship = copy.deepcopy(self._relationship)
        new._attached_offsets = copy.deepcopy(self._attached_offsets)
        new._friendship = copy.deepcopy(self._friendship)
        new._actions = copy.deepcopy(self._actions)
        
        new._local_timer = 0.0
        new._last_spawn_time = 0.0
        new._vec_position = copy.deepcopy(self._vec_position)
        new._vec_velocity = copy.deepcopy(self._vec_velocity)
        
        return new
    
    def _get_mutated_value(self, value):
        if random.uniform(0, 1) >= self._spawn_mutation_chance:
            value *= random.uniform(1 - self._spawn_mutation_rate, 1 + self._spawn_mutation_rate)
            return value
        return value