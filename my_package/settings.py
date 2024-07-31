# -*- coding: utf-8 -*-
class Settings:
    """A class to store all settings for Sideways Shooter game."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.background_color = (230, 230, 230)

        # Ship settings
        self.ship_limit = 3 

        # Bullet settings
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (0, 0, 0)
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 50

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initalize_easy_settings()
        self.initialize_medium_settings()
        self.initialize_hard_settings()
        

    def initalize_easy_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 2
        self.bullet_speed = 3
        self.alien_speed = 1.0

        # Scoring settings
        self.alien_points = 50

        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

    def initialize_medium_settings(self):
        """Initalize medium settings."""
        self.ship_speed = 2
        self.bullet_speed = 3
        self.alien_speed = 1.5

        # Scoring settings
        self.alien_points = 60

        self.fleet_direction = 1
    
    def initialize_hard_settings(self):
        """Initialize hard settings."""
        self.ship_speed = 2
        self.bullet_speed = 3
        self.alien_speed = 2

        # Scoring settings
        self.alien_points = 70

        self.fleet_direction = 1
    
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)