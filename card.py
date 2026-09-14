import pygame
from constants import CARD_WIDTH, CARD_HEIGHT, WHITE, BLACK, GRAY, LIGHT_BLUE

class Card:
    def __init__(self, pair_id, image=None):
        self.pair_id = pair_id
        self.face_up = False
        self.matched = False
        self.image = image
        self.rect = None

    def draw(self, surface, x, y):
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        self.rect = rect

        if self.matched:
            pygame.draw.rect(surface, GRAY, rect)
            pygame.draw.rect(surface, BLACK, rect, 2)
            return

        if self.face_up:
            if self.image:
                surface.blit(self.image, (x, y))
            else:
                color = ( (self.pair_id * 50) % 256, (self.pair_id * 80) % 256, (self.pair_id * 120) % 256 )
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, BLACK, rect, 2)
                font = pygame.font.Font(None, 30)
                text = font.render(str(self.pair_id), True, BLACK)
                surface.blit(text, (x + CARD_WIDTH//2 - 10, y + CARD_HEIGHT//2 - 10))
        else:
            pygame.draw.rect(surface, LIGHT_BLUE, rect)
            pygame.draw.rect(surface, BLACK, rect, 2)

    def flip(self):
        self.face_up = not self.face_up

    def set_matched(self):
        self.matched = True
        self.face_up = False