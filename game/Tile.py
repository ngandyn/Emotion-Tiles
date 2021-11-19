import random
import math

from .Colors import BLACK

COLUMNS = {
  0: ["Scared", "Hands Up"],
  1: ["Shocked", "Open mouth,", "Arms down"],
  2: ["Smiling", "Peace Sign,", "Fist Pump"],
  3: ["Laughing", "2 Thumbs Up"]
}

class Tile():
  def __init__(self, pygame, x, y, width, height, column, color=BLACK):
    self.width = width
    self.height = height
    self.x = x
    self.y = y
    self.speed = 10
    self.color = color
    self.column = column
    self.font = pygame.font.Font(None, 24)

  def render(self, pygame, window):
    pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
    descriptions = COLUMNS[self.column]
    for i in range(len(descriptions)):
      desc = descriptions[i]
      text = self.font.render(desc, 1, BLACK)
      window.blit(text, (self.x + 15, self.y + self.height/3 + i*20))

  def update(self, display_size, columns):
    self.y = self.y + self.speed

  def relocate(self, display_size, columns):
    # self.column = random.randrange(columns)
    self.y = -display_size[1]/2
    self.x = self.column * self.width

  # Temporary for resetting when it reaches the bottom
  def force_reset(self, display_size, columns):
    if self.y + self.height > display_size[1]:
      # self.column = random.randrange(columns)
      self.y = -display_size[1]/2
      self.x = self.column * self.width

  def get_column(self):
    return self.column

  def get_y(self):
    return self.y

  def is_in_screen(self):
    return self.y > 0

  def is_reached_bottom(self, display_size):
    return self.y + self.height >= display_size[1]