import os
import pygame

images = []

for filename in sorted(os.listdir("sprites")):
    if filename.endswith(".png"):
        image = pygame.image.load(
            os.path.join("sprites", filename)
        )
        images.append(image)
