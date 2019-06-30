import pygame
import copy
import random

#------------------------------------------------------------preperations--------------------------------------------------------------

#opens the game
pygame.init()
pygame.display.set_caption('SET')

#____________________________________values's and constants I need during the game______________________________________
display_width = 800
display_height = 600
playing = True
black = (0,0,0)
white = (255,255,255)
blue =(0,0,255)
red = (255,0,0)
green = (0,255,0)
yellow = (255,255,0)
secs=0
number_of_cards=12
rows= 3
columns= 4
cards_in_deck_position=(display_width-200,10)
mistakes_position=(display_width-200,120)
your_score_position=(display_width-200,70)
opponents_score_position=(display_width-200,170)
timer_position =(display_width-200,220)
comment_position = (display_width-200,400)
comment_position2 = (display_width-200,430)
comment_position6 = (display_width-250, 460)
comment_position3 = ((display_width-300)/2,(display_height-20)/2)
comment_position4 = ((display_width-300)/2,((display_height-20)/2)+50)
comment_position5 = ((display_width-300)/2,((display_height-20)/2)+80)

#this will become consisting of the loaded images of all SETcards, this list will not change during the game
#further on there will be another list called 'image_deck' this list will be a copy of the full deck, and this will be the list we actually use as a deck during gameplay
full_deck = []

#this will become a list of the currently selected SETcards
selected_cards = []

#this will become a list of all SETcards currently in play
cards_in_play = []

#this will become a list of all possible SET's with the current cards
set_list = []

mistakes = 0
your_score = 0
opponents_score = 0
clock = pygame.time.Clock()
font=pygame.font.SysFont('comicsans',35)
font2=pygame.font.SysFont('comicsans',45,True)
font3=pygame.font.SysFont('comicsand',20)


#different SET card properties        
Number = ['1','2','3']
Shape = ['wave', 'oval', 'diamonds']
Filling = ['full','empty', 'halffull']
Color = ['red','green', 'blue']

#_______________________________________________________________first function___________________________________________________________


#funtion that will introduce the game to the player and ask for a timer value

def Introduction():
    print('welcome to SET')
    print('The game works as follows')
    print('There are 12 cards, every card had 4 different features:')
    print('number of items, shape of the items, how full the items are, and the color of the items')
    print('You need to select a series of 3 cards')
    print('For all of the 4 features, those cards should all have the same feature (for instance they all have 1 item), or they should all be different (for instance 1, 2 and 3 items)')
    print("If thats true, you have a 'SET', you get a point, the cards will be removed and 3 new cards will be added")
    print('Tut you have to be quick, because if the timer runs out the computer will get SET')
    print('The game is over if the deck runs out of cards')
    print('')
    print('To select a card, use the left mouse button')
    print('To deselect a card, use the right mouse button')
    print('When the timer runs out, the computer will show you the SET he found, or he will print that there was no SET')
    print('To continue after that, press any key')
    print('')
    print('Lets start playing!')


    while True:
        try:
            time = int(input('Please Enter how many seconds you would like the timer to be: '))
            break
        except ValueError:
            print('please enter an integer')
    
    return(time)
#____________________________________________________get the display ready____________________________________________

#get a timer value by running the introduction function
#its positioned here to make sure you are done in the python display when it opens the game display
time = Introduction()


#loads a display, from now on we will refer to this surface as "display"
display=pygame.display.set_mode((display_width,display_height))




#___________________________________________________SETcard class_______________________________________________________

#it is a sprite to be able to represent it as a surface in game
class SETCard(pygame.sprite.Sprite):
    def __init__(self, number, shape, filling, color):
        
        pygame.sprite.Sprite.__init__(self)
        self.clicked = False
        self.number = number
        self.shape = shape
        self.filling = filling
        self.color = color
        
        #loads the image of the card
        self.image = pygame.transform.scale(pygame.image.load(number+'_'+shape+'_'+filling+'_'+color+'.png'),(100,148))

    #function will display the card at a certain position on the display
    def Display(self,position):
        #displays the image and remembers the coordinates of the 4 corners
        self.rect = display.blit(self.image,(position))
        #gets the coordinates of the top left corner as x and y
        self.x = position[0]
        self.y = position[1]

    #function that react when the card gets clicked
    def On_Click(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            #checks if the position of the mouse is within the 4 corners of the image
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                #checks if the left or right mouse button is pressed and returns the button
                if event.button == 1:                   
                    return 1                    
                elif event.button == 3:
                    return 3

    #draws a yellow rectangle around the image            
    def Selection(self):
         pygame.draw.rect(display,yellow,[self.x-3,self.y-3,106,154],6)
         
    #removes the yellow rectangle by drawing a white rectangle over it
    def Remove_Selection(self):
        pygame.draw.rect(display,white,[self.x-3,self.y-3,106,154],6)
        
#_________________________________________________________________END SETcard class____________________________________________________

        
                               
#________________________________________________________________Functions that we need as building blocks___________________________________________________

#creates a deck as a list of SETcard instances
def Create_Deck():
    for number in Number:
        for shape in Shape:
            for filling in Filling:
                for color in Color:
                    full_deck.append(SETCard(number,shape,filling,color))
    return full_deck

#creates a dictionary that enables you to fill in the card number and get the card position
def Position_Dict(number_of_cards,rows,columns):
    dict= {}
    n=0
    y=-110
    x=50
    while n < number_of_cards:
        x+=120
        if n % columns == 0:
            y += 170
            x = 50
        dict[n]=(x,y)
        n+=1
    return dict
                
#function that uses the dictionary above to get the coordinates from a certain card currently in play                
def Get_Position(cards_in_play,card,position_dict):
    index = cards_in_play.index(card)
    return position_dict[index]
    
#draws a random card from the image_deck and removes it from the list    
def Random_Card(image_deck):
    a= random.randint(0,len(image_deck)-1)
    card = image_deck[a]
    image_deck.pop(a)
    return card

#function to replace an old card by a new card from the Random_Card function, and displays this card at the right position in play
def Replace_Card(card,new_card,cards_in_play,image_deck,position_dict):
    position = Get_Position(cards_in_play,card,position_dict)
    index = cards_in_play.index(card)
    cards_in_play.insert(index,new_card)
    cards_in_play.pop(index+1)
    cards_in_play[index].Display(position)
    return cards_in_play

#checks for a certain feature if the 3 selected cards have them all the same, all different, or neither of those
def Check_Type(card1,card2,card3):
    if card1 == card2 and card1 == card3:
        return True
    elif (card1 != card2) and (card1 != card3) and (card2 != card3):
        return True
    else:
        return False


#_______________________________________________________________functions used to check SET's and update the set_list ________________________________________________________

#uses the Check_type function on every feature to see if the 3 selected cards form a SET or not
def Check_Set(card1,card2,card3):
    if Check_Type(card1.number,card2.number,card3.number):
        if Check_Type(card1.shape,card2.shape,card3.shape):
            if Check_Type(card1.filling,card2.filling,card3.filling):
                if Check_Type(card1.color,card2.color,card3.color):
                    return True
    return False

#function that can find all SET's in play that use a specific card, and adds it to the set_list
def Find_all_Sets_with(card,cards_in_play,set_list,skip_list):
    skip_list.append(card)
    for card1 in cards_in_play:
        if card1 not in skip_list:
            skip_list.append(card1)
            for card2 in cards_in_play:
                if card2 not in skip_list:
                    if Check_Set(card,card1,card2):
                        if {card,card1,card2} not in set_list:
                            set_list.append({card,card1,card2})
    return set_list

#funtion that can removes all sets containing a specific card from the set_list                  
def Remove_from_set_list(card,set_list):
    set_list[:] = [SET for SET in set_list if not (card in SET)]
    return set_list


#_____________________________________________________primary functions that use the building block functions___________________________________________



#function that removes a certain card, adds a new one, and updates all lists
def New_Cards(card, set_list,image_deck,cards_in_play,position_dict):
    card.Remove_Selection()
    set_list = Remove_from_set_list(card,set_list)
    new_card = Random_Card(image_deck)
    cards_in_play = Replace_Card(card,new_card,cards_in_play,image_deck,position_dict)
    set_list = Find_all_Sets_with(new_card,cards_in_play,set_list,[])
    Text_Printer("cards left: ",len(image_deck), cards_in_deck_position,blue,font)
    Still_Cards = True
    if len(image_deck) == 0:
        Still_Cards = False
    return(cards_in_play,set_list,Still_Cards)


#function that puts 12 cards in play at the start of the game and update all lists accordingly 
def Before_Start(full_deck,number_of_cards,rows,columns,set_list):
    image_deck = copy.copy(full_deck)
    position_dict=Position_Dict(number_of_cards,rows,columns)
    
    #makes a white background on game display
    display.fill(white)
    #for each of the 12 cards, displays it and updates all lists
    for i in range(0,number_of_cards):
        cards_in_play.append(Random_Card(image_deck))
        cards_in_play[i].Display(position_dict[i])
    skip_list = []
    for card in cards_in_play:
        set_list = Find_all_Sets_with(card,cards_in_play,set_list,skip_list)
        skip_list.append(card)
    return (image_deck,position_dict,set_list)

#_______________________________________________________________________other functions_______________________________________________________

#function that can print text on the game's display
def Text_Printer(name,value, position,color,font):
    display.fill(white, (position[0], position[1], 200,30))
    text = font.render(name+str(value),1,color)
    display.blit(text,(position[0],position[1]))

#_______________________________________________________________operations needed before the start of the game____________________________________________

#creates start of game
full_deck = Create_Deck()
beginning=Before_Start(full_deck,number_of_cards,rows,columns,set_list)

#definitions we need to set before the game
image_deck = beginning[0]
position_dict = beginning[1]
set_list = beginning[2]

#tells if the deck is empty or not
Still_Cards = True

#prints different scores and values on the game display
Text_Printer("your score: ",your_score,your_score_position,black,font)
Text_Printer("comp score: ",opponents_score,opponents_score_position,black,font)
Text_Printer("mistakes: ",mistakes,mistakes_position,black,font)  
Text_Printer("cards left: ",len(image_deck), cards_in_deck_position,blue,font)

#time it took to get here
start_time = pygame.time.get_ticks()


#-----------------------------------------------------------------------start Game loop 1----------------------------------------------------------------

#playing is True
while playing:

#-----------------------------------------------------------------------start Game loop 2------------------------------------------------------
    #loop in the first game loop will give the posibility to check if the player wants to play again
    while playing:

        #checks if a second has passed
        if pygame.time.get_ticks()-secs>=0:
            secs+=1000

            #updates the timer in game
            current_time = round(float(time)-((pygame.time.get_ticks()-(start_time))/1000))
            Text_Printer('Time left: ',str(current_time),timer_position,red,font)

#____________________________________________________________if time is up___________________________________________________________________
            #if the time is up
            if current_time <=0:
                #remove all selections the player made
                for card in selected_cards:
                    card.Remove_Selection()
                selected_cards=[]
                
                #if there are no SETs
                if len(set_list) == 0:
                    Text_Printer('There was no SET','',comment_position6,black,font)
                    #adds 3 cards to set_list to replace in the future
                    set_list.append({cards_in_play[0],cards_in_play[1],cards_in_play[2]})
                    
                #if there where SETs
                else:
                    #show the first set in the set_list and updates the computers score
                    for card in set_list[0]:
                        card.Selection()
                    opponents_score+=1
                    Text_Printer("comp score: ",opponents_score,opponents_score_position,black,font)
                    
                Text_Printer('Times Up','',comment_position,red,font2)
                Text_Printer('To continue press any key','',comment_position2,black,font3)                
                pygame.display.update()

                
                Continue = False
                #pauses the game until the player has pressed any key                
                while not Continue:
                    for event in pygame.event.get():

                        #posibitily to quit
                        if event.type == pygame.QUIT:
                            playing = False
                            Continue = True
                        if event.type == pygame.KEYDOWN:
                            Continue = True
                            
                #when any key is pressed continue, add 3 new cards, if the deck can't support 3 new cards: end game loop 2
                for card in set_list[0]:
                    if Still_Cards:
                        new = New_Cards(card, set_list,image_deck,cards_in_play,position_dict)
                        set_list = new[1]
                        cards_in_play = new[0]
                        Still_Cards = new[2]
                    else:
                        playing = False
                        break
                    
                #reset the game timer by updating the start time    
                start_time = pygame.time.get_ticks()
                secs = start_time
                display.fill(white, (comment_position6[0], comment_position[1], 300,100))
                pygame.display.update()


        
        for event in pygame.event.get():
            #possibility to quit again
            if event.type == pygame.QUIT:
                playing = False
#____________________________________________________________________________cards are clicked________________________________________________

            for card in cards_in_play:
                clicked = card.On_Click(event)

                #if left mouse button is pressed, select card
                if clicked == 1:
                    if card not in selected_cards:
                        selected_cards.append(card)
                        card.Selection()

                #if right mouse button is pressed, deselect card
                if clicked == 3:
                    if card in selected_cards:
                        selected_cards.remove(card)
                        card.Remove_Selection()

#______________________________________________________________________3 cards are selected_____________________________________________________
                #if 3 cards are selected check for SET        
                if len(selected_cards)== 3:
                    #check if it is in the set_list
                    if {selected_cards[0],selected_cards[1],selected_cards[2]} in set_list:
                        Text_Printer('SET','',comment_position,green,font2)
                        Text_Printer('To continue press any key','',comment_position2,black,font3)
                        pygame.display.update()
                        
                        #pauses the game until the player has pressed any key
                        Continue = False
                        while not Continue:
                            for event in pygame.event.get():

                                #posibitily to quit
                                if event.type == pygame.QUIT:
                                    playing = False
                                    Continue = True
                                if event.type == pygame.KEYDOWN:
                                    Continue = True
                                    
                        #removes cards and gets new cards into play
                        
                        for card in selected_cards:
                            #checks if the deck can support new cards
                            if Still_Cards:
                                new = New_Cards(card, set_list,image_deck,cards_in_play,position_dict)
                                set_list = new[1]
                                cards_in_play = new[0]
                                Still_Cards = new[2]
                            else:
                                playing = False
                                break
                        #resets the timer again and update your score
                        start_time = pygame.time.get_ticks()
                        secs = start_time
                        selected_cards=[]
                        your_score += 1
                        display.fill(white, (comment_position6[0], comment_position[1], 300,100))
                        Text_Printer("your score: ",your_score,your_score_position,black,font)

                    #if not a set, update the mistake counter and continue as if nothing happened
                    else:
                        Text_Printer('Wrong','',comment_position,red,font2)
                        for card in selected_cards:
                            card.Remove_Selection()
                        selected_cards=[]
                        mistakes +=1
                        Text_Printer("mistakes: ",mistakes,mistakes_position,black,font)
        #update the display                
        pygame.display.update()
        
#-------------------------------------------------------------------------end Game loop 2------------------------------------------------------------

    #remove all images, display the scores        
    display.fill(white)
    Text_Printer("your score: ",your_score,your_score_position,black,font)
    Text_Printer("comp score: ",opponents_score,opponents_score_position,black,font)
    Text_Printer("mistakes: ",mistakes,mistakes_position,black,font)  
    Text_Printer("cards left: ",len(image_deck), cards_in_deck_position,blue,font)

    #display if player has won or lost
    if your_score > opponents_score:
        Text_Printer('Congratulations, you won!','',comment_position3,green,font2)
    elif your_score == opponents_score:
        Text_Printer('Draw','',comment_position3,blue,font2)
    else:
        Text_Printer('Better luck next time','',comment_position3,red,font2)
    Text_Printer('To play again, press spacebar','',comment_position4,black,font)
    Text_Printer('To quit press backspace','',comment_position5,black,font)
    
    pygame.display.update()

    #waits for player to quit, or to play again
    Quit=True
    while Quit:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

#__________________________________________________________reset all values needed to start a new game if spacebar is pressed____________________________________________________
                if event.key == pygame.K_SPACE:
                    playing = True
                    Quit = False

                    selected_cards = []
                    cards_in_play = []
                    set_list = []
                    mistakes = 0
                    your_score = 0
                    opponents_score = 0
                    secs=0
                    beginning=Before_Start(full_deck,number_of_cards,rows,columns,set_list)
                    image_deck = beginning[0]
                    position_dict = beginning[1]
                    set_list = beginning[2]
                    Still_Cards = True
                    time = Introduction()
                       
                    Text_Printer("your score: ",your_score,your_score_position,black,font)
                    Text_Printer("comp score: ",opponents_score,opponents_score_position,black,font)
                    Text_Printer("mistakes: ",mistakes,mistakes_position,black,font)  
                    Text_Printer("cards left: ",len(image_deck), cards_in_deck_position,blue,font)
                    start_time = pygame.time.get_ticks()
                    pygame.display.update()
#____________________________________________________________quits the game if the player wants to quit_____________________________________________________
                    
                elif event.key == pygame.K_BACKSPACE:
                    Quit = False
            elif event.type == pygame.QUIT:
                Quit = False
                print('thanks for playing')
#--------------------------------------------------------------end Game loop 1---------------------------------------------------------------------------------                    
            
#quit game
pygame.quit()

