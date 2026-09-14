import random
from card import Card

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cards = []
        self.generate_board()

    def generate_board(self):
        total_cards = self.rows * self.cols
        if total_cards % 2 != 0:
            raise ValueError("El número de casillas debe ser par")
        num_pairs = total_cards // 2
        card_pairs = []
        for pair_id in range(num_pairs):
            card_pairs.append(Card(pair_id))
            card_pairs.append(Card(pair_id))

        random.shuffle(card_pairs)
        self.cards = []
        index = 0
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                row.append(card_pairs[index])
                index += 1
            self.cards.append(row)

    def get_card(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.cards[row][col]
        return None

    def all_matched(self):
        for row in self.cards:
            for card in row:
                if not card.matched:
                    return False
        return True

    def reset(self):
        self.generate_board()