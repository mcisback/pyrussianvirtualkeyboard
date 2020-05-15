#!/usr/bin/python3
# -*- coding: utf-8 -*-
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

class PyRussianSysTray():
    def __init__(self, main_window):
        self.main_window = main_window
        
        self.icon = Gtk.StatusIcon()
        self.icon.set_from_file('img/slav-icon.png')
        self.icon.connect('popup-menu', self.on_right_click)
        self.icon.connect('activate', self.on_left_click)

    def make_menu(self, event_button, event_time, data=None):
        self.menu = Gtk.Menu()
        self.open_item = Gtk.MenuItem("Open Keyboard")
        self.close_item = Gtk.MenuItem("Quit")
        
        #Append the menu items  
        self.menu.append(self.open_item)
        self.menu.append(self.close_item)
        #add callbacks
        self.open_item.connect_object("activate", self.open_app, "Open Keyboard")
        self.close_item.connect_object("activate", self.close_app, "Quit")
        #Show the menu items
        self.open_item.show()
        self.close_item.show()
        
        #Popup the menu
        self.menu.popup(None, None, None, None, event_button, event_time)
            
    def on_right_click(self, data, event_button, event_time):
        self.make_menu(event_button, event_time)
        print("Status Icon Right Clicked")
        
    def on_left_click(self, event):
        print("Status Icon Left Clicked")
        self.open_app()
        
    def open_app(self, event=None):
        self.main_window.toggle()

    def close_app(self, event=None):
        Gtk.main_quit()
                
