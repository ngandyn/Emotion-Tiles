import random
import time

from .Tile import Tile
from .Scoreboard import Scoreboard
from .Lives import Lives
from .Colors import WHITE, BLACK


class Game():
  def __init__(self, pygame, window, display_size):
    self.pygame = pygame
    self.window = window
    self.display_size = display_size
    self.columns = 4
    self.scoreboard = Scoreboard(pygame, display_size)
    self.lives = Lives(pygame, display_size)

    self.tiles = []
    self.generate_tiles(display_size)
    self.last_update_time = time.time()
    self.game_update_speed = 5 # Frames per second

    self.is_game_over = False

  def update(self):
    current_time = time.time()
    if current_time < self.last_update_time + 1/self.game_update_speed:
      return

    self.window.fill(WHITE)
    if self.is_game_over:
      font = self.pygame.font.Font(None, 35)
      text = font.render("GAME OVER", 1, BLACK)
      self.window.blit(text, (self.display_size[0]/2.5, self.display_size[1]/2))
      self.scoreboard.render(self.window)
      self.lives.render(self.window)
      self.pygame.display.update()
      return

    for tile in self.tiles:
      tile.update(self.display_size, self.columns)
      # tile.force_reset(self.display_size, self.columns) # TODO: remove
      tile.render(self.pygame, self.window)
      is_reached_bottom = tile.is_reached_bottom(self.display_size)
      if is_reached_bottom:
        tile.relocate(self.display_size, self.columns)
        self.lives.decrease_live()
        if self.lives.get_lives() == 0:
          self.is_game_over = True

    self.scoreboard.render(self.window)
    self.lives.render(self.window)
    self.pygame.display.update()
    self.last_update_time = time.time()


  def input_update(self, prediction_input):
    if self.is_game_over:
      return

    # Cluster 3 is neutral so ignored
    # Cluster 2 requires the player to stand up and clap
    # Replace cluster 2 with 4 since many social signals fall into it
    CLUSTER_COLUMN_MAPPER = {
      0: [0],
      1: [1],
      4: [2, 3]
    }
    
    if not prediction_input in CLUSTER_COLUMN_MAPPER:
      return
    print("Cluster:", prediction_input)

    # Find tile with key == column
    selected_tile = None
    for tile in self.tiles:
      tile_column = tile.get_column()
      if not tile.is_in_screen():
        continue
      
      matching_columns = CLUSTER_COLUMN_MAPPER[prediction_input]
      if tile_column in matching_columns:
        if selected_tile != None:
          if tile.get_y() > selected_tile.get_y():
            selected_tile = tile
        else:
          selected_tile = tile
    
    # Matching found
    if selected_tile != None and selected_tile.is_in_screen():
      selected_tile.relocate(self.display_size, self.columns)
      self.scoreboard.increaseScore()


  # For testing purpose
  def keyboard_input_update(self, key):
    if self.is_game_over:
      return
    
    key_column_dict = {
      'a': 0,
      's': 1,
      'd': 2,
      'f': 3,
    }
    if key not in key_column_dict:
      return

    # Find tile with key == column
    selected_tile = None
    for tile in self.tiles:
      tile_column = tile.get_column()
      if key_column_dict[key] == tile_column:
        if selected_tile != None:
          if tile.get_y() > selected_tile.get_y():
            selected_tile = tile
        else:
          selected_tile = tile
    
    # Matching found
    if selected_tile != None and selected_tile.is_in_screen():
      selected_tile.relocate(self.display_size, self.columns)
      self.scoreboard.increaseScore()


  def generate_tiles(self, display_size):
    colors = [(33,150,243), (3,169,244), (0,188,212), (0,150,136)]

    for i in range(self.columns):
      width = display_size[0]/self.columns
      height = width * 1.5
      # column = random.randrange(self.columns)
      column = i
      x = column * width
      y = i * height - display_size[1]
      tile = Tile(self.pygame, x, y, width, height, column, color=colors[i])
      self.tiles.append(tile)