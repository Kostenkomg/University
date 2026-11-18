
# Магический Лямбдинг!

import random

class Card(object):
    cardtype = '_'

    def __init__(self, name, attack, defense):
        """
        Создаёт карту с именем, силой атаки и силой защиты.
        >>> card_1 = Card('Гарри', 400, 300)
        >>> card_1.name
        'Гарри'
        >>> card_1.attack
        400
        >>> card_1.defense
        300
        >>> card_2 = Card('Гермиона', 300, 500)
        >>> card_2.attack
        300
        >>> card_2.defense
        500
        """
        self.name = name
        self.attack = attack
        self.defense = defense

    def power(self, other_card):
        """
        Мощь вычисляется так:
        (сила атаки карты игрока) - (сила защиты карты противника)/2
        >>> card_1 = Card('Гарри', 400, 300)
        >>> card_2 = Card('Гермиона', 300, 500)
        >>> card_1.power(card_2)
        150.0
        >>> card_2.power(card_1)
        150.0
        >>> card_3 = Card('Рон', 200, 400)
        >>> card_1.power(card_3)
        200.0
        >>> card_3.power(card_1)
        50.0
        """
        return self.attack - other_card.defense / 2


    def effect(self, other_card, player, opponent):
        """
        У простых карт нет особых действий.
        """
        return

    def __repr__(self):
        """
        Возвращает строку с читаемой информацией о карте в виде:
        <имя_карты>: <тип_карты>, [<атака>, <защита>]
        """
        return '{} {} [{}, {}]'.format(self.name, self.cardtype, self.attack, self.defense)

    def copy(self):
        """
        Возвращает копию карты.
        """
        return Card(self.name, self.attack, self.defense)

class Player(object):
    def __init__(self, deck, name):
        """Создаёт игрока.
        Игрок начинает партию забирая 5 карт из своей колоды (deck). Каждый ход игрок
        забирает одну карту из колоды и одну играет с руки (hand).
        >>> test_card = Card('тест', 100, 100)
        >>> test_deck = Deck([test_card.copy() for _ in range(6)])
        >>> test_player = Player(test_deck, 'тестер')
        >>> len(test_deck.cards)
        1
        >>> len(test_player.hand)
        5
        """
        self.deck = deck
        self.name = name
        self.hand = [self.deck.draw() for _ in range(5)]

    def draw(self):
        """Забирает карту из колоды в руку игрока.
        >>> test_card = Card('тест', 100, 100)
        >>> test_deck = Deck([test_card.copy() for _ in range(6)])
        >>> test_player = Player(test_deck, 'тестер')
        >>> test_player.draw()
        >>> len(test_deck.cards)
        0
        >>> len(test_player.hand)
        6
        """
        assert not self.deck.is_empty(), 'Колода кончилась!'
        self.hand.append(self.deck.draw())

    def play(self, card_index):
        """Играет карту с руки с заданным индексом — убирает из руки и возвращает.
        >>> from cards import *
        >>> test_player = Player(standard_deck, 'tester')
        >>> girl1, girl2 = GirlCard("girl_1", 300, 400), GirlCard("girl_2", 500, 600)
        >>> boy1, boy2 = BoyCard("boy_1", 200, 500), BoyCard("boy_2", 600, 400)
        >>> test_player.hand = [girl1, girl2, boy1, boy2]
        >>> test_player.play(0) is girl1
        True
        >>> test_player.play(2) is boy2
        True
        >>> len(test_player.hand)
        2
        """
        return self.hand.pop(card_index)

    def display_hand(self):
        """
        Отображает карты в руке игрока.
        """
        print('В руке:')
        for card_index, displayed_card in zip(range(len(self.hand)),[str(card) for card in self.hand]):
            indent = ' '*(5 - len(str(card_index)))
            print(card_index, indent + displayed_card)

    def play_random(self):
        """
        Играет случайную карту с руки.
        """
        return self.play(random.randrange(len(self.hand)))

##########################
# Дополнительные вопросы #
##########################

class BoyCard(Card):
    cardtype = '♂'

    def effect(self, other_card, player, opponent):
        """
        Сбрасывает первые три карты из руки противника и меняет их на новые карты из колоды.
        >>> from cards import *
        >>> player1, player2 = Player(player_deck, 'p1'), Player(opponent_deck, 'p2')
        >>> other_card = Card('other', 500, 500)
        >>> boy_test = BoyCard('boy', 500, 500)
        >>> initial_deck_length = len(player2.deck.cards)
        >>> boy_test.effect(other_card, player1, player2)
        p2 сбрасывает с руки 3 карты и меняет их на новые!
        >>> len(player2.hand)
        5
        >>> len(player2.deck.cards) == initial_deck_length - 3
        True
        """
        for _ in range(3):
            opponent.play(0)
            opponent.draw()
        print('{} сбрасывает с руки 3 карты и меняет их на новые!'.format(opponent.name))

    def copy(self):
        """
        Создаёт копию карты.
        """
        return BoyCard(self.name, self.attack, self.defense)

class GirlCard(Card):
    cardtype = '♀'

    def effect(self, other_card, player, opponent):
        """
        Меняет атаку и защиту карты противника.
        >>> from cards import *
        >>> player1, player2 = Player(player_deck, 'p1'), Player(opponent_deck, 'p2')
        >>> other_card = Card('other', 300, 600)
        >>> girl_test = GirlCard('girl', 500, 500)
        >>> girl_test.effect(other_card, player1, player2)
        >>> other_card.attack
        600
        >>> other_card.defense
        300
        """
        other_card.attack, other_card.defense = other_card.defense, other_card.attack

    def copy(self):
        """
        Создаёт копию карты.
        """
        return GirlCard(self.name, self.attack, self.defense)

class TeacherCard(Card):
    cardtype = '✪'

    def effect(self, other_card, player, opponent):
        """
        Добавляет атаку и защиту карты противника ко всем картам игрока.
        Затем удаляет из колоды противника все карты, у которых
        защита или атака равны соответствующим значениям карты противника.

        >>> test_card = Card('card', 300, 300)
        >>> teacher_test = TeacherCard('teacher', 500, 500)
        >>> opponent_card = test_card.copy()
        >>> test_deck = Deck([test_card.copy() for _ in range(8)])
        >>> player1, player2 = Player(test_deck.copy(), 'p1'), Player(test_deck.copy(), 'p2')
        >>> teacher_test.effect(opponent_card, player1, player2)
        Игрок p2 теряет карты из колоды! Пропало карт: 3
        >>> [(card.attack, card.defense) for card in player1.deck.cards]
        [(600, 600), (600, 600), (600, 600)]
        >>> len(player2.deck.cards)
        0
        """
        orig_opponent_deck_length = len(opponent.deck.cards)
        for card in player.deck.cards:
            card.attack += other_card.attack
            card.defense += other_card.defense
        opponent.deck.cards = [
            card for card in opponent.deck.cards
            if card.attack != other_card.attack and card.defense != other_card.defense
        ]
        discarded = orig_opponent_deck_length - len(opponent.deck.cards)
        if discarded:
            print('Игрок {} теряет карты из колоды! Пропало карт: {}'.format(opponent.name, discarded))
            return

    def copy(self):
        return TeacherCard(self.name, self.attack, self.defense)


################################
# Ниже ничего трогать не нужно #
################################

class Deck(object):
    def __init__(self, cards):
        """
        Создаёт колоду из списка карт cards. Колода учитывает, какие карты вышли,
        а какие остались, обеспечивая вытягивание случайной карты draw.
        """
        self.cards = cards

    def draw(self):
        """
        Вытаскивает случайную карту из колоды.
        """
        assert self.cards, 'Колода пуста!'
        rand_index = random.randrange(len(self.cards))
        return self.cards.pop(rand_index)

    def is_empty(self):
        return len(self.cards) == 0

    def copy(self):
        """
        Создаёт копию колоды.
        """
        return Deck([card.copy() for card in self.cards])

class Game(object):

    win_score = 8

    def __init__(self, player1, player2):
        """
        Создаёт игру Магический Лямбдинг.
        """
        self.player1, self.player2 = player1, player2
        self.p1_score = 0
        self.p2_score = 0

    def play_round(self, p1_card, p2_card):
        """
        После того, как каждый игрок вытащил по карте, они играют друг против друга раунд.
        """
        p1_card.effect(p2_card, self.player1, self.player2)
        p2_card.effect(p1_card, self.player2, self.player1)
        p1_power = p1_card.power(p2_card)
        p2_power = p2_card.power(p1_card)
        if p1_power > p2_power:
            # Player 1 победил в раунде.
            self.p1_score += 1
            result = 'победа'
        elif p2_power > p1_power:
            # Player 2 победил в раунде.
            self.p2_score += 1
            result = 'поражение'
        else:
            # Ничья в раунде.
            result = 'ничья'
        # Отображение результатов.
        print('Результат этого раунда — {}!'.format(result))
        print('Игрок {} бросает карту «{}», её мощь: {}'.format(self.player1.name, p1_card, p1_power))
        print('Противник бросает  карту «{}» с мощью: {}'.format(p2_card, p2_power))


    def game_won(self):
        """
        Проверяет, выиграна ли игра. Если да, то определяет победителя.
        """
        if self.p1_score < self.win_score and self.p2_score < self.win_score:
            return 0
        return 1 if self.p1_score > self.p2_score else 2

    def display_scores(self):
        """
        Отображает очки игроков.
        """
        print('Игрок «{}» набрал {} очков.'.format(self.player1.name, self.p1_score))
        print('Противник набрал {} очков'.format(self.p2_score))
