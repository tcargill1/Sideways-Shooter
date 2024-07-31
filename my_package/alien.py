# -*- coding: utf-8 -*-
import pygame
from pygame.sprite import Sprite
from my_package.ship import resource_path

class Alien(Sprite):
    """Class to manage Alien assets."""
    def __init__(self, sideways):
        super().__init__()

        self.screen = sideways.screen
        self.settings = sideways.settings

        # Load the alien image and set its starting position.
        image_path = resource_path('my_package/assets/images/alien.png')
        self.image = pygame.image.load(image_path).convert_alpha()
        self.angle = 90
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.settings.screen_width - self.rect.width
        self.rect.y = 0

        # Store the alien's exact vertical position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True is alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.bottom >= screen_rect.bottom) or (self.rect.top <= 0)

    def update(self):
        """Move the alien up and down"""
        self.y += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.y = self.y