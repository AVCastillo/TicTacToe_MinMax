import pygame,sys
from pygame.locals import *
import math
import copy


game_tiles=[[" "," "," "],[" "," "," "],[" "," "," "]]

print(game_tiles)



class tile:
    def __init__(self,value,x,y,loc):
        self.value=value
        self.loc=loc
        self.x=x
        self.y=y

    def getloc(self,mouse_coords): #checks if this tile was clicked
        if (mouse_coords[0]>=self.loc[0] and mouse_coords[0]<=self.loc[0]+100) and (mouse_coords[1]>=self.loc[1] and mouse_coords[1]<=self.loc[1]+100):
            return True
        else:
            return False
    def set_val(self,value):
        self.value=value
        game_tiles[self.x][self.y]=value

    def get_coords(self):
        return ([self.x,self.y])          


def someone_won(game_tiles):
    
    #this will check if someone won on either of the two diagonals in the game tiles
    #iw will return an array of which consist of a True boolean value and the marker of the winner (X or O)
    if game_tiles[0][0] != ' 'and game_tiles[0][0] == game_tiles[1][1] and game_tiles[1][1] == game_tiles[2][2]:
        return [True,game_tiles[0][0]]
    elif  game_tiles[0][2] != ' ' and game_tiles[0][2] == game_tiles[1][1] and game_tiles[1][1] == game_tiles[2][0]:
        return [True,game_tiles[0][2]]
    

    #this will check if someone won on either of the three verticals in the game tiles
    #iw will return an array of which consist of a True boolean value and the marker of the winner (X or O)
    for j in range(3):
        if game_tiles[2][j] != ' 'and  game_tiles[0][j] == game_tiles[1][j] and game_tiles[1][j] == game_tiles[2][j]:
            return [True,game_tiles[1][j]]

    
    
    #this will check if someone won on either of the three horizontals in the game tiles
    #iw will return an array of which consist of a True boolean value and the marker of the winner (X or O)
    for i in game_tiles:
        if i[2] != ' ' and i[0] == i[1] and i[1] == i[2]:
            return [True,i[1]]

    
  
    
    return [False,None]


#this will check if someone won the game or not
#if someone one and it is the user player, -1 will be returned, if it is the computer player, 1 will be returned
#if either of the players have won, 0 will be returned signifying a tie 
def utility(game_tiles):
    global player
    if someone_won(game_tiles)[0]:
        if someone_won(game_tiles)[1]!=player:
            return 1
        else:
            return -1

    return 0    

#this is the pseudocode from the handout with alpha beta pruning implementation
def min_value(game_tiles,alp,bet):
    global player #marker of the player
    
    beta=bet #upper bound
    alpha=alp #lower bound
    holder_copy= copy.deepcopy(game_tiles) # copy the state of the game_tiles to a holder so that we can traverse the next possible actions without compromising the main game_tiles state
    m=math.inf #min value

    #traverses the possible moves in the current state of the holder_copy
    for move in possible_moves(holder_copy):
        holder_copy[move[0]][move[1]]=player #places a marker of the player to each instance of possible actions
        v=value(True,holder_copy,alpha,beta) #calls value function which will then call the max_value function if someone hasn't won yet
        holder_copy[move[0]][move[1]] = ' '  #revert back to the previous state of the holder_copy before doing the action/move
        
        m=min(m,v) 

        #implementation of alpha beta pruning
        if v<=alpha:
            return m
        beta=min(beta,m)

    return m

#this is the pseudocode from the handout with alpha beta pruning implementation
def max_value(game_tiles,alp,bet):
    global computer #marker of the computer/ai
    alpha=alp #lower bound
    beta=bet #upper bound
    holder_copy= copy.deepcopy(game_tiles) # copy the state of the game_tiles to a holder so that we can traverse the next possible actions without compromising the main game_tiles state
    m=-math.inf #max value

    #traverses the possible moves in the current state of the holder_copy
    for move in possible_moves(holder_copy):
        holder_copy[move[0]][move[1]]=computer #places a marker of the computer to each instance of possible actions
        v=value(False,holder_copy,alpha,beta) #calls value function which will then call the min_value function if someone hasn't won yet
        holder_copy[move[0]][move[1]] = ' ' #revert back to the previous state of the holder_copy before doing the action/move
        
        m=max(m,v)

        #alpha beta pruning implementation
        if v>=beta:
            return m
        alpha=min(alpha,m)

    return m

#this will be used to traverse all the possible moves from a state up to the terminal states
#terminal states are either the game is won by someone or there are no winners at all (tie)
#max and min value functions will just be called interchangeably until one of the terminals states is achieved
def value(turn,game_tiles,alpha,beta):
    if someone_won(game_tiles)[0] or check_tie(game_tiles):
        return utility(game_tiles)
    if turn:
        return max_value(game_tiles,alpha,beta)

    if not turn:
        return min_value(game_tiles,alpha,beta)    


#determines if there is a tie by checking the empty strings in the game tile array
def check_tie(game_tiles):
    for i in game_tiles:
        for j in i:
            if j == ' ':
                return False
    return True

#returns all the possible moves of a certain state of game_tiles
def possible_moves(game_tiles):
    moves=[]
    for i in range(0,len(game_tiles)):
        for j in range(0,len(game_tiles[0])):
            if game_tiles[i][j] == ' ':
                moves.append([i,j])

    return moves            

#this will serve as the parent node of all the nodes that are generated
#this will be called every after the user exhausted his/her turn
def caller_to_move(game_tiles):
    global computer
    action = None
    holder_copy = copy.deepcopy(game_tiles)
    max_value = -math.inf
    for move in possible_moves(holder_copy):
        holder_copy[move[0]][move[1]] = computer
        print("ai",move)
        result_value = value(False,holder_copy, -math.inf, math.inf)
        holder_copy[move[0]][move[1]] = ' '  

        #if the resulting value on a certain move is greater than -infinity, then it's the best move
        if result_value > max_value:
            action = move #the move that is done to achieve the current resulting value will be assigned to the actionv variable
            max_value = result_value #the new max value will be the current resulting value
    
    return action #after all possible moves have been exhausted, the action variable will contain the best possible move to be done, so it will be returned to the caller


pygame.init()

width=600
height=600

window=pygame.display.set_mode((width,height))
pygame.display.set_caption('Exer 10')

turn=None
player=None
computer=None
run=True
choose_marker=True
play=False

def render_grid():
    bg=(255,255,200)
    color=(50,50,50)
    window.fill(bg)
    for i in range(0,4):
        pygame.draw.line(window,color,(0,i*100),(width-300,i*100))
        pygame.draw.line(window,color,(i*100,0),(i*100,height-300))
textfont=pygame.font.SysFont("monospace",50)
textfont2=pygame.font.SysFont("monospace",30)
textfont3=pygame.font.SysFont("monospace",20)
bg=(173, 216, 230)
while run:
    
    window.fill(bg)


    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        elif event.type==pygame.MOUSEBUTTONUP:
            pos=pygame.mouse.get_pos()
            if not someone_won(game_tiles)[0] and not check_tie(game_tiles):
                if play:
                    for i in tile_array:
                        if i.getloc(pos) and turn==1 and i.value==' ':
                            i.set_val(player)
                            print(i.value)
                            turn=0
                            print(i.x,i.y)
                            game_tiles[i.x][i.y]=player    
                        
    
                if choose_marker:
                    if (pos[0]>= 135 and pos[0]<=135+80) and (pos[1]>=50 and pos[1] <= 50+30): 
                        print("chose X!")
                        turn=1
                        player="X"
                        computer="O"
                        choose_marker=False
                        play=True
                    elif (pos[0]>= 235 and pos[0]<=235+80) and (pos[1]>=50 and pos[1] <= 50+30):
                        print("chose O!")
                        turn=0
                        player="O"
                        computer="X"
                        choose_marker=False
                        play=True  
            
            
        
            if (pos[0]>= 335 and pos[0]<=335+80) and (pos[1]>=50 and pos[1] <= 50+30):
                print("Exit!")
                pygame.quit()
                sys.exit()
    
    if turn==0 and not someone_won(game_tiles)[0] and not check_tie(game_tiles) and play:
        comp=caller_to_move(game_tiles)
        game_tiles[comp[0]][comp[1]]=computer
        turn=1
    if someone_won(game_tiles)[0]:
        if someone_won(game_tiles)[1]==computer:
            pygame.draw.rect(window,(255,255,255),(135,50,80,30))
            result=textfont2.render("You lost!",1,(0,0,0))
            result2=result.get_rect()
            result2.center=(280,500)
            window.blit(result,result2)
        else:
            pygame.draw.rect(window,(255,255,255),(135,50,80,30))
            result=textfont2.render("You won!",1,(0,0,0))
            result2=result.get_rect()
            result2.center=(280,500)
            window.blit(result,result2)    



    if check_tie(game_tiles):
        
        pygame.draw.rect(window,(255,255,255),(135,50,80,30))
        result=textfont2.render("Draw!",1,(0,0,0))
        result2=result.get_rect()
        result2.center=(280,500)
        window.blit(result,result2)

   #draw the X option button
    pygame.draw.rect(window,(255,255,255),(135,50,80,30))
    X_text=textfont2.render("X",1,(0,0,0))
    X_text2=X_text.get_rect()
    X_text2.center=(170,65)
    window.blit(X_text,X_text2)

    #draw the O option button
    pygame.draw.rect(window,(255,255,255),(235,50,80,30))
    O_text=textfont2.render("O",1,(0,0,0))
    O_text2=O_text.get_rect()
    O_text2.center=(270,65)
    window.blit(O_text,O_text2)

    #draw the button for exit
    pygame.draw.rect(window,(255,255,255),(335,50,80,30))
    exit_text=textfont3.render("Exit",1,(0,0,0))
    exit_text2=exit_text.get_rect()
    exit_text2.center=(375,65)
    window.blit(exit_text,exit_text2)

    tile1=tile(game_tiles[0][0],0,0,(120,120))
    tile2=tile(game_tiles[0][1],0,1,(225,120))
    tile3=tile(game_tiles[0][2],0,2,(330,120))
    tile4=tile(game_tiles[1][0],1,0,(120,225))
    tile5=tile(game_tiles[1][1],1,1,(225,225))
    tile6=tile(game_tiles[1][2],1,2,(330,225))
    tile7=tile(game_tiles[2][0],2,0,(120,330))
    tile8=tile(game_tiles[2][1],2,1,(225,330))
    tile9=tile(game_tiles[2][2],2,2,(330,330))         

    tile_array=[tile1,tile2,tile3,tile4,tile5,tile6,tile7,tile8,tile9]
    
    
    #render and re-render the values of each tiles
    t1=textfont.render(str(tile1.value),1,(0,0,0))  
    t2=textfont.render(str(tile2.value),1,(0,0,0))  
    t3=textfont.render(str(tile3.value),1,(0,0,0))  
    t4=textfont.render(str(tile4.value),1,(0,0,0))  
    t5=textfont.render(str(tile5.value),1,(0,0,0))  
    t6=textfont.render(str(tile6.value),1,(0,0,0))  
    t7=textfont.render(str(tile7.value),1,(0,0,0))  
    t8=textfont.render(str(tile8.value),1,(0,0,0))  
    t9=textfont.render(str(tile9.value),1,(0,0,0))  

    text_array=[t1,t2,t3,t4,t5,t6,t7,t8,t9]
    

    #draw and re-draw tiles along with their values
    for j in range(len(tile_array)):
        pygame.draw.rect(window,(255,255,255),(tile_array[j].loc[0],tile_array[j].loc[1],100,100))
        window.blit(text_array[j],(tile_array[j].loc[0]+35,tile_array[j].loc[1]+20))  

    pygame.display.update()

pygame.QUIT()            