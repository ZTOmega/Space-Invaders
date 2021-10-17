# Space Invaders by Eclizanto #

import pygame, sys
from random import choice, randint
from player import Player
from barriers import Block, shape
from aliens import Alien, Ship
from laser import Laser


class Game:
    def __init__(self):                                         # Declara Grupos de Sprites e Configurações
        # Player Setup
        playerSprite = Player((screenWidth/2,screenHeight - 70),screenWidth,5)
        self.player = pygame.sprite.GroupSingle(playerSprite)

        # Health and Score Setup
        self.lives = 3
        self.liveImage = pygame.image.load("../Space Invaders/Sprites/Laser_Canon.png").convert_alpha()
        self.liveXStartPos = self.liveImage.get_size()[0]
        self.score = 0
        self.font = pygame.font.Font("../Space Invaders/Font/ShareTechMono-Regular.ttf", 30)

        # Barrier Setup
        self.shape = shape
        self.blockSize = 3
        self.barrier = pygame.sprite.Group()
        self.barrierAmount = 4
        self.barrierXPosicion = [num * (screenWidth/self.barrierAmount - 10) for num in range(self.barrierAmount)]
        self.createMultipleBarriers(*self.barrierXPosicion, xStart=screenWidth/11.5, yStart=430)

        # Alien Setup
        self.aliens = pygame.sprite.Group()
        self.alienLasers = pygame.sprite.Group()
        self.alienArmy(lines=5, columns=10)
        self.alienDirection = choice((1,-1))

        # Ship Setup
        self.ship = pygame.sprite.GroupSingle()
        self.shipSpawnTime = randint(400,800)

        # Audios
        # Music
        music = pygame.mixer.Sound("../Space Invaders/Audio/Background_Sound.wav")
        music.set_volume(0.4)
        music.play(loops = -1)
        # Ship
        self.shipSound = pygame.mixer.Sound("../Space Invaders/Audio/Audio_Ship.mp3")
        self.shipSound.set_volume(0.2)
        # Alien Explosion
        self.AlienExplosionSound = pygame.mixer.Sound("../Space Invaders/Audio/Audio_Explosion.wav")
        self.AlienExplosionSound.set_volume(0.4)
        # Player Explosion
        self.playerExplosionSound = pygame.mixer.Sound("../Space Invaders/Audio/Player_Explosion.mp3")
        self.playerExplosionSound.set_volume(0.1)


    def createBarrier(self, xStart, yStart, offsetX):
        for lineIndex, line in enumerate(self.shape):
            for columnIndex, column, in enumerate(line):
                if column == "x":
                    x = xStart + columnIndex * self.blockSize + offsetX
                    y = yStart + lineIndex * self.blockSize
                    block = Block(self.blockSize, (40,175,140), x, y)
                    self.barrier.add(block)

    def createMultipleBarriers(self, *offset, xStart, yStart):
        for offsetX in offset:
            self.createBarrier(xStart, yStart, offsetX)

    def alienArmy(self, lines, columns, xDistance=42,yDistance=44, xOffset=60,yOffset=100):
        for lineIndex, line in enumerate(range(lines)):
            for columnIndex, column in enumerate(range(columns)):
                x = columnIndex * xDistance + xOffset
                y = lineIndex * yDistance + yOffset
                if lineIndex == 0: alienSprite = Alien("Alien_Orange", x,y)
                elif 1 <= lineIndex <= 2: alienSprite = Alien("Alien_Yellow", x,y)
                else: alienSprite = Alien("Alien_White", x,y)
                self.aliens.add(alienSprite)

    def alienPocisionChecker(self):
        allAliens = self.aliens.sprites()
        for alien in allAliens:
            if alien.rect.right >= screenWidth:
                self.alienDirection = -1
                self.alienMoveDown(8)
            elif alien.rect.left <= 0:
                self.alienDirection = 1
                self.alienMoveDown(8)

    def alienMoveDown(self, distance):
       if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alienShoot(self):
        if self.aliens.sprites():
            randomAlien = choice(self.aliens.sprites())
            laserSprite = Laser(randomAlien.rect.center, 6, screenHeight - 30, (255,100,100))
            self.alienLasers.add(laserSprite)

    def shipTimer(self):
        self.shipSpawnTime -= 1
        if self.shipSpawnTime <= 0:
            self.ship.add(Ship(choice(["right", "left"]),screenWidth))
            self.shipSpawnTime = randint(400,800)
            self.shipSound.play()

    def collisionChecks(self):
        # Player Laser
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # Barrier Collision
                if pygame.sprite.spritecollide(laser, self.barrier, True):
                    laser.kill()

                # Alien Collision
                aliensHit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliensHit:
                    for alien in aliensHit:
                        self.score += alien.value
                    laser.kill()
                    self.alienExplosionSound.play()

                # Ship Collision
                if pygame.sprite.spritecollide(laser, self.ship, True):
                    self.score += 50
                    laser.kill()
                    self.alienExplosionSound.play()
                    self.shipSound.stop()


        # Alien Lasers
        if self.alienLasers:
            for laser in self.alienLasers:
                # Barrier Collision
                if pygame.sprite.spritecollide(laser, self.barrier, True):
                    laser.kill()

                # Player Collision
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    self.playerExplosionSound.play()
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        # Aliens
        if self.aliens:
            for alien in self.aliens:
                # Barrier Collision
                pygame.sprite.spritecollide(alien, self.barrier, True)

                # Player Collision
                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()

                if alien.rect.y >= screenHeight - 100:
                    pygame.quit()
                    sys.exit()

    def displayLives(self):
        for live in range(self.lives - 1):
            x = self.liveXStartPos + (live * (self.liveImage.get_size()[0] + 10))
            screen.blit(self.liveImage, (x,screenHeight - 25))

    def displayScore(self):
        scoreSurf = self.font.render(f"SCORE: {self.score}", False, "white")
        scoreRect = scoreSurf.get_rect(topleft = (screenWidth - 200, screenHeight - 30))
        screen.blit(scoreSurf,scoreRect)

    def victoryMessage(self):
        if not self.aliens.sprites():
            victorySurf = self.font.render("YOU WIN!", False, "Yellow")
            victoryRect = victorySurf.get_rect(center = (screenWidth/2, screenHeight/3))
            screen.blit(victorySurf,victoryRect)


    def run(self):                                              # Atualiza e Desenha Grupos de Sprites
        self.player.update()
        self.alienLasers.update()
        self.ship.update()

        self.aliens.update(self.alienDirection)
        self.alienPocisionChecker()
        self.shipTimer()
        self.collisionChecks()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.barrier.draw(screen)
        self.aliens.draw(screen)
        self.alienLasers.draw(screen)
        self.ship.draw(screen)
        self.displayLives()
        self.displayScore()
        self.victoryMessage()

class CRT:
    def __init__(self):
        self.tv = pygame.image.load("../Space Invaders/Sprites/CRT_Vignette_Filter.png").convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (screenWidth, screenHeight))

    def createCrtLines(self):
        lineHight = 3
        lineAmount = int(screenHeight / lineHight)
        for line in range(lineAmount):
            yPos = line * lineHight
            pygame.draw.line(self.tv, "black", (0,yPos),(screenWidth,yPos),1)


    def draw(self):
        self.tv.set_alpha(randint(95,120))
        self.createCrtLines()
        screen.blit(self.tv,(0,0))

if __name__ == "__main__":
    pygame.init()
    screenWidth = 500
    screenHeight = 600
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("SPACE INVADERS by Eclizanto")
    ground = pygame.Rect(0, screenHeight - 30, screenWidth, 2)
    clock = pygame.time.Clock()
    game = Game()
    crt = CRT()

    alienShootLaser = pygame.USEREVENT +1
    pygame.time.set_timer(alienShootLaser, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == alienShootLaser:
                game.alienShoot()

        screen.fill((5,5,5))
        pygame.draw.rect(screen, (34,204,0), ground)
        game.run()
        crt.draw()

        pygame.display.flip()
        clock.tick(60)