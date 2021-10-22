import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x,y):
        super().__init__()
        filePath = "../Space Invaders/Sprites/" + color + ".png"
        self.image = pygame.image.load(filePath).convert_alpha()
        self.rect = self.image.get_rect(center = (x,y))
        
        # Valor de Pontuação
        if color == "Alien_White": self.value = 10
        elif color == "Alien_Yellow": self.value = 20
        else: self.value = 30

    def update(self, direction):
        self.rect.x += direction

class Ship(pygame.sprite.Sprite):
    def __init__(self, side, screenWidth):
        super().__init__()
        self.image = pygame.image.load("../Space Invaders/Sprites/Ship_Red.png").convert_alpha()
        self.shipconstraint = screenWidth

        if side == "right":
            x = screenWidth + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft = (x,30))

    def destroy(self):
        if self.rect.x <= -100 or self.rect.x >= self.shipconstraint + 100:
            self.kill()

    def update(self):
        self.rect.x += self.speed
        self.destroy()