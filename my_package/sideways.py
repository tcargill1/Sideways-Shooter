# -*- coding: utf-8 -*-
import sys
import pygame
import json
from pathlib import Path
from time import sleep
import os

from .settings import Settings
from .ship import Ship
from .bullets import Bullets
from .alien import Alien
from .game_stats import GameStats
from .button import Button
from .easy_button import Easy_Button
from .med_button import Med_Button
from .hard_button import Hard_Button
from .scoreboard import Scoreboard
from .background import Background
from .sound import Sound
import logging

class Sideways:
    """Class to manage sideways shooter game"""

    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()

        # Initialize settings of the game.
        self.settings()

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        # Initalize ships, bullets, and aliens onto the game.
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Create a fleet of aliens.
        self._create_fleet()

        # Create an instance to store game statistics and create a scoreboard.
        self.sb = Scoreboard(self)

        # Make the Play button.
        self.play_button = Button(self, "Play")

        # Make the Easy button.
        self.easy_button = Easy_Button(self, "Easy")

        # Make the Medium button.
        self.med_button = Med_Button(self, "Medium")

        # Make the Hard button.
        self.hard_button = Hard_Button(self, "Hard")

        # Start off with easy settings if they don't choose a button.
        self.settings.initalize_easy_settings()

        # Make sounds for aliens and game.
        self.sound = Sound(self)

        # Create a background image for the game.
        self.background = Background(self)

        # Start Alien Invasion in an active state.
        self.game_active = False
    
    def settings(self):
        """Function to define settings of the game."""
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Sideways Shooter")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.sound.background_music.play()

            if self.game_active:
                self.ship.update()
                self._update_aliens()
                self._update_bullets()

            self._upgrade_screen()
            self.clock.tick(60)
    
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._close_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_buttons(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            self._close_game()
    
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
    
    def check_buttons(self, mouse):
        """Function to check if any buttons have been pressed."""
        self._check_play_button(mouse)
        self._check_easy_button(mouse)
        self._check_med_button(mouse)
        self._check_hard_button(mouse)
    
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
                    self._start_game()
    
    def _check_easy_button(self,mouse_pos):
        """Start an easy game when the player clicks Easy Mode."""
        easy_click = self.easy_button.rect.collidepoint(mouse_pos)
        if easy_click:
            self.settings.initalize_easy_settings()
    
    def _check_med_button(self, mouse_pos):
        """Start a medium game when the player clicks Medium Mode."""
        med_click = self.med_button.rect.collidepoint(mouse_pos)
        if med_click:
            self.settings.initialize_medium_settings()
    
    def _check_hard_button(self, mouse_pos):
        """Start a hard game when the player clicks Hard Mode."""
        hard_click = self.hard_button.rect.collidepoint(mouse_pos)
        if hard_click:
            self.settings.initialize_hard_settings()
    
    def _reset_statistics(self):
        """Reset the game statistics."""
        self.stats.reset_stats()
        self.sb.prep_images()

    def _start_game(self):
        """Function to start fresh game."""
        # Reset the game statistics.
        self._reset_statistics()
        self.game_active = True

        # Get rid of any remaining bullets and aliens.
        self.bullets.empty()
        self.aliens.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
    
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.game_active = False
    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullets(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.right >= self.settings.screen_width:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        if collisions:
            for alien, bullets in collisions.items():
                self.stats.aliens_hit += len(bullets)

            self.alien_sound()
            self._add_points(collisions)

        if not self.aliens:
            # If the aliens are dead, start a new level.
            self._start_new_level()
    
    def alien_sound(self):
        self.sound.background_music.stop()
        self.sound.alien_sound.play()
        self.sound.background_music.play()
    
    def _add_points(self, v):
        """Add points for shooting an alien."""
        for aliens in v.values():
            self.stats.score += self.settings.alien_points * len(aliens)
        self.sb.prep_score()
        self.sb.check_high_score()
    
    def _start_new_level(self):
            """Start a new level in the game."""
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()
    
    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""
        new_alien = Alien(self)
        new_alien.y = y_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _delete_row_of_aliens(self, column_index):
        """Delete all aliens in a specific row."""
        aliens_to_remove = []
    
        for alien in self.aliens.sprites():
            if alien.rect.x // alien.rect.width == column_index:
                aliens_to_remove.append(alien)
    
        for alien in aliens_to_remove:
            self.aliens.remove(alien)
    
    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_height = alien.rect.height
        alien_width = alien.rect.width

        # Calculate starting positions
        current_y, current_x = alien_height, alien_width
        while current_x < (self.settings.screen_width - 3 * alien_width):
            while current_y < (self.settings.screen_height - 2 * alien_height):
                self._create_alien(current_x, current_y)
                current_y += 2 * alien_height
            
            # Finished a row, reset y value, and increment x value
            current_y = alien_height
            current_x += 2 * alien_width
        
        self.settings.fleet_direction = 1  # Start moving down
        self._delete_row_of_aliens(1)
        self._delete_row_of_aliens(3)

    
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the left of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.right <= 0:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break
    
    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _upgrade_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.background_color)
        self.screen.blit(self.background.background_image, self.background.rect)

        if self.game_active:
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

            self.ship.blitme()
            self.aliens.draw(self.screen)
            self.sb.show_score()
        else:
            self.draw_all_buttons()

        pygame.display.flip()
    
    def draw_all_buttons(self):
        """Function that draws all buttons onto the screen."""
        self.play_button.draw_button()
        self.easy_button.draw_button()
        self.med_button.draw_button()
        self.hard_button.draw_button()

    def _write_score_to_file(self):
        """Write current score to the file to save it."""
        path = Path('sideways_high_score.json')
        contents = json.dumps(self.stats.high_score)
        path.write_text(contents)
    
    def _close_game(self):
        """Save high score and exit."""
        saved_high_score = self.stats.get_saved_high_score()
        if self.stats.high_score > saved_high_score:
            self._write_score_to_file()
        
        sys.exit()

def main():
    logging.debug("Starting game...")
    try:
        sideways = Sideways()
        sideways.run_game()
    except Exception as e:
        logging.error("Error running game: %s", e)
        print("Error running game:", e)
        input("Press Enter to exit...")

if __name__ == '__main__':
    # Make a game instance, and then run the game
    main()
    """sideways = Sideways()
    sideways.run_game()"""
    