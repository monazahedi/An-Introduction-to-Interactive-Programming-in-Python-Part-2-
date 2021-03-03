
# implementation of card game - Memory

import simplegui
import random


# helper function to initialize globals
def new_game():
    global state, memory_deck, exposed, turns, match_index
    list_1=range(8)
    list_2=range(8)
    random.shuffle(list_1)
    random.shuffle(list_2)
    list_1.extend(list_2)
    memory_deck = list_1
    state = 0
    turns = 0
    exposed = [False]*16
    match_index = []
    label.set_text("Turns = " + str(turns))
         
# define event handlers

def mouseclick(pos):
    global card_1, card_2, card_3, state, card_index_1, card_index_2, card_index_3, turns
    
    if state == 0:
        card_index_1 = pos[0] // 50
        card_1 = memory_deck[card_index_1]
        exposed[card_index_1] = True
        state = 1
        
    elif state == 1:
        card_index_2 = pos[0] // 50
        if not (card_index_2 == card_index_1):
            if card_index_2 not in match_index:
                card_2 = memory_deck[card_index_2]
                exposed[card_index_2] = True
                state = 2
                turns += 1
                label.set_text("Turns = " + str(turns))
                
    else:
        card_index_3 = pos[0] // 50
        if not((card_index_3 == card_index_2) or (card_index_3 == card_index_1)):
            card_3 = memory_deck[card_index_3]
            if card_index_3 not in match_index:
                exposed[card_index_3] = True
                if card_1 == card_2:
                    match_index.append(card_index_1)
                    match_index.append(card_index_2)
                else:
                    exposed[card_index_1] = False
                    exposed[card_index_2] = False  
            state = 1
            card_1 = card_3
            card_index_1 = card_index_3
                          
# cards are logically 50x100 pixels in size    
def draw(canvas):
      
    for i in range(16): 
        canvas.draw_text(str(memory_deck[i]), [15 + i*50, 65], 36, 'White') 
                                     
    for i in range(16):
        if exposed[i] == False:
            canvas.draw_polygon([[0 + i*50, 0], [50 + i*50, 0], [50 + i*50, 100], [0 + i*50, 100]], 1, 'Green', 'Green')
    
    for i in range(1,16):
        canvas.draw_line([50*i, 0], [50*i, 100], 2, 'Black')
            
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)
label = frame.add_label("Turns = 0")

# get things rolling
new_game()
frame.start()




