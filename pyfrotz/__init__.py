import subprocess
import threading
import time
from distutils.spawn import find_executable
from os.path import exists
from googletrans import Translator


from pyfrotz.parsers import default_intro_parser, default_room_parser
with open('frcommands', 'r') as file:
    data = file.read().splitlines()
    #print (data[1].split(':'))
    #autre = data[1].split(':')
    #print(autre[1])

class Frotz:
    def __init__(self, game_data,
                 interpreter=None,
                 save_file="allo.qzl",
                 prompt_symbol=">",
                 intro_parser=None,
                 room_parser=None):
        self.data = game_data
        self.interpreter = (interpreter or
                            find_executable("dfrotz") or
                            "/usr/games/dfrotz")
        self.save_file = save_file
        self.prompt_symbol = prompt_symbol
        self.intro = None
        self.current_room = None
        self.intro_parser = (intro_parser or default_intro_parser)
        self.room_parser = (room_parser or default_room_parser)
        self._get_frotz()

    def _get_frotz(self):

        self.frotz = subprocess.Popen([self.interpreter,self.data],
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE)
        time.sleep(0.1)  # Allow to load

        # Load default savegame
        if exists(self.save_file):
            #print('Loading saved game')
            self.restore(self.save_file)

    def save(self, filename=None):
        """
            Save game state.
        """
        filename = filename or self.save_file
        self.save_file = filename
        self.do_command('save')
        time.sleep(0.5)
        #self._clear_until_prompt(':')
        self.do_command(filename)  # Accept default savegame
        time.sleep(0.5)
        # Check if game returns Ok or query to overwrite
        self.do_command('y')  # reply yes
        #while True:
        #    char = self.frotz.stdout.read(1)
        #    time.sleep(0.01)
        #    if char == b'.':  # Ok. (everything is done)
        #        break  # The save is complete
        #    if char == b'?':  # Indicates an overwrite query
        #        self.do_command('y')  # reply yes

        time.sleep(0.5)
        #self._clear_until_prompt()

    def restore(self, filename=None):
        """
            Restore saved game.
        """
        filename = filename or self.save_file
        self.do_command('restore')
        time.sleep(0.5)
        #self._clear_until_prompt(':')
        self.do_command(filename)  # Accept default savegame
        time.sleep(0.5)
        #self._clear_until_prompt()

    def _clear_until_prompt(self, prompt=None):
        """ Clear all received characters until the standard prompt. """
        # Clear all data with title etcetera
        prompt = prompt or self.prompt_symbol
        char = self.frotz.stdout.read(1).decode()
        if len(prompt) == 1:
            while char != prompt:
                time.sleep(0.001)
                try:
                    char = self.frotz.stdout.read(1).decode()
                except: # non-unicode?
                    pass
        else:
            while not char.endswith(prompt):
                time.sleep(0.001)
                char += self.frotz.stdout.read(1).decode()

    def do_tcommand(self, action):

        tosend='' 
        # translate the right command
                
        for i in data :
            command = i.split(':')
            #print(command)
            if action == command[1] :

                tosend = command[0]
                print(tosend)
                break;
            

                
        if tosend == '' and action != '':            
            translator = Translator()
            translation = translator.translate(action,dest='en')
            tosend = translation.text
            print ('----'+tosend)



            """ Write a command to the interpreter. """
            self.frotz.stdin.write(tosend.encode() + b'\n')
            self.frotz.stdin.flush()
            return self._frotz_read()
        else :
            return

    def do_command(self, action):
        """ Write a command to the interpreter. """
        self.frotz.stdin.write(action.encode() + b'\n')
        self.frotz.stdin.flush()
        return self._frotz_read()


    def _frotz_read(self, prompt_symbol=None):
        """
        Read from frotz interpreter process.
        Returns current scene description.
        """
        
        prompt_symbol = prompt_symbol or self.prompt_symbol
        # Read info
        output = self.frotz.stdout.read(1).decode()
        while output[-1] not in [prompt_symbol,"?"]:
            if self.game_ended():
                return output + "\nGAME OVER"
            output += self.frotz.stdout.read(1).decode()
            
            if  self.save_file in output :
                #print ("POUET")
                return output

        # remove prompt symbol
        if output.endswith(prompt_symbol):
            output = output[:-1]

        # extract room info
        if self.room_parser:
            self.room, output = self.room_parser(output)
        # translate the text 
        if output !='' :
            translator = Translator()
            translation = translator.translate(output,dest='fr')
        
        return translation.text.strip()

    def parse_intro(self):
        if self.intro_parser:
            # custom code to "startup" this game
            self.intro = self.intro_parser(self)
        else:
            # default to clearing everything until prompt
            self._clear_until_prompt()
            self.intro = self.do_command("look")
        return self.intro

    def play_loop(self):
        # just for testing in cli
        self.parse_intro()
        print(self.intro)
        try:
            while not self.game_ended():
                cmd = input(">>").strip()
                descript = self.do_tcommand(cmd).strip()
                if not descript and cmd != "look":
                    # some games dont give output sometimes (eg, Advent)
                    try:
                        descript = self.do_command("look").strip()
                    except:
                        pass
                print(descript)
        except KeyboardInterrupt:
            pass

    def game_ended(self):
        poll = self.frotz.poll()
        if poll is None:
            return False
        else:
            return True


class EventFrotz(threading.Thread):
    def __init__(self, game_data, on_game_intro=None,
                 on_game_ended=None,
                 on_game_output_ready=None,
                 on_game_waiting_input=None,
                 on_game_room_changed=None,
                 daemon=True,
                 *args, **kwargs):
        super().__init__(daemon=daemon)
        self.frotz = Frotz(game_data, *args, **kwargs)
        self.cmd = None
        self.cmd_ready = threading.Event()
        self.last_description = None

        self.on_game_ended = on_game_ended
        self.on_game_intro = on_game_intro
        self.on_game_room_changed = on_game_room_changed
        self.on_game_output_ready = on_game_output_ready
        self.on_game_waiting_input = on_game_waiting_input

    def save(self, filename=None):
        self.frotz.save(filename)

    def restore(self, filename=None):
        self.frotz.restore(filename)

    def do_command(self, command):
        # wait until previous command has been consumed
        while self.cmd_ready.is_set():
            time.sleep(0.1)
        self.cmd = command
        self.cmd_ready.set()

    def run(self):
        self.frotz.parse_intro()

        if self.on_game_intro is not None:
            self.on_game_intro(self.frotz.intro)

        if self.on_game_waiting_input is not None:
            self.on_game_waiting_input()

        room = self.frotz.current_room
        while not self.frotz.game_ended():
            self.cmd.wait()
            self.last_description = self.frotz.do_command(self.cmd)

            if self.on_game_output_ready is not None:
                self.on_game_output_ready(self.last_description)

            if self.frotz.current_room != room:
                room = self.frotz.current_room
                if self.on_game_room_changed is not None:
                    self.on_game_room_changed(room)

            self.cmd.clear()

            if self.on_game_waiting_input is not None:
                self.on_game_waiting_input()

        if self.on_game_ended is not None:
            self.on_game_ended()

