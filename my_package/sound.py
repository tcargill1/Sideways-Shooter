# -*- coding: utf-8 -*-
import pygame.mixer
from my_package.ship import resource_path

class Sound:
    """A class to implement sounds into the game."""

    def __init__(self, ai_game):
        """Initialize sound attributes."""
        pygame.mixer.init()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        image_path = resource_path('my_package/assets/sounds/alien_sound.mp3')
        self.alien_sound = pygame.mixer.Sound(image_path)
        self.alien_sound.set_volume(0.5)

        image_path_2 = resource_path('my_package/assets/sounds/space.mp3')
        self.background_music = pygame.mixer.Sound(image_path_2)