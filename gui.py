#!/usr/bin/python3
# -*- coding: utf-8 -*-
import gi

gi.require_version("Gtk", "3.0")
gi.require_version('Keybinder', '3.0')

from gi.repository import Gtk, Gdk, Keybinder

import subprocess

import logging
import threading
import time

from keymap import ruKeyMap, ruKeyMapSpecial

from systray import PyRussianSysTray

import xrussian
from xrussian import XRussian

ruKeyMap={**ruKeyMap, **ruKeyMapSpecial}

print("RUSSIAN ALPHABET, BLYAT: ")
ruAlphabet=list(ruKeyMap.values())

print('BLYAT LEN: ', len(ruAlphabet))
print(ruAlphabet)

xrussian_thread = None
_xrussian = None
main_thread = None

class PyRussianWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="PyRussianBLYATIFULL")
        self.h = 400
        self.w = 800

        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_size(self.w, self.h)

        self.WINDOW_TOGGLED = True
        self.VBOX_LIMIT=10

        self.xrussian = None

        #self.set_decorated(False)
        #self.set_resizable(False)
        #self.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0,0,0,1))
        #self.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("grey"))
        #self.set_opacity(0.8)

        self.box = Gtk.VBox(spacing=6)
        self.add(self.box)

        self.buttons = []

        i = 1
        j = 1

        self.bbox = [Gtk.HBox(spacing=6)]
        self.box.pack_start(self.bbox[j - 1], True, True, 0)

        for letter in ruAlphabet:
            #button_label = str(i) + ':' + letter
            button_label = letter
            
            button = Gtk.Button(label=button_label)
            button.connect("clicked", self.on_button_clicked, button_label)
            self.bbox[j-1].pack_start(button, True, True, 0)

            if i % self.VBOX_LIMIT == 0 and i < len(ruAlphabet):
                j += 1
                print("Adding VBOX, i: {}, j:{}".format(i, j))
                self.bbox.append(Gtk.HBox(spacing=3))
                self.box.pack_start(self.bbox[j - 1], True, True, 0)

            self.buttons.append(button)

            i += 1

        self.load_css()
            
    def toggle(self):
        if self.WINDOW_TOGGLED:
            self.hide()
            self.WINDOW_TOGGLED=False
        else:
            self.show()
            self.WINDOW_TOGGLED=True
        
    def on_button_clicked(self, btn, letter):
        print('You Pressed: ', letter)

        if self.xrussian is not None:
            print('Sending Russian...')
            self.xrussian.sendStringToActiveWindow(letter)

    def load_css(self):
        css = b"""
        button, GtkButton {
        font: 24px "Comic Sans";
        background-color: #222222;
        color: white;
        border: 2px white solid;
        }
        * {
        background-color: #222222;
        }
        """
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css)

        context = Gtk.StyleContext()

        screen = Gdk.Screen.get_default()

        context.add_provider_for_screen(screen, css_provider,
                                    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    def setXRussian(self, xrussian):
        self.xrussian = xrussian
        
def global_hotkey_callback(keystr, main_window):
    print ("Handling", main_window)
    print ("Event time:", Keybinder.get_current_event_time())

    main_window.toggle()
    
def global_hotkey_quit(keystr=''):
    print("Exiting...")

    import sys
    sys.exit(0)
#    stop_threads()
    
#    Gtk.main_quit()

def global_russian_blyat(keystr):
    _xrussian.toggle()

def run_gui():
    global main_thread, xrussian_thread
    
    main_window = PyRussianWindow()
    main_window.connect("destroy", lambda w: global_hotkey_quit())
    main_window.show_all()

    main_window.setXRussian(_xrussian)

    PyRussianSysTray(main_window)

    keystr = "<Ctrl><Alt>M"
    Keybinder.init()
    Keybinder.bind(keystr, global_hotkey_callback, main_window)
    print ("Press ", keystr, " to handle keybinding and quit")

    keystr = "<Ctrl><Alt>Q"
    Keybinder.bind(keystr, global_hotkey_quit)
    print ("Press ", keystr, " to quit program.")

    keystr = "<Ctrl><Alt>L"
    Keybinder.bind(keystr, global_russian_blyat)
    print ("Press ", keystr, " to enable russian autocomplention.")    

#    Gtk.main()

    main_thread = threading.Thread(name='main_window_t', target=Gtk.main, daemon=True)

    xrussian_thread = threading.Thread(name='xrussian_t', target=run_xrussian, args=(), daemon=True)

    main_thread.start()
    xrussian_thread.start()
    
    main_thread.join()
    xrussian_thread.join()
    
def stop_threads():
    global _xrussian, xrussian_thread, main_thread
    print("Stopping Threads")

    _xrussian.stopRunning()
    xrussian_thread.join()
    
    Gtk.main_quit()
    main_thread.join()

def run_xrussian():
    global _xrussian
    
    print("Launching XRussian")
    _xrussian.mainLoop()
            
if __name__ == '__main__':
    print("Starting XRussian Thread")

    _xrussian = XRussian()

    #xrussian_thread = threading.Thread(name='xrussian_t', target=run_xrussian, args=(_xrussian), daemon=True)
    #xrussian_thread.start()
    #xrussian_thread.join()
    
    print("XRussian Toggled IS: ", str(_xrussian.TOGGLED))
    # main_thread = threading.Thread(name='main_window_t', target=run_gui, daemon=True)
    # main_thread.start()
    # main_thread.join()

    run_gui()

    
