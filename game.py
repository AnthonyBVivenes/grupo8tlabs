import pygame
import sys
from constants import *
from board import Board
from player import Player

class Game:
    def __init__(self, num_humans=1, num_ais=0):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Memory")
        self.clock = pygame.time.Clock()
        self.running = True

        self.board = Board(BOARD_ROWS, BOARD_COLS)
        self.players = []
        for i in range(num_humans):
            self.players.append(Player(f"Jugador {i+1}", is_human=True))
        for i in range(num_ais):
            self.players.append(Player(f"IA {i+1}", is_human=False))

        self.current_player_index = 0
        self.selected_cards = []
        self.waiting = False
        self.wait_timer = 0

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.waiting:
                if self.players[self.current_player_index].is_human:
                    mouse_pos = pygame.mouse.get_pos()
                    self.handle_click(mouse_pos)

    def handle_click(self, pos):
        card_width = CARD_WIDTH + CARD_MARGIN
        card_height = CARD_HEIGHT + CARD_MARGIN
        total_width = BOARD_COLS * card_width - CARD_MARGIN
        total_height = BOARD_ROWS * card_height - CARD_MARGIN
        start_x = (SCREEN_WIDTH - total_width) // 2
        start_y = (SCREEN_HEIGHT - total_height) // 2

        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                x = start_x + c * card_width
                y = start_y + r * card_height
                rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
                if rect.collidepoint(pos):
                    card = self.board.get_card(r, c)
                    if card and not card.matched and not card.face_up:
                        card.flip()
                        self.selected_cards.append((r, c))
                        if len(self.selected_cards) == 2:
                            self.waiting = True
                            self.wait_timer = pygame.time.get_ticks()
                    return

    def update(self):
        if self.waiting:
            if pygame.time.get_ticks() - self.wait_timer > 1000:
                self.check_pair()
                self.waiting = False
                self.next_turn()
        if not self.waiting and not self.players[self.current_player_index].is_human:
            self.ai_turn()
        if self.board.all_matched():
            self.end_game()

    def check_pair(self):
        if len(self.selected_cards) != 2:
            return
        (r1, c1), (r2, c2) = self.selected_cards
        card1 = self.board.get_card(r1, c1)
        card2 = self.board.get_card(r2, c2)
        if card1 and card2 and card1.pair_id == card2.pair_id:
            card1.set_matched()
            card2.set_matched()
            self.players[self.current_player_index].add_pair()
        else:
            card1.flip()
            card2.flip()
        self.selected_cards = []

    def ai_turn(self):
        available = []
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                card = self.board.get_card(r, c)
                if not card.matched and not card.face_up:
                    available.append((r, c))
        if len(available) < 2:
            return
        import random
        selected = random.sample(available, 2)
        for r, c in selected:
            card = self.board.get_card(r, c)
            card.flip()
            self.selected_cards.append((r, c))
        self.waiting = True
        self.wait_timer = pygame.time.get_ticks()

    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def render(self):
        self.screen.fill(WHITE)
        card_width = CARD_WIDTH + CARD_MARGIN
        card_height = CARD_HEIGHT + CARD_MARGIN
        total_width = BOARD_COLS * card_width - CARD_MARGIN
        total_height = BOARD_ROWS * card_height - CARD_MARGIN
        start_x = (SCREEN_WIDTH - total_width) // 2
        start_y = (SCREEN_HEIGHT - total_height) // 2

        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                x = start_x + c * card_width
                y = start_y + r * card_height
                card = self.board.get_card(r, c)
                card.draw(self.screen, x, y)

        font = pygame.font.Font(None, 30)
        for i, player in enumerate(self.players):
            color = (0, 0, 0)
            if i == self.current_player_index:
                color = (255, 0, 0) 
            text = font.render(f"{player.name}: {player.score} pares", True, color)
            self.screen.blit(text, (20, 20 + i * 30))

        pygame.display.flip()

    def end_game(self):
        winner = max(self.players, key=lambda p: p.score)
        print(f"¡{winner.name} gana con {winner.score} pares!")
        self.running = False