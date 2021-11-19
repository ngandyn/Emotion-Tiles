from .Colors import GREEN

class Scoreboard():
  def __init__(self, pygame, display_size):
    self.x = display_size[0] - 100
    self.y = 20
    self.score = 0
    self.font = pygame.font.Font(None, 24)

  def render(self, window):
    text = self.font.render(f"Score: {self.score}", 1, GREEN)
    window.blit(text, (self.x, self.y))

  def increaseScore(self):
    self.score += 1