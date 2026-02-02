from pyfrotz import Frotz
from pyfrotz.parsers import advent_intro_parser, planetfall_intro_parser

# load your game file
data = 'games/zork1.z5'
#data = "/home/miro/PycharmProjects/GameSkills/ovos-skill-planet-fall-game/res/planetfall.z5"
game = Frotz(data,"/usr/games/dfrotz")




#description  = game.do_command("zorktest.qzl")
#print (description)
# or play in the cli

             
game.play_loop()

