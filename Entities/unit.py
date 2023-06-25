from turtle import Vec2D
from typing import Tuple, List, Any
import pygame

from pygame.surface import Surface
from pygame.rect import Rect
from Engine.entity import Entity
from Engine.image import Image
from Engine.utils import draw_collision_rect

from Engine.vector import Vector
from Engine.window import Window
from Entities.bullet import Bullet


class Unit(Entity):
    tile_position: Vector
    screen_position: Vector
    tower_img: Image  # go to resource instance
    unique_id: int
    collision_rect: Rect  # go to resource instance
    target: Entity
    unit_manager: Any  # UnitManager
    fire_range: int
    fire_range_rect: Rect
    has_entity_in_range: bool

    def __init__(
        self,
        tile_position: Vector,
        unit_manager,
        id: int = 0,
    ):
        self.unique_id = id
        self.has_entity_in_range = False
        self.tile_position = tile_position
        self.target = None
        self.fire_range = 15
        self.screen_position = Window.to_isometric_position_from_vector(tile_position)
        self.screen_position += Vector(0, -14)
        self.collision_rect = pygame.Rect(
            self.screen_position.x + 6, self.screen_position.y, 17, 27
        )
        self.unit_manager = unit_manager

        self.tower_img = Image("./res/sprites/tower.png", (255, 0, 0))
        self.center_position = Vector(
            self.screen_position.x + self.tower_img.width / 2,
            self.screen_position.y + self.tower_img.height / 2,
        )
        self.create_range()
        super().__init__(self.center_position)

    def update(self):
        pass

    def draw(self, surface: Surface, offset: Vector = Vector()):
        self.tower_img.draw(surface, self.screen_position, offset)
        # self.draw_fire_range(surface, offset)
        # draw_collision_rect(self.collision_rect, surface, offset)

    def create_range(self):
        width_range = self.fire_range * 2
        height_range = self.fire_range
        self.fire_range_rect = pygame.Rect(
            (self.center_position.x - width_range * 2 * 1.2),
            (self.center_position.y - height_range * 2),
            width_range * 5,
            height_range * 5,
        )

    def draw_fire_range(self, surface: Surface, offset: Vector = Vector()):
        color = (0, 200, 255)
        if self.has_entity_in_range:
            color = (200, 0, 0)
        shape_surf = pygame.Surface(self.fire_range_rect.size, pygame.SRCALPHA)
        pygame.draw.ellipse(shape_surf, color, shape_surf.get_rect())

        shape_surf.set_alpha(30)

        surface.blit(
            shape_surf,
            pygame.Rect(
                self.fire_range_rect.x - offset.x,
                self.fire_range_rect.y - offset.y,
                self.fire_range_rect.width,
                self.fire_range_rect.height,
            ),
        )
        pygame.draw.ellipse(
            surface,
            (210, 210, 245),
            pygame.Rect(
                self.fire_range_rect.x - offset.x,
                self.fire_range_rect.y - offset.y,
                self.fire_range_rect.width,
                self.fire_range_rect.height,
            ),
            width=1,
        )

    def is_in_range(self, entity: Entity):
        if self.fire_range_rect.colliderect(entity.collision_rect):
            self.has_entity_in_range = True
            return
        self.has_entity_in_range = False

    def set_target(self, target: Entity):
        self.target = target

    def fire(self):
        self.unit_manager.bullets.append(
            Bullet(self.center_position.copy(), self.target, 6)
        )

    def __eq__(self, compared: object) -> bool:
        if type(compared) != type(self):
            return False
        return self.tile_position == compared.tile_position

    def __str__(self) -> str:
        return f"Unit(id: {self.unique_id}, tile_position: {self.tile_position}) "
