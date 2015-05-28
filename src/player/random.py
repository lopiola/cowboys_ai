from random import *


class Player:

    def name( self, name):
        self.name = name
        self.strategies = ["LADUJ", "UNIK", "LADUJ", "LADUJ"]
        for i in range(3):
           if( i != name ):
             self.strategies += ["STRZEL %d" % i]
        self.message( "strategies = %s" % str(self.strategies) )
        

    def message( self, s ):
        pass
#        print "Player %i: %s" % (self.name, s)
    
    def start( self ):
        self.message( "start" )

    def strategy( self ):
        s = choice( self.strategies )
        self.message( s )
        return s
    
    def preround_info( self, alive, bullets ):
        pass

    def round_result( self, s ):
        self.message( "round results --> %s" % str( s ) )

    def die( self ):
        self.message( "died" )
 
    def game_over( self, x ):
        self.message( "game over --> %f" % x )
