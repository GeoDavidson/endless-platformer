import os
import random
import sys

import pygame

pygame.init()

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Game")

font = pygame.font.Font(os.path.join("font", "chakrapetch-regular.ttf"), 48)

playerGroup = []
tileGroup = []

clock = pygame.time.Clock()


class Player():
    def __init__(self, colour, jumpPower, fallSpeed, fallMultiplier, maxFallSpeed, width, height, pos_x, pos_y):
        self.colour = colour
        self.jumpPower = jumpPower
        self.fallSpeed = fallSpeed
        self.fallMultiplier = fallMultiplier
        self.maxFallSpeed = maxFallSpeed
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        self.gravity = 0
        self.isGrounded = False

    def update(self):
        key = pygame.key.get_pressed()
        if self.gravity > 0:
            self.gravity += self.fallSpeed * self.fallMultiplier
        elif key[pygame.K_SPACE]:
            if self.isGrounded:
                self.gravity = self.jumpPower
                self.isGrounded = False
            self.gravity += self.fallSpeed
        else:
            self.gravity += self.fallSpeed * self.fallMultiplier
        self.rect.y += self.gravity

        if self.gravity > self.maxFallSpeed:
            self.gravity = self.maxFallSpeed
            

    def draw(self):
        pygame.draw.rect(window, self.colour, self.rect)


class Tile():
    def __init__(self, colour, width, height, pos_x, pos_y):
        self.colour = colour
        self.rect = pygame.Rect(pos_x, pos_y, width, height)

    def draw(self):
        pygame.draw.rect(window, self.colour, self.rect)


def player_tile_collision():
    for player in playerGroup:
        for tile in tileGroup:
            if player.rect.colliderect(tile.rect):
                top = player.rect.bottom - tile.rect.top
                left = player.rect.right - tile.rect.left
                if top <= left:
                    player.rect.bottom = tile.rect.top
                    player.isGrounded = True
                    player.gravity = 0
                else:
                    player.rect.right = tile.rect.left


def manage_tiles(speed):
    for tile in tileGroup:
        if len(tileGroup) <= 10:
            width = random.randint(50, 150)
            tilePosX = tileGroup[-1].rect.x + tileGroup[-1].rect.width + random.randint(60, 250)
            tilePosY = tileGroup[-1].rect.y + random.randint(-20, 20)
            if tilePosY > window.get_height() - 28:
                tilePosY = window.get_height() - 28
            elif tilePosY < 120:
                tilePosY = 120
            tile = Tile((140, 255, 92), width, 1000, tilePosX, tilePosY)
            tileGroup.append(tile)

        if tile.rect.right <= 0:
            tileGroup.remove(tile)

        tile.rect.x += speed


def start():
    playerGroup.clear()
    player = Player((255, 0, 0), -10, 0.3, 4, 15, 32, 64, 48, 32)
    playerGroup.append(player)

    tileGroup.clear()
    base = Tile((140, 255, 92), window.get_width(), 64, 0, window.get_height() - 160)
    tileGroup.append(base)

def checkScore(currentScore, bestScore):
    if currentScore > bestScore: 
        with open(os.path.join("score.txt"), "w") as file:
            file.write(str(currentScore))
        return currentScore
    return bestScore

start()

speed = -5

currentScore = 0
scoreText = font.render(f"{currentScore}", True, (0, 0, 0))

with open(os.path.join("score.txt"), "r") as file:
    bestScore = float(file.read())

bestText = font.render(f"{bestScore}", True, (0, 0, 0))
bestRect = bestText.get_rect()
bestRect.topright = (window.get_width() - 12, 12)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            checkScore(currentScore, bestScore)
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            checkScore(currentScore, bestScore)
            pygame.quit()
            sys.exit()

    window.fill((0, 140, 255))

    # update
    speed -= 0.005

    for player in playerGroup:
        player.update()

        # when player dies
        if player.rect.y > window.get_height():
            start()
            bestScore = checkScore(currentScore, bestScore)
            currentScore = 0
            speed = -5

    manage_tiles(speed)

    player_tile_collision()

    # draw
    for player in playerGroup:
        player.draw()

    for tile in tileGroup:
        tile.draw()

    currentScore += 1 / 60
    scoreText = font.render(f"{round(currentScore, 1)}", True, (0, 0, 0))
    window.blit(scoreText, (12, 12))

    bestText = font.render(f"{round(bestScore, 1)}", True, (0, 0, 0))
    bestRect = bestText.get_rect()
    bestRect.topright = (window.get_width() - 12, 12)
    window.blit(bestText, bestRect)

    pygame.display.update()

    clock.tick(60)
