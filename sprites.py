import os
import pygame

images = []

def init_sprites():
    """Initialize sprites."""
    # import all sprites alphabetically
    for filename in sorted(os.listdir("sprites")):
        if filename.endswith(".png"):
            image = pygame.image.load(
                os.path.join("sprites", filename)
            )
            images.append(image)
