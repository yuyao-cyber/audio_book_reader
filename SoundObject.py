'''
SoundObject class.
A.Hornof (ajh) - 11-5-2021, 11-8-2021

This file is part of a pushbutton-input audio-ouput system created by
Anthony Hornof for CIS 443/543 User Interfaces.
Uses Python 3.10 and pygame 2.0.2

Defines a class of SoundObject objects, each of which is prepared to:
  (a) load a soundfile from disk;
  (b) start playing it from a specific location; and
  (c) set a duration after which it should stop playing.

The times are in ms.

SoundObject - file location and name, start time, duration
    play() - stops whatever is currently playing, clears the queue, and adds
             this to the queue. The sound will get played immediately.
    chain() - Adds this sound to the queue of currently playing objects. It
              will get played when all the objects ahead of it in the queue are
              played.

Sources for ideas:
eventlist.py from
https://www.pygame.org/docs/ref/examples.html#pygame.examples.eventlist.main
'''

import pygame # Currently using 2.0.2
import os

# The following should accompany this file, and were created by ajh.
import SoundObjChain

# Global module variables
SOUND_OBJECT_CHAIN = None

################################################################################
class SoundObject:
    def __init__(self, data_dir_in, filename_in, start_in, duration_in):
        # Pseudo-private member variables.
        # Save all these settings for later playback.
        self._data_dir = data_dir_in
        self._filename = filename_in
        self._start_time = start_in
        self._duration = duration_in
        self._offset = 0
    def get_curpos(self):
        # gets the current position of the e-reader
        curpos = ((pygame.mixer.music.get_pos()/1000) + self._offset)
        return curpos*1000

    def set_pos(self, pos):
        # because the interrupts reset the get_pos function, _lastplayed must be used for moving through the system
        self._offset = (pos/1000)
    ############################################################################
    # Getter for duration.
    def get_duration(self):
        return( self._duration )

    ############################################################################
    # Play a SoundObject
    # SHOULD be used within a menu.
    def play(self):
        # global SOUND_OBJECT_CHAIN

        # Stop the currently-playing sound, and clear the queue of sounds.
        get_SoundObjChain().stop_playing()

         # Add this SoundObject to the chain. This will cause the SoundObject to
        #   be loaded from disk, and the SoundObject to start playing.
        get_SoundObjChain().append_SoundObject( self )


    ############################################################################
    # Chain a SoundObject
    # SHOULD be used within a menu.
    # Same as play(), but adds to the chain of sounds without stopping what is
    #   currently playing.
    def chain(self):

        # Add this SoundObject to the chain. When items currently in the chain
        #   are done playing, this SoundObject will be loaded from disk, and
        #   it will start playing.
        get_SoundObjChain().append_SoundObject( self )


    ############################################################################
    # Add a sound to be played after the current sound being played.
    def load_sound(self, data_dir, file_name):

        # Load the soundfile from disk. For better or worse, this must be done
        #   every time a sound is played. See long comment at the top of the file.

        # Set up path to subdirectory (from Pete Shinners)
        main_dir = os.path.split(os.path.abspath(__file__))[0]
        data_dir = os.path.join(main_dir, data_dir)

        # Join the path and filename, cross-platform.
        filename = os.path.join(data_dir, file_name)

        # Create the pygame.mixer.Sound object.
        # Try to load the sound file. Exit gracefully if it fails.
        try:
            pygame.mixer.music.load(filename)

        except pygame.error:
            print("Cannot load sound file:", filename)
            raise SystemExit(str(pygame.get_error()))


    ############################################################################
    # Play a sound based on the member variables.
    # Should NOT be used within a menu. Should only by used by SoundObjChain.
    # Permits SoundObject filename details to remain hidden from SoundObjChain.
    def play_from_inside_SoundObjChain( self ):

        # Load the soundfile from disk.
        self.load_sound(self._data_dir, self._filename)

        # Play the sound from the specified start time. Convert from ms to s.
        pygame.mixer.music.play(0, self._start_time/1000)

################################################################################
# set_SoundObjChain () - Receive the one SoundObjChain that the program will
#   be using. The play() and chain() methods above will be using it.
def set_SoundObjChain (chain_in):
    global SOUND_OBJECT_CHAIN # Gain access to the global module variable.
    SOUND_OBJECT_CHAIN = chain_in

################################################################################
# get_SoundObjChain () - Return the SoundObjChain.
def get_SoundObjChain ():
    global SOUND_OBJECT_CHAIN # Gain access to the globalmodule variable.
    return SOUND_OBJECT_CHAIN

################################################################################
# dprint() - debug print. An easy way to turn on/off print statements.
def dprint(str):
    if (False): # True prints. False doesn't print.
        print(str)
