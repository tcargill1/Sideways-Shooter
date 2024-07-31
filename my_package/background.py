# -*- coding: utf-8 -*-
import pygame
from pygame.sprite import Sprite
from my_package.ship import resource_path

class Background(Sprite):
    """A class to manage the background image of the game."""

    def __init__(self, ai_game):
        super().__init__()

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        image_path = resource_path('my_package/assets/images/background_space.png')
        self.image = pygame.image.load(image_path)
        self.background_image = pygame.transform.smoothscale(self.image, (self.settings.screen_width, self.settings.screen_height))
        self.rect = self.background_image.get_rect()
       