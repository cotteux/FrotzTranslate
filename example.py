from pyfrotz import Frotz
from pyfrotz.parsers import advent_intro_parser, planetfall_intro_parser
import time
# load your game file
data = 'games/zork1.z5'
#data = "/home/miro/PycharmProjects/GameSkills/ovos-skill-planet-fall-game/res/planetfall.z5"
game = Frotz(data,"/usr/games/dfrotz")


# use it inside code
#game_intro = game.parse_intro()
#print(game_intro)
#description  = game.do_command("north")

#print (room)
#print (description)
#time.sleep(0.5)
#des = game.restore('SAVE/zork1.qzl')
#print (des)
#time.sleep(0.5)
#description  = game.do_command("restore")
#print (description)
#time.sleep(0.4)
#description  = game.do_command("zorktest.qzl")
#print (description)
#time.sleep(0.4)
#description  = game.do_command("north")

#print (description)
#time.sleep(0.4)
#description  = game.save("SAVE/zork1.qzl")
#print (description)


#description  = game.do_command("zorktest.qzl\n")
#print (description)
# or play in the cli

             
game.play_loop()

