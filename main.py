import sys
import argparse
import pygame
import cv2
from game.Game import Game
from camera.Camera import Camera

def main(webcam_ip, is_no_cam):
  print(webcam_ip)
  pygame.init()
  display_size = (500, 700)
  window = pygame.display.set_mode(display_size)
  game = Game(pygame, window, display_size)
  camera = None
  prediction_input = None

  if not is_no_cam:
    camera = Camera(webcam_ip)

  isStopped = False
  while not isStopped:
    if not is_no_cam:
      prediction_input = camera.update()
    game.update()
    game.input_update(prediction_input)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        isStopped = True
      
      # Testing purpose only
      if event.type == pygame.KEYDOWN:
        accepted_keys = ['a', 's', 'd', 'f']
        if event.unicode in accepted_keys:
          game.keyboard_input_update(event.unicode)

  # Clean up
  pygame.quit()
  if camera:
    camera.destroy()

# Command line parser
parser = argparse.ArgumentParser()
parser.add_argument("--webcam", dest="webcam_ip", help="IP Webcam ip")
parser.add_argument("--no_cam", dest="is_no_cam", help="Run the game without camera", default=False, action='store_true')
args = parser.parse_args()

main(args.webcam_ip, args.is_no_cam)