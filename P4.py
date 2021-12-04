"""
Audio_Menu_State.py
by A.Hornof (ajh) 10-27-2021

This implements a simple audio menu using pygame and the State design pattern.

The State code draws heavily from:
https://refactoring.guru/design-patterns/state
https://refactoring.guru/design-patterns/state/python/example

The pygame code draws heavily from www.pygame.org.

----------------------------------------

User input: <D> or <J> advances through a menu.
            <F> or <K> goes backward through a menu.
            <S> or <L> swaps the menu and outputs the new menu.
            <A> or <;> gives a warning and then quits.
            <Q> or <ESC> quit the program with no warning.
Menu One includes "1", "2", "3"
Menu Two includes "10", "20", "30"
The print statements to the display are strictly for tracing and debuggint, and
  are not considered part of the user interface.

Notes: The "_" in _variable indicates it is a private class variable.

Uses Python 3.10 and pygame 2.0.2
----------------------------------------
Sources for ideas:
eventlist.py from
https://www.pygame.org/docs/ref/examples.html#pygame.examples.eventlist.main
"""
################################################################################

# Import modules
from __future__ import annotations # For annotations in function arguments.
import abc       # For abstract base classes.
import pygame    # Currently using 2.0.2.
from pygame import mixer
import time

from pygame.font import Font
# from pygame.music import play 
# The following should accompany this file, and were created by ajh.
import SoundObject
import SoundObjChain
import SceneManager
# GLOBAL VARIABLES
DATA_DIR = "data"                      # Data subdirectory.
S_FILE_NAV = "Ones_Menu_Navigation.ogg"   # Navigation sounds file name.
S_FILE_PRO = "Navigation_Prompts.ogg" #Prompts sounds file name.
S_FILE_PROMPT = "menu_prompt.ogg"
S_FILE_BOOK = "Norman Chapter 2 Audio.ogg"
S_FILE_HEADING= "heading.ogg"
S_FILE_H_TS = "h_and_ts.ogg"
POS = 0
# f = open("timer.txt", "r")
timer = 0
transition_state = None

import os
def is_non_zero_file(fpath):  #to check if the text file is empty or not
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

class GUI: #the class for the user interface
    def __init__(self) -> None:
        self.title_font = pygame.font.SysFont('FreeSans', 40, bold=True) #set title font
        self.font_color = (0,0,0) #set font color
        self.screen_size = 1920, 1080 #set screen size
        self.bgp1 = pygame.image.load("picture.jpeg") ## set background picture
        self.bgp2 = pygame.image.load("book_reader.png") #et background picture
        self.screen = pygame.display.set_mode(self.screen_size,pygame.RESIZABLE) #initialize the screen
        self.font = pygame.font.SysFont('FreeSans', 25, bold=True) #set the font size 
        self.screen.fill((255,255,255)) #fill the screen in white
        self.screen.blit(self.bgp1,(0,0)) #blit bgp onto screen
        # self.surface = pygame.Surface(self.screen_size)
        self.ellipse_color = (255,255,165)

    def draw_text(self, text, font, color, surface, x, y):
        #draw text function
        textobj = font.render(text, 1, color) #initialize the text object
        textrect = textobj.get_rect() #set the shape of the text
        textrect.topleft = (x, y) #set the position of the text
        surface.blit(textobj, textrect) #blit onto the surface

    def main_menu(self):
        '''
        main menu interface
        '''
        self.screen.blit(self.bgp1,(0,0)) #blit bgp onto the screen everytime main_menu get called
        self.draw_text('Main Menu',self.title_font, self.font_color,self.screen, 735, 100)
        pygame.draw.ellipse(self.screen, self.ellipse_color, (700,293,350,50)) #draw an ellipse

        self.draw_text('1. Choose Your Book', self.font, self.font_color, self.screen, 735,300) 
        self.draw_text('2. Confirm your selection(After pressing 1)', self.font, self.font_color, self.screen, 735,360)
        self.draw_text('3. Continue Reading', self.font, self.font_color, self.screen, 735,390)        
        self.draw_text('4. Help', self.font, self.font_color, self.screen, 735,420) 
        # self.surface.blit(self.screen,(0,0))
        pygame.display.update()

    def choose_book(self):
        '''choose book sub menu interface'''
        self.screen.blit(self.bgp1,(0,0)) #blit bgp onto the screen everytime choose_book get called
        self.draw_text('1. Switch your selection',self.font, self.font_color, self.screen, 735,220) 
        self.draw_text('2. Confirm your selection', self.font, self.font_color, self.screen, 735,250)
        self.draw_text('Main Menu',self.title_font, self.font_color,self.screen, 735, 100)
        self.draw_text('Choose Your Book',self.font, self.font_color,self.screen, 735, 300)
        self.draw_text('0) Design of Everyday Things',self.font, self.font_color,self.screen, 735, 330)
        self.draw_text('1) The Descendent of the Empire',self.font, self.font_color,self.screen, 735, 360)
        self.draw_text('2) Eden Raging',self.font, self.font_color,self.screen, 735, 390)
        self.draw_text('3) Apex Pandemic',self.font, self.font_color,self.screen, 735, 420)
        self.draw_text('4) Bionic Eden',self.font, self.font_color,self.screen, 735, 450)
        self.draw_text('5) Renewal',self.font, self.font_color,self.screen, 735, 480)
        self.draw_text('6) Benediction',self.font, self.font_color,self.screen, 735, 510)
        self.draw_text('7) Alpha Falling',self.font, self.font_color,self.screen, 735, 540)
        self.draw_text('8) Cosmic Son',self.font, self.font_color,self.screen, 735, 570)
        self.draw_text('9) City of Solaris',self.font, self.font_color,self.screen, 735, 600)

        pygame.display.update()

    def book_reader(self):
        '''book reader menu interface'''
        self.screen.blit(self.bgp1,(0,0)) #blit bgp onto the screen everytime book_reader get called
        self.draw_text('Book Reader Menu',self.title_font, self.font_color,self.screen, 735, 100)
        self.draw_text('0.Back to Main',self.font, self.font_color,self.screen, 735, 300)
        self.draw_text('1.Read the Book',self.font, self.font_color,self.screen, 735, 330)
        self.draw_text('2.Read the Headings',self.font, self.font_color,self.screen, 735, 360)
        self.draw_text('3.Read the Headings and Topic Sentences',self.font, self.font_color,self.screen, 735, 390)
        self.draw_text('4.Help',self.font, self.font_color,self.screen, 735, 420)

        pygame.display.update()

    def whole_book(self):
        '''read entire book interface'''
        self.screen.blit(self.bgp2,(0,0)) #blit bgp onto the screen everytime whole_book get called
        self.draw_text('Read Entire Book Page',self.title_font, self.font_color,self.screen, 735, 100)
        self.draw_text('0.Back to Main',self.font, self.font_color,self.screen, 735, 300)
        self.draw_text('1.Go backward 10s ',self.font, self.font_color,self.screen, 735, 330)
        self.draw_text('2.Go forward 10s',self.font, self.font_color,self.screen, 735, 360)
        self.draw_text('3.Play/Pause',self.font, self.font_color,self.screen, 735, 390)
        self.draw_text('4.Help',self.font, self.font_color,self.screen, 735, 420)
        pygame.display.update()

    def only_heading(self):
        '''read only heading interface'''
        self.screen.blit(self.bgp2,(0,0))#blit bgp onto the screen everytime main_menu get called
        self.draw_text('Read Headings Page',self.title_font, self.font_color,self.screen, 735, 100)
        self.draw_text('0.Back to Main',self.font, self.font_color,self.screen, 735, 300)
        self.draw_text('1.Go backward 10s ',self.font, self.font_color,self.screen, 735, 330)
        self.draw_text('2.Go forward 10s',self.font, self.font_color,self.screen, 735, 360)
        self.draw_text('3.Play/Pause',self.font, self.font_color,self.screen, 735, 390)
        self.draw_text('4.Help',self.font, self.font_color,self.screen, 735, 420)
        pygame.display.update()

    def heading_and_hs(self):
        '''read only heading and topic sentence interface'''
        self.screen.blit(self.bgp2,(0,0)) #blit bgp onto the screen everytime main_menu get called
        self.draw_text('Read Headings and Topic Sentences Page',self.title_font, self.font_color,self.screen, 500, 100)
        self.draw_text('0.Back to Main',self.font, self.font_color,self.screen, 735, 300)
        self.draw_text('1.Go backward 10s ',self.font, self.font_color,self.screen, 735, 330)
        self.draw_text('2.Go forward 10s',self.font, self.font_color,self.screen, 735, 360)
        self.draw_text('3.Play/Pause',self.font, self.font_color,self.screen, 735, 390)
        self.draw_text('4.Help',self.font, self.font_color,self.screen, 735, 420)
        pygame.display.update()

def main():
################################################################################

    """
    This function is called when the program starts. it initializes everything
    it needs, and then loops until the program terminates.
    """

    # Initialize pygame.
    pygame.init()
    # Create a small window to make sure that pygame can be accessed.
    screen = pygame.display.set_mode((1920, 1080),pygame.RESIZABLE)
    font = pygame.font.SysFont('FreeSans', 25, bold=True)
    pygame.display.set_caption('Audio Book Reader')

    # Load the clock
    clock = pygame.time.Clock()
    bgp = pygame.image.load("picture.jpeg")
    UI = GUI()
    UI.main_menu()
    # ------------------------------------------------------------------------ #
    #
    # Main Loop
    # Set up  auditory elements.

    # Create the initial enterring-application sound.
    # Send in the backup directory name, the sound file name, the start time,
    #   and the duration. Sometimes different sounds are in the same file.
    # sound_start = SoundObject.SoundObject(DATA_DIR, S_FILE_NAV, 680, 17800)
    # ------------------------------------------------------------------------ #
    # sound_start = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 149700,1600)
    # Create the one SoundObjChain object that the program should be using.
    # There should be only one. You should never have to access it directly.
    SoundObject_chain = SoundObjChain.SoundObjChain()
    # Give the SoundObject module access to the  SoundObjChain object.
    SoundObject.set_SoundObjChain(SoundObject_chain)
    # Variables used within Main Loop
    program_running = True
    # Initialized the menu state.
    context = Context(Main_Menu())

    # start_off()
    # sound_start.play()
    # time.sleep(2)
    while program_running and context.program_running():
        
        # Limits the while loop to a max of 60 clock-ticks per second.
        clock.tick(60)

        # Handle Input Events
        for event in pygame.event.get():

            # This permits closing the pygame window to quit the program.
            if event.type == pygame.QUIT:
                program_running = False

            # Handle Keystroke Events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # print("User pressed Button 0.")
                    context.button_0_press()
                # Button 1 is pressed
                elif event.key == pygame.K_j or event.key == pygame.K_a:
                    # print("User pressed Button 1.")
                    context.button_1_press()

                # Button 2 is pressed
                elif event.key == pygame.K_k or event.key == pygame.K_s:
                    # print("User pressed Button 2.")
                    context.button_2_press()

                # Button 3 is pressed
                elif event.key == pygame.K_l or event.key == pygame.K_d:
                    # print("User pressed Button 3.")
                    context.button_3_press()

                # Button 4 is pressed
                elif event.key == pygame.K_SEMICOLON or event.key == pygame.K_f:
                    # print("User pressed Button 4.")
                    context.button_4_press()

                elif event.key == pygame.K_q:
                    context.button_q_press()
                # <ESC> or <Q> quits
                elif event.key == pygame.K_ESCAPE:
                    # print("User pressed <ESC> or <Q>.")
                    # Ideally, this would give a warning before quitting,
                    #   but that is not implemented yet.
                    program_running = False
                    # sys.exit()
        # Play the sounds in the queue until they are done, or stopped.
        SoundObject_chain.play_until_empty()
    # f.close()
    # Done
    pygame.quit()


################################################################################
class Context:
    """
    The Context defines the interface of interest to clients. It also maintains
    a reference to an instance of a State subclass, which represents the current
    state of the Context. (Code and comments from https://refactoring.guru.)
    """

    # Private class variable.
    _state = None   # A reference to the current state of the Context.
    _program_running = True

    def __init__(self, state: State) -> None:
    # (In the above line, ": State" and "-> None" are annotations.)
        self.transition_to(state)
        
    # Other menu objects must be able to change the current menu at runtime.
    def transition_to(self, state: State):
        print(f"Context: Transition to {type(state).__name__}")
        self._state = state         # Uses @property (the getter decorator)
        self._state.context = self  # Uses @context.setter (setter decorator)
        self._state.entering() #call entering first everytime
    # Quit the program
    def quit(self):
        self._program_running = False

    # Getter for _program_running
    def program_running(self):
        return (self._program_running)

    # The Context delegates part of its behavior to the current State object.
    #   The functions handle each possible button press.
    def button_0_press(self):
        self._state.handle_0()
    def button_1_press(self):
        self._state.handle_1()
    def button_2_press(self):
        self._state.handle_2()
    def button_3_press(self):
        self._state.handle_3()
    def button_4_press(self):
        self._state.handle_4()
    def button_q_press(self):
        self._state.handle_q()

################################################################################

class State(abc.ABC):

    """
    The abstract base class State class declares methods that all Concrete State
    objects should implement, and also provides a backreference to the Context
    object, associated with the State. This backreference can be used by States
    to transition the Context to another State. (From refactoring.guru.)

    The State class provides a template for all of the menus.
    """

    @property         # This is a getter decorator.
    def context(self) -> Context:
        # print("@property was used")
        return self._context

    @context.setter   # This is a setter decorator.
    def context(self, context: Context) -> None:
        # print("@context.setter was used")
        self._context = context
    # @abc.abstractmethod
    # def handle_0(self) -> None:
    #     pass
    @abc.abstractmethod
    def entering(self) -> None:
        pass  
    @abc.abstractmethod
    def handle_0(self) -> None:
        pass    

    @abc.abstractmethod
    def handle_1(self) -> None:
        pass

    @abc.abstractmethod
    def handle_2(self) -> None:
        pass

    @abc.abstractmethod
    def handle_3(self) -> None:
        pass

    @abc.abstractmethod
    def handle_4(self) -> None:
        pass
    
    @abc.abstractmethod
    def handle_q(self) -> None:
        pass   
    # @abc.abstractmethod
    # def handle_H(self) -> None:
    #     pass
################################################################################
# Concrete States implement various behaviors, associated with a state of the
#   Context.

class Book_Library:
    '''save book attribute in the future when more books available
    e.g. name, availablility, cover picture etc'''
    def __init__(self,name, availablility=False) -> None:
        
        self.availablity = availablility
        self.name = name 
book0 = Book_Library(name="Design of Everyday Things",availablility=True)
book1 = Book_Library(name="book1")
book2 = Book_Library(name="book2")
book3 = Book_Library(name="book3")
book4 = Book_Library(name="book4")
book5 = Book_Library(name="book5")
book6 = Book_Library(name="book6")
book7 = Book_Library(name="book7")
book8 = Book_Library(name="book8")
book9 = Book_Library(name="book9")

class Main_Menu(State):
    '''main menu for choosing books and continue reading from previously'''
    prompt1_1 = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 152640, 960) 
    prompt1_2 = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 153700, 7300)
    prompt2 = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 161800, 4900)
    prompt3 = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 167600, 5000)
    prompt_main = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 86000, 2500)
    gui = GUI() #arouse GUI for main menu UI
    book_0 = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 14900, 2200)
    book_1 = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 17100, 2300)
    book_2 = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 19400, 1550)
    book_3 = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 20950, 1600)
    book_4 = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 22550, 1650)
    book_5 = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 24200, 1100)
    book_6 = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 25300, 1360)
    book_7 = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 26660, 1440)
    book_8 = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 28100, 1460)
    book_9 = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 29560, 2340)
    Not_available = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 13534, 957)
    books = [book_0, book_1, book_2, book_3, book_4, book_5, book_6,
             book_7, book_8, book_9]  # List of books
    num_books = len(books)
    prompt1_1.state = True
    i = -1 #iterates through books
    def entering(self) -> None: 
        # self._state = context._state
        # Play the startup sound.
        if self.prompt1_1.state == True: #to check if it is the first time entering this menu
            self.prompt1_1.play()
            self.prompt1_2.chain()
            self.prompt1_1.state = False # set state to false, so it won't prompt the second time.
            print("Press 1 to select the book. Press 2 to confirm your selection. Press 3 to continue reading. Press 4 for help.")
        else:
            self.prompt1_1.play() #only play which menu you are in
            print("Main Menu.") 
    def handle_0(self) -> None:
        pass
    def handle_1(self) -> None:
        print("Choose your book. Press 1 to switch your selection. Press 2 to select.")
        self.gui.choose_book() #go to choose_book() in the gui
        self.i = (self.i+1) % self.num_books #get the index of book
        self.books[self.i].play()
    def handle_2(self) -> None:
        if (self.i == 0):  # The only supported book has been selected
            self.context.transition_to(Book_Reader_Menu())
            self.gui.book_reader() # go to book_reader in gui
        else:  # Any other book was selected
            self.Not_available.play()
            # self.sound_one.play()
        # self.context.transition_to(Book_Reader_Menu())
    def handle_3(self) -> None:
        global transition_state 
        transition_state = self 
        print("transition_state is", transition_state)
        # print("Continue reading.")
        global f 
        f = open("timer.txt", "r")
        # check if size of file is 0
        if os.stat("timer.txt").st_size == 0: #check if the text file is empty
            print('File is empty')
            print("No content has been read.")
            self.prompt3.play()
            f.close() #if empty, close timer.txt

            self.context.transition_to(Main_Menu())
            self.gui.main_menu()
            return None
        content = f.readlines() #else read the two lines from timer.txt

        index = int(content[0].strip("\n")) #first line repreesnts index
        global timer 
        timer = round(float(content[1]), 3) #second line represents timer
        f.close()
        if index == 1: #this is the mark for whole_book()
            self.context.transition_to(Whole_Book()) #initialize a way of recording the menu
            self.gui.whole_book() # go to whole_book() in gui
        if index == 2: #this is the mark for headings()
            self.context.transition_to(Headings())#initialize a way of recording the menu
            self.gui.only_heading() # go to only_heading menu in gui
        if index == 3: # this is the mark for headings_and_ts
            self.context.transition_to(Headings_And_TS())#initialize a way of recording the menu
            self.gui.heading_and_hs() # go to heading_and_ts menu in gui
    def handle_4(self) -> None:
        self.prompt_main.play() #tell the user the current location, chapter.
        self.prompt1_2.chain() #tell the user the instruction
        # global transition_state
        # transition_state = self
        # self.context.transition_to(Help_Menu())
    def handle_q(self) -> None:
        print("quitting.")
        global transition_state #set a global value for quitting button
        transition_state = self #set the value to be the current class
        self.context.transition_to(Menu_Quitting()) 

class Book_Reader_Menu(State):
    '''book reader menu for choosing which reading mode the user wants'''
    prompt1_1 = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 32600, 1390) 
    prompt1_2 = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 34160, 11340)
    prompt_book_reader = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 98630, 2300)
    prompt1_1.state = True #prompt1_1 saved.
    gui = GUI() #initialzie a GUI class object to create an interface
    def entering(self) -> None:
        '''enter this function automatically'''
        if self.prompt1_1.state == True: #if the first time coming into this menu
            self.prompt1_1.play() 
            self.prompt1_2.chain()
            self.prompt1_1.state = False# set state to false, so it won't prompt the second time.
            print("Press 1 to read the whole book. Press 2 to only read headings. Press 3 to read headings and Topic sentences. Press 4 for help. Press 0 to back to Main Menu.")
        else: # if the user has been this menu
            self.prompt1_1.play() #only play which menu you are in
            print("Book Reader Menu.") 
    def handle_0(self) -> None:
        print("Go back to the main menu.")
        self.context.transition_to(Main_Menu())
        self.gui.main_menu() #call main_menu() to go back to main visual interface
    def handle_1(self) -> None:
        print("Read the whole book.")
        self.context.transition_to(Whole_Book())
        self.gui.whole_book() #go to visual interface
    def handle_2(self) -> None:
        print("Only read headings.")
        self.context.transition_to(Headings())
        self.gui.only_heading() #go to heading interface
        # self.sound_two.play()
    def handle_3(self) -> None:
        print("Read headings and topic sentences.")
        self.context.transition_to(Headings_And_TS())
        self.gui.heading_and_hs() #go to heading and topic sentence interface
    def handle_4(self) -> None:
        print("Enter the help menu.")
        self.prompt_book_reader.play()
        self.prompt1_2.chain()
    def handle_q(self) -> None:
        print("Quitting.")
        global transition_state #set a global value for quitting button
        transition_state = self #set the value to be the current class
        self.context.transition_to(Menu_Quitting())


class Whole_Book(State):
    
    prompt1_1 =  SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 49500, 1570)
    prompt1_2 =  SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 51480, 9350)

    sound_book =  SoundObject.SoundObject(DATA_DIR, S_FILE_BOOK, POS, 100000000)
    prompt_whole_book = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 105800, 6000)
    gui = GUI()#initialzie a GUI class object to create an interface
    prompt1_1.state = True 
    def entering(self) -> None:
        # self.paused = paused
        # Play the startup sound.
        if self.prompt1_1.state == True:#to check if it is the first time entering this menu
            self.prompt1_1.play()
            self.prompt1_2.chain()
            self.prompt1_1.state = False# set state to false, so it won't prompt the second time.
            print(" Press 0 to go back to Main Menu. Press 1 to move backward 10 seconds, 2 to move forward 10 seconds. 3 to play or pause. Press 4 for help.")
        else:
            self.prompt1_1.play() #only play which menu you are in
        global transition_state
        if transition_state.__class__ is Main_Menu:
            print("Continue Reading.")
            global POS
            POS = timer*1000 # set position of the music
            POS = int(POS)
            sound_book1 =  SoundObject.SoundObject(DATA_DIR, S_FILE_BOOK, POS, 100000000)
            sound_book1.chain()
        else:
            self.sound_book.chain()

    def handle_0(self) -> None:
        print("Go back to main menu.")
        global f 
        global POS
        f = open("timer.txt", "w+") #write to timer.txt to save the current reading time
        f.write("1\n") #mark this menu so it could be recongized which menu at line 454
        f.write(str(POS/1000)) #the current time
        f.close()
        self.context.transition_to(Main_Menu())
        self.gui.main_menu()#go back to main
    def handle_1(self) -> None:
        print("Move backward 10 seconds.")
        global POS
        POS = self.sound_book.get_curpos() #get the current position
        if (POS < 10000):
            POS = 0 #start from 0 if the current time is less than 10 s
        else:
            POS -= 10000 #reduce 10 seconds
        self.sound_book = SoundObject.SoundObject(DATA_DIR, S_FILE_BOOK, POS, 100000000)
        self.sound_book.set_pos(POS) #set to this position
        self.sound_book.play()
        # self.context.transition_to(Book_Reader_Content_Page())
        
    def handle_2(self) -> None:
        print("Move forward 10 seconds.")
        global POS
        POS = self.sound_book.get_curpos() #get the current position
        POS += 10000
        self.sound_book = SoundObject.SoundObject(DATA_DIR, S_FILE_BOOK, POS, 100000000)
        self.sound_book.set_pos(POS) #set to this position
        self.sound_book.play()
        
    def handle_3(self) -> None:
        if mixer.music.get_busy():#check if any sound is currently playing
            print("Pause reading.")
            mixer.music.pause() #pause the sound
        else:
            print("Continue reading.")
            mixer.music.unpause() #unpause the sound
    def handle_4(self) -> None:
        global f 
        global POS
        f = open("timer.txt", "w+")#write to timer.txt to save the current reading time
        f.write("1\n")#mark this menu so it could be recongized which menu at line 454
        f.write(str(POS/1000))#mark this time
        f.close()
        print("Enter the help menu.")
        self.prompt_whole_book.play()
        self.prompt1_2.chain()
    def handle_q(self) -> None:
        global f 
        global POS
        f = open("timer.txt", "w+")#write to timer.txt to save the current reading time
        f.write("1\n")#mark this menu so it could be recongized which menu at line 454
        f.write(str(POS/1000))#mark this time
        f.close()
        print("quitting.")
        global transition_state
        transition_state = self#set transition_state to be the current menu
        self.context.transition_to(Menu_Quitting())

class Headings(State):
    prompt1_1 =  SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 60800, 1500)
    prompt1_2 =  SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 51480, 9350)

    sound_heading =  SoundObject.SoundObject(DATA_DIR, S_FILE_HEADING, 0, 15333)
    prompt_heading = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 116670, 6300)
    gui = GUI()#initialzie a GUI class object to create an interface
    prompt1_1.state = True
    def entering(self) -> None:
        if self.prompt1_1.state == True:#to check if it is the first time entering this menu
            self.prompt1_1.play()
            self.prompt1_2.chain()
            self.prompt1_1.state = False# set state to false, so it won't prompt the second time.
            print(" Press 0 to go back to Main Menu. Press 1 to move backward 10 seconds, 2 to move forward 10 seconds. 3 to play or pause. Press 4 for help.")
        else:
            self.prompt1_1.play() #only play which menu you are in
        global transition_state
        if transition_state.__class__ is Main_Menu:
            print("Continue Reading.")
            global POS
            POS = timer*1000 # set position of the music
            POS = int(POS)
            sound_heading1 =  SoundObject.SoundObject(DATA_DIR, S_FILE_HEADING, POS, 100000000)
            sound_heading1.chain()
        else:
            self.sound_heading.chain()

    def handle_0(self) -> None:
        print("Go back to main menu.")
        global f 
        global POS
        f = open("timer.txt", "w+")#write to timer.txt to save the current reading time
        f.write("2\n")#mark this menu so it could be recongized which menu at line 454
        f.write(str(POS/1000))#mark this time
        f.close()
        self.context.transition_to(Main_Menu())
        self.gui.main_menu()#go back to main
    def handle_1(self) -> None:
        print("Move backward 10 seconds.")
        global POS
        POS = self.sound_heading.get_curpos()#get the current position
        if (POS < 10000):#start from 0 if the current time is less than 10 s
            POS = 0
        else:
            POS -= 10000#reduce 10 seconds
        self.sound_heading = SoundObject.SoundObject(DATA_DIR, S_FILE_HEADING, POS, 100000000)
        self.sound_heading.set_pos(POS) #set to this position
        self.sound_heading.play()
        # self.context.transition_to(Book_Reader_Content_Page())
    def handle_2(self) -> None:
        print("Move forward 10 seconds.")
        global POS
        POS = self.sound_heading.get_curpos()
        print("POS is ", POS)

        if POS > 5322: #This is to avoid the program going over range.
            POS = 0 #set back to 0
        else:
            POS += 10000 #set time to 10s later
        self.sound_heading = SoundObject.SoundObject(DATA_DIR, S_FILE_HEADING, POS, 100000000)
        self.sound_heading.set_pos(POS) #set to this position
        self.sound_heading.play()
    def handle_3(self) -> None:
        if mixer.music.get_busy():#check if any sound is currently playing
            print("Pause reading.")
            mixer.music.pause() #pause the sound
        else:
            print("Continue reading.")
            mixer.music.unpause() #unpause the sound
    def handle_4(self) -> None:
        global f 
        global POS
        f = open("timer.txt", "w+")#write to timer.txt to save the current reading time
        f.write("2\n")#mark this menu so it could be recongized which menu at line 454
        f.write(str(POS/1000))#mark this time
        f.close()
        print("Enter the help menu.")
        self.prompt_heading.play()
        self.prompt1_2.chain()
    def handle_q(self) -> None:
        print("quitting.")
        global f 
        global POS
        f = open("timer.txt", "w+")#write to timer.txt to save the current reading time
        f.write("2\n")#mark this menu so it could be recongized which menu at line 454
        f.write(str(POS/1000))#mark this time
        f.close()
        global transition_state
        transition_state = self#set transition_state to be the current menu
        self.context.transition_to(Menu_Quitting())
class Headings_And_TS(State):
    prompt1_1 =  SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 72000, 2400)
    prompt1_2 =  SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 51480, 9350)
   
    sound_heading_and_ts =  SoundObject.SoundObject(DATA_DIR, S_FILE_H_TS, POS, 10000000)
    prompt_heading_and_ts = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 127800, 7200)
    gui = GUI()#initialzie a GUI class object to create an interface
    prompt1_1.state = True
    def entering(self) -> None:
        if self.prompt1_1.state == True:#to check if it is the first time entering this menu
            self.prompt1_1.play()
            self.prompt1_2.chain()
            self.prompt1_1.state = False# set state to false, so it won't prompt the second time.
            print("Press 0 to go back to Main Menu. Press 1 to move backward 10 seconds, 2 to move forward 10 seconds. 3 to play or pause. Press 4 for help.")
        else:
            self.prompt1_1.play() #only play which menu you are in
        global transition_state
        if transition_state.__class__ is Main_Menu:
            print("Continue Reading.")
            global POS
            POS = timer*1000 # set position of the music
            POS = int(POS)
            sound_heading_and_ts1 =  SoundObject.SoundObject(DATA_DIR, S_FILE_H_TS, POS, 100000000)
            sound_heading_and_ts1.chain()
        else:
            self.sound_heading_and_ts.chain()

    def handle_0(self) -> None:
        print("Go back to main menu.")
        global f 
        global POS
        f = open("timer.txt", "w+")#write to timer.txt to save the current reading time
        f.write("3\n")#mark this menu so it could be recongized which menu at line 454
        f.write(str(POS/1000))#mark this time
        f.close()
        self.context.transition_to(Main_Menu())
        self.gui.main_menu()#go back to main
    def handle_1(self) -> None:
        print("Move backward 10 seconds.")
        global POS
        POS = self.sound_heading_and_ts.get_curpos()#get the current position
        if (POS < 10000):#start from 0 if the current time is less than 10 s
            POS = 0 #set back to 0
        else:
            POS -= 10000 #reduce 10 seconds
        self.sound_heading_and_ts = SoundObject.SoundObject(DATA_DIR, S_FILE_H_TS, POS, 100000000)
        self.sound_heading_and_ts.set_pos(POS) #set to this position
        self.sound_heading_and_ts.play()
        # self.context.transition_to(Book_Reader_Content_Page())
    def handle_2(self) -> None:
        print("Move forward 10 seconds.")
        global POS
        POS = self.sound_heading_and_ts.get_curpos()
        if POS > 477599: #to aviod POS to go over range
            POS = 0 #set back to 0
        else:
            POS += 10000 #10s added
        self.sound_heading_and_ts = SoundObject.SoundObject(DATA_DIR, S_FILE_H_TS, POS, 100000000)
        self.sound_heading_and_ts.set_pos(POS) #set to this position
        self.sound_heading_and_ts.play()
    def handle_3(self) -> None:
        if mixer.music.get_busy(): #check if any sound is currently playing
            print("Pause reading.")
            mixer.music.pause() #pause the sound
        else:
            print("Continue reading.")
            mixer.music.unpause() #unpause the sound
    def handle_4(self) -> None:
        global f 
        global POS
        f = open("timer.txt", "w+")#write to timer.txt to save the current reading time
        f.write("3\n")#mark this menu so it could be recongized which menu at line 454
        f.write(str(POS/1000))#mark this time
        f.close()
        self.prompt_heading_and_ts.play()
        self.prompt1_2.chain()
    def handle_q(self) -> None:
        print("quitting.")
        global f 
        global POS
        f = open("timer.txt", "w+")#write to timer.txt to save the current reading time
        f.write("3\n")#mark this menu so it could be recongized which menu at line 454
        f.write(str(POS/1000)) #mark this time
        f.close()
        print("quitting.")
        global transition_state
        transition_state = self #set transition_state to be the current menu
        self.context.transition_to(Menu_Quitting())

################################################################################

class Menu_Quitting(State):

    # Create the sounds for this menu.
    # sound_ones should probably not be created a second time.
    # sound_ones =  SoundObject.SoundObject(DATA_DIR, S_FILE_NAV, 6000, 600)
    # sound_quit =  SoundObject.SoundObject(DATA_DIR, S_FILE_NAV, 8600, 1300)
    sound_quit = SoundObject.SoundObject(DATA_DIR, S_FILE_PROMPT, 143750, 5250)
    gui = GUI()
    # Play sound upon entering mode.
    def entering(self):
        print("Press again to quit. Press 0 to Main Menu. Press 1 to cancel quitting.")
        self.sound_quit.play()  # Play the quitting sound.

    # Handle the four possible key inputs.
    def handle_0(self) -> None:
        print("Go back to main menu.")
        self.context.transition_to(Main_Menu())
        self.gui.main_menu() #go back to main
    def handle_1(self) -> None:
        self.context.transition_to(transition_state)
        # print("Return to Ones Menu.")
        # self.sound_ones.play()  # Play the transition sound.
        # self.context.transition_to(Menu_Ones())
    def handle_2(self) -> None:
        pass
        # print("Return to Ones Menu.")
        # self.sound_ones.play()  # Play the transition sound.
        # self.context.transition_to(Menu_Ones())
    def handle_3(self) -> None:
        pass
        # print("Return to Ones Menu.")
        # self.sound_ones.play()  # Play the transition sound.
        # self.context.transition_to(Menu_Ones())
    def handle_4(self) -> None:
        pass
    def handle_q(self) -> None:
        print("Quitting.")
        self.context.quit()
################################################################################

# This calls the 'main' function when this script is executed.
if __name__ == "__main__":
    main( )
