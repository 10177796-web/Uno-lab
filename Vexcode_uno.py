#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()
motor_1 = Motor(Ports.PORT1, False)
motor_5 = Motor(Ports.PORT5, True)


# Wait for sensor(s) to fully initialize
wait(100, MSEC)

# generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 

# Initialize random seed 
initializeRandomSeed()

#endregion VEXcode Generated Robot Configuration
# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode EXP Python Project
# 
# ------------------------------------------

# Library imports
from vex import *

# Begin project code

# Create events
FWD = Event()
RT = Event ()
LT = Event () 

# Function 
def when_started():
    FWD.broadcast_and_wait()
    LT.broadcast_and_wait()
    FWD.broadcast_and_wait()
    RT.broadcast_and_wait()
    FWD.broadcast_and_wait()

def motor1_move_forward():
    motor_1.spin_for(FORWARD, 425, DEGREES)
def motor5_move_forward():
    motor_5.spin_for(FORWARD, 425, DEGREES)
def motor1_turn_right():
    motor_1.spin_for(FORWARD, 220, DEGREES)
def motor5_turn_right():
    motor_5.spin_for(REVERSE, 220, DEGREES)
def motor_1_turn_left():
    motor_1.spin_for(REVERSE, 220, DEGREES)
def motor5_turn_left():
    motor_5.spin_for(FORWARD, 220, DEGREES)

# Register the callback functions to the events 
FWD(motor1_move_forward)
FWD(motor5_move_forward)
RT(motor1_turn_right)
RT(motor5_turn_right)
LT(motor_1_turn_left)
LT(motor5_turn_left)
wait(15, MSEC)

# Start the program!
from vex import *
import random

# Initialize the VEX EXP Brain
brain = Brain()

def move_forward():
    """Stub for moving forward by 2 units."""
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Driving Forward...")
    wait(1000, MSEC)

def turn_right():
    """Stub for turning right 90 degrees."""
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Turning Right 90deg")
    wait(500, MSEC)

def turn_left():
    """Stub for turning left 90 degrees."""
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Turning Left 90deg")
    wait(500, MSEC)

def robot_trip_action(action_name):
    """
    Simulates robot trip to the center, performing a card action, 
    and driving back to the player.
    """
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Robot Moving...")
    
    # 1. Drive to center (2 forward movements)
    move_forward()
    move_forward()
    
    # 2. Perform action at center
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Action: {action_name}")
    wait(1000, MSEC)
    
    # 3. Turn around (180 degrees via two 90-degree turns)
    turn_right()
    turn_right()
    
    # 4. Drive back to player (2 forward movements)
    move_forward()
    move_forward()
    
    # 5. Turn back to starting orientation
    turn_right()
    turn_right()

def create_uno_deck():
    """Generates a standard 108-card UNO deck using dictionaries."""
    colors = ['Red', 'Yellow', 'Green', 'Blue']
    deck = []
    
    # 1. Number cards (0-9)
    for color in colors:
        deck.append({'color': color, 'type': 'number', 'value': 0})
        for value in range(1, 10):
            deck.append({'color': color, 'type': 'number', 'value': value})
            deck.append({'color': color, 'type': 'number', 'value': value})
            
    # 2. Action cards (Skip, Reverse, Draw Two)
    action_types = ['Skip', 'Reverse', 'Draw Two']
    for color in colors:
        for action in action_types:
            deck.append({'color': color, 'type': 'action', 'value': action})
            deck.append({'color': color, 'type': 'action', 'value': action})
            
    # 3. Wild cards (Wild, Wild Draw Four)
    for _ in range(4):
        deck.append({'color': 'Wild', 'type': 'wild', 'value': 'Wild'})
        deck.append({'color': 'Wild', 'type': 'wild', 'value': 'Wild Draw Four'})
        
    return deck

def shuffle_deck(deck):
    """Shuffles the deck in place using the Fisher-Yates algorithm."""
    n = len(deck)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]
    return deck

def draw_card(deck):
    """Removes and returns the top card from the deck."""
    if len(deck) > 0:
        return deck.pop(0)
    else:
        return None

def start_game(deck):
    """Deals a starting hand of 7 cards from the deck."""
    hand = []
    for _ in range(7):
        card = draw_card(deck)
        if card:
            hand.append(card)
    return hand

def display_discard_menu(deck):
    """Menu to set up and show the top card of the discard pile (Fits 5x16 screen)."""
    top_card = draw_card(deck)
    
    # Robot goes to center to establish discard pile
    robot_trip_action("Set Discard")
    
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Discard Pile:")
    
    brain.screen.set_cursor(2, 1)
    if top_card:
        card_str = "{top_card['color']} {top_card['value']}"
        brain.screen.print(card_str[:16])
    else:
        brain.screen.print("Deck Empty!")
    
    brain.screen.set_cursor(4, 1)
    brain.screen.print("Press CHECK to")
    brain.screen.set_cursor(5, 1)
    brain.screen.print("start game...")
    
    while not brain.buttonCheck.pressing():
        wait(20, MSEC)
    while brain.buttonCheck.pressing():
        wait(20, MSEC)
        
    return top_card

def configure_wild_card():
    """Allows player to choose color, value, and draw count for a Wild card using Left/Right/Check."""
    colors = ['Red', 'Yellow', 'Green', 'Blue']
    color_idx = 0
    
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("Wild: Color")
        brain.screen.set_cursor(3, 1)
        brain.screen.print("> {colors[color_idx]}")
        brain.screen.set_cursor(5, 1)
        brain.screen.print("L/R:Cycle C:Select")
        
        if brain.buttonLeft.pressing():
            color_idx = (color_idx - 1) % len(colors)
            wait(200, MSEC)
        elif brain.buttonRight.pressing():
            color_idx = (color_idx + 1) % len(colors)
            wait(200, MSEC)
        elif brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                wait(20, MSEC)
            chosen_color = colors[color_idx]
            break
        wait(50, MSEC)
        
    values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', 'Draw Two']
    val_idx = 0
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("Wild: Value")
        brain.screen.set_cursor(3, 1)
        brain.screen.print("> {values[val_idx]}")
        brain.screen.set_cursor(5, 1)
        brain.screen.print("L/R:Cycle C:Select")
        
        if brain.buttonLeft.pressing():
            val_idx = (val_idx - 1) % len(values)
            wait(200, MSEC)
        elif brain.buttonRight.pressing():
            val_idx = (val_idx + 1) % len(values)
            wait(200, MSEC)
        elif brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                wait(20, MSEC)
            chosen_value = values[val_idx]
            break
        wait(50, MSEC)
        
    draw_counts = [0, 2, 4, 6]
    draw_idx = 0
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("Wild: Draw Count")
        brain.screen.set_cursor(3, 1)
        brain.screen.print("> Draw {draw_counts[draw_idx]} cards")
        brain.screen.set_cursor(5, 1)
        brain.screen.print("L/R:Cycle C:Select")
        
        if brain.buttonLeft.pressing():
            draw_idx = (draw_idx - 1) % len(draw_counts)
            wait(200, MSEC)
        elif brain.buttonRight.pressing():
            draw_idx = (draw_idx + 1) % len(draw_counts)
            wait(200, MSEC)
        elif brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                wait(20, MSEC)
            chosen_draw_count = draw_counts[draw_idx]
            break
        wait(50, MSEC)
        
    return chosen_color, chosen_value, chosen_draw_count

def get_legal_cards(player_hand, top_card):
    """Checks which cards from the player's hand are legal to play."""
    legal_indices = []
    for i, card in enumerate(player_hand):
        if (card['color'] == 'Wild' or 
            card['color'] == top_card['color'] or 
            str(card['value']) == str(top_card['value'])):
            legal_indices.append(i)
    return legal_indices

def choose_legal_card_or_draw(player_hand, legal_indices, top_card):
    """Allows player to choose a legal card or draw using buttons."""
    selection_idx = 0
    max_idx = len(legal_indices)  
    
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        
        if not legal_indices:
            brain.screen.print("No Legal Cards!")
            brain.screen.set_cursor(2, 1)
            brain.screen.print("Must Draw Card")
            brain.screen.set_cursor(5, 1)
            brain.screen.print("CHECK: Confirm")
            
            while not brain.buttonCheck.pressing():
                wait(20, MSEC)
            while brain.buttonCheck.pressing():
                wait(20, MSEC)
            return -1
            
        if selection_idx < len(legal_indices):
            hand_idx = legal_indices[selection_idx]
            card = player_hand[hand_idx]
            brain.screen.print("Legal ({selection_idx+1}/{len(legal_indices)})")
            brain.screen.set_cursor(2, 1)
            brain.screen.print("{card['color']} {card['value']}"[:16])
            brain.screen.set_cursor(4, 1)
            brain.screen.print("L/R: Scroll")
            brain.screen.set_cursor(5, 1)
            brain.screen.print("CHECK: Play Card")
        else:
            brain.screen.print("Action Option:")
            brain.screen.set_cursor(2, 1)
            brain.screen.print("> Draw Card")
            brain.screen.set_cursor(4, 1)
            brain.screen.print("L/R: Scroll")
            brain.screen.set_cursor(5, 1)
            brain.screen.print("CHECK: Draw Card")
            
        if brain.buttonLeft.pressing():
            selection_idx = (selection_idx - 1) % (max_idx + 1)
            wait(200, MSEC)
        elif brain.buttonRight.pressing():
            selection_idx = (selection_idx + 1) % (max_idx + 1)
            wait(200, MSEC)
        elif brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                wait(20, MSEC)
            
            if selection_idx == len(legal_indices):
                return -1  
            else:
                return legal_indices[selection_idx]  
                
        wait(50, MSEC)

# --- Main Program Execution ---
brain.screen.clear_screen()
brain.screen.set_cursor(1, 1)
brain.screen.print("Setting up UNO...")

uno_deck = create_uno_deck()
shuffle_deck(uno_deck)
player_hand = start_game(uno_deck)
current_top_card = display_discard_menu(uno_deck)

pending_draw_penalty = 0
if current_top_card['value'] == 'Draw Two':
    pending_draw_penalty = 2
elif current_top_card['value'] == 'Wild Draw Four':
    pending_draw_penalty = 4

# --- Main Game Loop ---
while True:
    brain.screen.clear_screen()
    
    # 1. Handle active forced draw penalties
    if pending_draw_penalty > 0:
        brain.screen.set_cursor(1, 1)
        brain.screen.print("Forced Draw: {pending_draw_penalty}")
        brain.screen.set_cursor(3, 1)
        brain.screen.print("Press CHECK to draw")
        
        while not brain.buttonCheck.pressing():
            wait(20, MSEC)
        while brain.buttonCheck.pressing():
            wait(20, MSEC)
            
        # Robot goes to center to draw penalty cards
        robot_trip_action("Draw Penalty")
        
        for _ in range(pending_draw_penalty):
            dc = draw_card(uno_deck)
            if dc:
                player_hand.append(dc)
                
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("Drew {pending_draw_penalty} cards!")
        brain.screen.set_cursor(4, 1)
        brain.screen.print("Press CHECK for")
        brain.screen.set_cursor(5, 1)
        brain.screen.print("next turn...")
        
        while not brain.buttonCheck.pressing():
            wait(20, MSEC)
        while brain.buttonCheck.pressing():
            wait(20, MSEC)
            
        pending_draw_penalty = 0
    else:
        # 2. Find legal cards and let player choose
        legal_card_indices = get_legal_cards(player_hand, current_top_card)
        chosen_index = choose_legal_card_or_draw(player_hand, legal_card_indices, current_top_card)
        
        if chosen_index == -1:
            # Voluntary draw action
            robot_trip_action("Draw Card")
            
            drawn_card = draw_card(uno_deck)
            if drawn_card:
                player_hand.append(drawn_card)
                brain.screen.clear_screen()
                brain.screen.set_cursor(1, 1)
                brain.screen.print("You Drew:")
                brain.screen.set_cursor(2, 1)
                brain.screen.print("{drawn_card['color']} {drawn_card['value']}"[:16])
                brain.screen.set_cursor(4, 1)
                brain.screen.print("Press CHECK for")
                brain.screen.set_cursor(5, 1)
                brain.screen.print("next turn...")
                
                while not brain.buttonCheck.pressing():
                    wait(20, MSEC)
                while brain.buttonCheck.pressing():
                    wait(20, MSEC)
        else:
            # Play card action
            played_card = player_hand.pop(chosen_index)
            
            if played_card['color'] == 'Wild':
                chosen_color, chosen_value, chosen_draw = configure_wild_card()
                played_card['color'] = chosen_color
                played_card['value'] = chosen_value
                pending_draw_penalty = chosen_draw
            else:
                if played_card['value'] == 'Draw Two':
                    pending_draw_penalty = 2
                elif played_card['value'] == 'Wild Draw Four':
                    pending_draw_penalty = 4
            
            # Robot drives to center to discard the card played
            robot_trip_action("Discard Card")
            current_top_card = played_card
                
            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)
            brain.screen.print("Played Successfully!")
            wait(1200, MSEC)

    # 3. Win Condition
    if len(player_hand) == 0:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("YOU WIN!")
        brain.screen.set_cursor(3, 1)
        brain.screen.print("UNO Game Over")
        break

    # Deck safety check & reshuffle
    if len(uno_deck) < 5:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("Reshuffling deck!")
        uno_deck = create_uno_deck()
        shuffle_deck(uno_deck)
        wait(1000, MSEC)