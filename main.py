from cards import *
from termcolor import colored


def draw(current_player, number, draw_set):
    cards = draw_set[:number]
    current_player.extend(cards)
    return current_player, draw_set[number:]


def your_turn(user_option, current_player, draw_set, discard_set):
    if user_option == "draw":
        current_player, draw_set = draw(current_player, 1, draw_set)
        card = current_player[-1]
        print("You drew a ", colored(card[0], card[1]), ". Would you like to play your drawn card?")
        answer = input()
        if answer == "yes":
            discard_set.append(card)
            current_player.pop()
    else:
        print("Enter colour of card")
        color = input()
        print("Enter number of card")
        number = input()
        card = [int(number), color.lower()]
        discard_set.append(card)
        current_player.remove(card)
    return current_player, draw_set, discard_set


def search_card(current_player, draw_set, discard_set):
    type_of_card = discard_set[-1][0]  # Number / Type of card
    colour = discard_set[-1][1]  # Colour of card
    for card in current_player:
        # Found a match in your cards (same colour or number)
        if card[0] == type_of_card or card[1] == colour:
            discard_set.append(card)
            current_player.remove(card)
            print("Computer played ", colored(card[0], card[1]))
            return current_player, draw_set, discard_set

    current_player, draw_set = draw(current_player, 1, draw_set)  # did not find a match -- draw 1 card
    # see if player can play that card
    if current_player[-1][1] == colour or current_player[-1][0] == type_of_card:
        discard_set.append(current_player[-1])
        current_player.pop()
        print("\nComputer played ", colored(current_player[-1][0], current_player[-1][1]))
    else:
        print("\nComputer drew a card")
    return current_player, draw_set, discard_set


def print_cards(current_player):
    for card in current_player:
        color = card[1]
        print(colored(card[0], color), end=' ')
    print('\n')


if __name__ == '__main__':
    CARD_DECK = get_initial_small_card_deck()  # Gets the whole UNO deck
    player = CARD_DECK[:7]  # distributes first seven cards to player
    computer = CARD_DECK[7:14]  # distributes next seven cards to computer
    discard_pile = [CARD_DECK[14]]  # puts the next card on discard pile
    draw_pile = CARD_DECK[15:]  # rest of the cards

    # Until someone finishes all their cards, keep playing
    while player and computer:
        print('Discard pile: ', colored(discard_pile[-1][0], discard_pile[-1][1]))
        print("_________________")
        print("your cards", end=': ')
        print_cards(player)
        print("enter 'deal' to deal an existing card and 'draw' to draw a card")
        option = input()
        player, draw_pile, discard_pile = your_turn(option, player, draw_pile, discard_pile)
        computer, draw_pile, discard_pile = search_card(computer, draw_pile, discard_pile)
        print("_________________")

    if not player:
        print("you win")
    if not computer:
        print("computer wins")
