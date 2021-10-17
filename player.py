import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.image = pygame.image.load("../Space Invaders/Sprites/Laser_Canon.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.maxXConstraint = constraint
        self.ready = True
        self.laserTime = 0
        self.laserCoolDown = 800
        self.lasers = pygame.sprite.Group()
        # Laser Sound
        self.laserSound = pygame.mixer.Sound("../Space Invaders/Audio/Audio_Laser.wav")
        self.laserSound.set_volume(0.1)

    def getInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shootLaser()
            self.ready = False
            self.laserTime = pygame.time.get_ticks()
            self.laserSound.play()

    def recharge(self):
        if not self.ready:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.laserTime >= self.laserCoolDown:
                self.ready = True

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.maxXConstraint:
            self.rect.right = self.maxXConstraint

    def shootLaser(self):
        self.lasers.add(Laser(self.rect.center, -11, self.rect.bottom, (34,204,0)))

    def update(self):
        self.getInput()
        self.constraint()
        self.recharge()
        self.lasers.update()