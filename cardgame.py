from classes import *
from cards import *

try:
    import readline
except ImportError:
    pass

###########
# Парсинг #
###########

def card_parse(line, handsize):
    tokens = line.split()
    if not tokens:
        raise SyntaxError('Команда не задана')
    elif len(tokens) > 1:
        raise SyntaxError('Слишком много команд')
    card_index = tokens.pop(0)
    if not card_index.isdigit():
        raise SyntaxError('Введено значение неверного типа')
    card_index = int(card_index)
    if card_index >= handsize or card_index < 0:
        raise SyntaxError('Неправильный номер карты')
    return card_index

def name_parse(line):
    if not line:
        raise SyntaxError('Команда не задана')
    return line

########
# REPL #
########

def read_eval_print_loop():
	while True:
		try:
			line = input('Как тебя зовут?> ')
			name = name_parse(line)
			break
		except (KeyboardInterrupt, EOFError, SystemExit): # При нажатии ctrl-c или ctrl-d
			print('\nДо встречи!')
			return
		except SyntaxError as e:
			print('ERROR:', e)
	p1 = Player(player_deck, name)
	p2 = Player(opponent_deck, 'Противник')
	print(WELCOME_MESSAGE)
	duel = Game(p1, p2)
	draw = True
	while True:
		if duel.game_won() == 1:
			print(WIN_MESSAGE)
			return
		elif duel.game_won() == 2:
			print(LOSE_MESSAGE)
			return
		print()
		try:
			if draw:
				p1.draw()
				p2.draw()
			else:
				draw = True
			p1.display_hand()
			print('Пожалуйста, введи номер карты.')
			line = input('карта> ')
			card_index = card_parse(line, len(p1.hand))
			duel.play_round(p1.play(card_index), p2.play_random())
			duel.display_scores()
		except (KeyboardInterrupt, EOFError, SystemExit): # При нажатии ctrl-c или ctrl-d
			print('\nА так хорошо играли. Пока!')
			return
		except AssertionError: # Колода кончилась
			if p1.deck.is_empty() and p2.deck.is_empty():
				print(TIE_MESSAGE)
				return
			elif p1.deck.is_empty():
				print(PLAYER_DECKOUT_MESSAGE)
				return
			else:
				print(OPPONENT_DECKOUT_MESSAGE)
				return
		except SyntaxError as e:
			print('ERROR:', e)
			draw = False

################
# Конфигурация #
################

WELCOME_MESSAGE = """
Добро пожаловать в Магический Лямбдинг!

Твой код оказался настолько прекрасен, что в нём пробудилось
сознание и он решил победить тебя в карточную игру! Если нужно
припомнить правила — посмотри соответствующий раздел в описании 
лабораторки.

Пора сразиться, не так ли?
"""

WIN_MESSAGE = """
Тебе удалось победить противника в поединке!

Поздравляю! Партия Магического Лямбдинга окончена, победа твоя.
"""

LOSE_MESSAGE = """
Противнику удалось забороть тебя!

Прости, но победа в Магическом Лямбдинге досталась противнику! 
"""

TIE_MESSAGE = """
И у тебя и у противника закончились карты в колоде.

Ничья. Кто же победит в следующей партии?
"""

PLAYER_DECKOUT_MESSAGE = """
У тебя не осталось карт в колоде!

Прости, но победа в Магическом Лямбдинге досталась противнику! 
"""

OPPONENT_DECKOUT_MESSAGE = """
У противника не осталось карт в колоде!

Поздравляю! Партия Магического Лямбдинга окончена, победа твоя.
"""

if __name__ == '__main__':
    read_eval_print_loop()