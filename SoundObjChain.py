################################################################################
# SoundObjChain.py
# Written by Anthony Hornof - 11-3-2021
# See https://www.pygame.org/docs/
################################################################################

'''
SoundObjChain chains together (queues) SoundObjects.
Attributions are provided in SoundObject.py

This file is part of a pushbutton-input audio-ouput system created by
Anthony Hornof in the CIS 443/543 User Interfaces class that he is teaching.

If you tell pygame in one line of code to play sound one, and in the next line
of code to play sound two, it will only play sound two. It will not wait for
sound one to finish playing. SoundObjChain is thus needed to let sound one
finish playing before starting sound two.

SoundObjChain includes a list of all SoundObjects to be played, as well as
the duration of the currently playing SoundObject ( or -1 if none is playing).

Functionality:

SoundObjChain - a list of SoundObjects to be played.
    Even if just one sound object is played, it still gets put into a chain.
    A chain only gets created if no sound is currently playing.

SoundObjChain.play_until_empty() - gets called multiple times a second in the
  main event loop, and moves through the chain of sounds, stopping each when it
  is done playing, and moving to the next sound if there is one in the chain.

'''

################################################################################

import pygame # Currently using 2.0.2

# The following should accompany this file, and were created by ajh.
import SoundObject

################################################################################
# SoundObjChain class. Defines a SoundObjChain object.
# Only one SoundObjChain object should be created when the program is run.
################################################################################

class SoundObjChain:

    def __init__(self):
        # Pseudo-private member variables.
        self._SoundObject_list = list( )   # The list of SoundObjects playing.
        # The duration of the first SoundObject in the list (currently playing).
        self._target_duration = -1

    ################################################################################
    # play_until_empty( )
    # Gets called many times a second in the main event loop.
    # If nothing is playing, but there is something in the SoundObject list, play
    #   the next item in the list.
    # If something is playing, and there is time left in its duration, do nothing.
    #   Just let it keep playing.

    def play_until_empty(self):

        # If no sounds are currently playing...
        if ( self._target_duration == -1 ):

            # If there there are sounds left to play...
            if ( len ( self._SoundObject_list ) > 0 ):

                # Get the next SoundObject in the list, removing it from the list.
                new_object_to_play = self._SoundObject_list.pop(0)
                # Get the sound's duration.
                self._target_duration = new_object_to_play.get_duration( )
                # Play it.
                new_object_to_play.play_from_inside_SoundObjChain( )

        # Else there IS a sound currently playing... ( self._target_duration != -1 )
        else:

            # If the sound ran past its duration...
            if ( pygame.mixer.music.get_pos() > self._target_duration ):

                # Stop playing the current sound.
                pygame.mixer.music.stop()

                # Indicate that the current sound is no longer playing.
                self._target_duration = -1


    ################################################################################
    # append_SoundObject( )
    # Add a new add_SoundObject to the end of the SoundObject list.

    def append_SoundObject( self, new_SoundObject ):
        self._SoundObject_list.append( new_SoundObject )

    ################################################################################
    # stop_playing( )
    # Stop the currently playing sound, and clear the queue.

    def stop_playing( self ):
        pygame.mixer.music.stop()
        self._target_duration = -1
        self._SoundObject_list.clear( )

################################################################################
# dprint() - debug print. An easy way to turn on/off print statements.
def dprint(str):
    if (False): # True prints. False doesn't print.
        print(str)
