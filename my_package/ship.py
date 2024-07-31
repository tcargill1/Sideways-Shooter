# -*- coding: utf-8 -*-
import pygame
import os
import sys
from pygame.sprite import Sprite

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Ship(Sprite):
    """A class to manage the ship."""
    
    def __init__(self, sideways_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = sideways_game.screen
        self.screen_rect = sideways_game.screen.get_rect()
        self.settings = sideways_game.settings

        # Make ship smaller
        self.scale_factor = 0.25

        image_path = resource_path('my_package/assets/images/ship2.png')
        self.image = pygame.image.load(image_path).convert_alpha()
        

        # Get new width and height from scale factor and make a smaller image
        self.new_width = int(self.image.get_width() * self.scale_factor)
        self.new_height = int(self.image.get_height() * self.scale_factor)
        self.smaller_image = pygame.transform.scale(self.image, (self.new_width, self.new_height))

        # Rotate the image to face correct direction
        self.smaller_image = pygame.transform.rotate(self.smaller_image, 270)

        # Start each new ship at the middle left of the screen
        self.rect = self.smaller_image.get_rect()
        self.rect.midleft = self.screen_rect.midleft

        # Store a float for the ship's exact horizontal position
        self.y = float(self.rect.y)

        # Moving flag: start with a ship that's not moving
        self.moving_up = False
        self.moving_down = False
        
    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.smaller_image, self.rect)

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_up and self.rect.top < self.screen_rect.bottom:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom > self.screen_rect.top:
            self.y += self.settings.ship_speed

        # Update rect object from self.x
        self.rect.y = self.y
    
    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midleft = self.screen_rect.midleft
        self.x = float(self.rect.x)