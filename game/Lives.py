from .Colors import GREEN

class Lives():
  def __init__(self, pygame, display_size):
    self.x = 20
    self.y = 20
    self.lives = 3
    self.font = pygame.font.Font(None, 24)

  def render(self, window):
    text = self.font.render(f"Lives: {self.lives}", 1, GREEN)
    window.blit(text, (self.x, self.y))

  def get_lives(self):
    return self.lives

  def decrease_live(self):
    self.lives -= 1