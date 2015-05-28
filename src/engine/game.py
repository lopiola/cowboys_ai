from random    import *
from itertools import *
from sys       import *

# player_names = ["pioro","anielski","ostaszewski","goik"]
# test = True


GAMES_TO_PLAY   = 10
ROUNDS_PER_GAME = 30
GUN_SIZE        = 3


def message( kind, msg ):
  print "### COWBOYS( %s ): %s" % (kind, msg)





def createPlayers( names ):
  players = []
  i = 0
  for name in names:
#    print name
    X = __import__(name)
    players += [ X.Player() ]
    try:
      players[i].name(i)
    except:
      pass
    i+=1

  return players





def games( names ):
  
  scores = [0.0, 0.0, 0.0]

  message( "START SERIES", str(names) )
  players = createPlayers( names )  
  for i in range( GAMES_TO_PLAY ):
     message( "GAME START", str(i+1) )
     scores = game( players, scores )

  return scores




def game( players, scores ):

  # stan gry
  bullets   = [ 0    , 0    , 0    ]  # liczba naboi w rewolwerze
  players_alive = 3                   # liczba zywych graczy
  alive     = [ True , True , True ]  # czy kowboj zyje
  hide_prev = [ False, False, False]  # czy poprzednio wykonal unik
  hide_now  = [ False, False, False]  # czy teraz wykonuje unik
  shoots    = [ False, False, False]  # czy do kogos strzela
  dies_now  = [ False, False, False]  # czy umiera w tej rundzie
  reason    = [ ""   , ""   , ""   ]  # powod smierci
  shoots_at = [ -1   , -1   , -1   ]  # do kogo strzela
  

  # poinformuj kazdego gracza o poczatku gry
  for i in range(3):
    try: 
      players[i].start()
    except:
      message( "EXCEPTION", "start of player %i" % i )

  # rozegraj kolejne rundy
  for r in range( ROUNDS_PER_GAME ):

    for i in range(3): 
      hide_prev[i] = hide_now[i]
      dies_now[i]  = False
      shoots[i]    = False

    for i in range(3):
      try:
        players[i].preround_info( alive[:], bullets[:] )
      except:
        message( "EXCEPTION", "player uses API <0.3?" )


    strategy = [ "UNIK", "UNIK", "UNIK" ]
    for i in range(3):
      try:
        if( alive[i] ):
          strategy[i] = players[i].strategy()
        else: 
          strategy[i] = "DEAD"
      except:
        strategy[i] = "UNIK"  
        message( "EXCEPTION", "players[%i].strategy()" % i )

    for i in range(3):
      if type(strategy[i]) != type(""):
        strategy[i] = "UNIK"


    message( "ROUND %i" % r, "strategies %s" % str( strategy ))

    # parsuj zaproponowane strategie
    for i in range(3):
    
      dies_now[i] = False

      if( alive[i] ):
        if( strategy[i] == "LADUJ" ):
          bullets[i] += 1

        hide_now[i] = False
        if( strategy[i] == "UNIK"  ):
          hide_now[i] = True

        shoots[i] = False
        if( strategy[i][0:6] == "STRZEL"): 
          shoots[i] = True
          shoots_at[i] = int(strategy[i][7:])
          # strzal w siebie przy bledzie---zmarnowana runda
          if( (shoots_at[i] < 0) or (shoots_at[i] > 2)):
            shoots_at[i] = i
            strategy[i] = ("STRZEL %i" % i)



    # wykonaj strategie
    for i in range(3):

      if( bullets[i] > GUN_SIZE ):
        dies_now[i] = True
        reason[i]   = "loading bullet above the limit"

      if( (hide_now[i] == True) and (hide_prev[i] == True) ):
        dies_now[i] = True
        reason[i]   = "hiding two times in a row"

      if( shoots[i] ):
        if( bullets[i] == 0 ):
          dies_now[i] = True
          reason[i] = "shoting without bullets"
          continue

        bullets[i] -= 1

        if( hide_now[shoots_at[i]] ):
          continue
        if( shoots[ shoots_at[i] ] and (shoots_at[ shoots_at[i] ] == i) ):
          continue
        dies_now[ shoots_at[i]] = True
        reason[ shoots_at[i]] = ("shot by %i" %i)



    # poinformuj o strategiach i o smierci
    for i in range(3):
      try:
        players[i].round_result( strategy )
      except:
        message( "EXCEPTION", "round_result %i" % i )      

      try:
        if( dies_now[i] and alive[i] ):
          message( "DIE", "player %i, reason = %s" % (i, reason[i]) )
          players[i].die()
      except:
        message( "EXCEPTION", "die %i" % i)      

    # sprawdz, czy ktos zyje
    for i in range(3):
      if( dies_now[i] ): 
        alive[i] = False      
    players_alive =  int(alive[0]) + int(alive[1]) + int(alive[2])
    if( players_alive <= 1 ):
      break 

    #ile nabojow
#    for i in range(3):
#      message("BULLETS", "%i --> %i" % (i, bullets[i]))

    

  # podaj wyniki
  game_scores = [0.0, 0.0, 0.0]
  if( players_alive > 0 ):
    for i in range(3):
      game_scores[i] = float( alive[i] ) / float(players_alive)
  else:
    get_points = int(dies_now[0]) + int(dies_now[1]) + int(dies_now[2])
    for i in range(3):
      game_scores[i] = float( dies_now[i] ) / float( get_points )

  for i in range(3):
    try:
      players[i].game_over( game_scores[i] )
    except:
      message( "EXCEPTION", "game_over %i" % i )


  for i in range(3):
    scores[i] += game_scores[i]
  

  return scores







if __name__ == "__main__":
   
  seed()
  if len(argv) < 4:
    print "Invocation:"
    print "   game player1 player2 player3"
    exit()

  scores = games( argv[1:4] )
  print scores





















