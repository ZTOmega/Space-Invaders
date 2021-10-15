import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, ground, color):
        super(). __init__()
        self.image = pygame.Surface((3,9))
        self.image.fill(color)
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.groundYConstraint = ground

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.groundYConstraint:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()