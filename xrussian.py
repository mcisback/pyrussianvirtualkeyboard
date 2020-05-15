#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Xlib.display import Display
from Xlib import X, protocol
from Xlib.ext import record
from Xlib.protocol import rq
from Xlib import XK

import subprocess
import time

from keymap import ruKeyMap, ruKeyMapSpecial

#disp = None

#toggle = False
#èòàèùì

#def getCapslockStatus():
#    return (subprocess.check_output("xset -q | grep Caps | awk '{print $4}' | tr -d '\n'", shell=True) == 'on')

#def getNumLockStatus():
#    return (subprocess.check_output("xset -q | grep Caps | awk '{print $8}' | tr -d '\n'", shell=True) == 'on')

class XRussian():

    def __init__(self):
        
        self.inputBuffer = ''
        self.specialMode = False

        # get current display
        self.disp = Display()
        self.root = self.disp.screen().root

        self.RUNNING = True
        self.TOGGLED = True

        # Monitor keypress and button press
        self.ctx = self.disp.record_create_context(
            0,
            [record.AllClients],
            [{
                'core_requests': (0, 0),
                'core_replies': (0, 0),
                'ext_requests': (0, 0, 0, 0),
                'ext_replies': (0, 0, 0, 0),
                'delivered_events': (0, 0),
                'device_events': (X.KeyReleaseMask, X.ButtonReleaseMask),
                'errors': (0, 0),
                'client_started': False,
                'client_died': False,
            }]
        )
    def setSpecialMode(self, specialMode):
        self.specialMode = bool(specialMode)

    def sendStringToActiveWindow(self, string):
        # Send Key Using xdotool
        subprocess.call(["xdotool", "type", string])
        
    def sendRussian(self, key='', _specialMode=False):
        _ruKeyMap = ruKeyMap

        if _specialMode:
            _ruKeyMap = ruKeyMapSpecial
        
        if key in _ruKeyMap:
            #    print('Sending {}'.format(ruKeyMap[key]))
            self.sendMappedKeyToActiveWindow(_ruKeyMap[key], _specialMode)
            #else:
            #    print('Keycode {} not mapped'.format(key))

    def sendMappedKeyToActiveWindow(self, string, _specialMode=False):
        #print("Using xdotool")

        # Send Backspace
        self.sendBackspace()

        if _specialMode:
            self.sendBackspace()

        # Send Key After
        self.sendStringToActiveWindow(string)

    def sendBackspace(self):
        subprocess.call(["xdotool", "key", "BackSpace"])
    
    def handler(self, reply):
        """ This function is called when a xlib event is fired """
        data = reply.data

        if self.TOGGLED == False:
            return

        while len(data):
            
            event, data = rq.EventField(None).parse_binary_value(data, self.disp.display, None, None)
            keycode = event.detail
        
            if event.type == X.KeyRelease:

                window = Display().get_input_focus().focus

                keysym = self.disp.keycode_to_keysym(keycode, 0)
                keystr = XK.keysym_to_string(keysym)

                # KEYCODE IS FOUND USERING event.detail
                print('KC: {}, KS: {}, KS: {}'.format(keycode, keysym, keystr))

                if str(keystr) == 'h' and self.specialMode == False:
                    print('Turing SpecialMode ON')

                    self.sendBackspace()
                
                    self.specialMode = True
                    continue

                if self.specialMode:
                    print('SpecialMode is ON')

                    if str(keystr).isalnum():
                        if str(keystr) != 'None':
                            self.inputBuffer += str(keystr)
                
                        if len(self.inputBuffer) == 2:
                            print('InputBuffer: ' + self.inputBuffer)
                    
                            self.sendRussian(self.inputBuffer, True)
                        
                            self.inputBuffer = ''
                            self.specialMode = False

                            print('Turning SpecialMode OFF')
                else:
                    # SEND MOTHER RUSSIA BLYAT!
                    self.sendRussian(keystr, False)

                print("Key: ", keystr)
                print('InputBuffer: ' + self.inputBuffer)
                print('SpecialMode: ', str(self.specialMode))

    def nextEvent(self):
        return self.root.display.next_event()

    def mainLoop(self):
        self.disp.record_enable_context(self.ctx, self.handler)
        self.disp.record_free_context(self.ctx)

        self.root.grab_keyboard(
            owner_events = True,
            pointer_mode = X.GrabModeAsync,
            keyboard_mode = X.GrabModeAsync,
            time = X.CurrentTime
        )
        while self.RUNNING:
            # Infinite wait, doesn't do anything as no events are grabbed
            print('XRussian TOGGLED is: ', str(self.TOGGLED))
            event = self.nextEvent()

    def stopRunning(self):
        self.RUNNING = False
    def toggle(self):
        self.TOGGLED = not self.TOGGLED
        print("XRussian Toggled IS: ", str(self.TOGGLED))

#if __name__ == '__main__':
#    xrussian = XRussian()
#    xrussian.mainLoop()
