#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import time
import threading
import gobject
from gol import GameOfLife


WIDTH = 50
HEIGHT = 50

BLACK = gtk.gdk.color_parse("black")
WHITE = gtk.gdk.color_parse("white")


class GameOfLifeGUI(object):
    def __init__(self, gol_obj, width=20, height=20):
        self.gol_obj = gol_obj
        self.width = width
        self.height = height

        self.is_start = False
        self.create_thread()

        self.set_window()

    def create_thread(self):
        self.update_thread = threading.Thread(target=self.next_step)
        self.update_thread.daemon = True
        gtk.threads_init()

    def set_window(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", gtk.main_quit)

        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_title("Game of Life")
        self.window.set_size_request(800, 600)

        self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('gray'))

    def create_main_buttons(self):
        self.button_hbox = gtk.HBox()

        self.start_button = gtk.Button("Start")
        self.start_button.connect("clicked", self.start_game)
        self.button_hbox.pack_start(self.start_button)

        self.reset_button = gtk.Button("Reset")
        self.reset_button.connect("clicked", self.reset_game)
        self.button_hbox.pack_start(self.reset_button)

        self.halign = gtk.Alignment(0.5, 1, 0, 0)
        self.halign.add(self.button_hbox)

    def create_cells(self):
        self.cell_vbox = gtk.VBox()
        self.cells = []

        for row in range(self.height):
            self.cell_hbox = gtk.HBox(True, 0)
            cell_column = []

            for column in range(self.width):
                self.button = ColoredButton()
                self.button.set_size_request(5, 5)
                self.button.change_color(WHITE)
                self.button.connect("button-release-event", self.colorize_cell)

                cell_column.append(self.button)
                self.cell_hbox.pack_start(self.button, True, True)

            self.cells.append(cell_column)
            self.cell_vbox.pack_start(self.cell_hbox, True, True)

    def create_game(self):
        self.create_main_buttons()
        self.create_cells()

        self.automata_layout = gtk.VBox()
        self.automata_layout.pack_start(self.halign, False, 3)
        self.automata_layout.pack_start(self.cell_vbox)

        self.window.add(self.automata_layout)
        self.window.show_all()

    def colorize_cell(self, widget, event=None):
        current_color = widget.get_style().bg[gtk.STATE_NORMAL]

        if current_color != BLACK:
            widget.change_color(BLACK)
        else:
            widget.change_color(WHITE)

    def start_game(self, widget=None):
        self.initialize_world()
        self.is_start = not self.is_start

        if not self.update_thread.isAlive():
            self.update_thread.start()

    def next_step(self):
        while True:
            if self.is_start:
                self.gol_obj.change_world(self.gol_obj.next_generation())
                self.update_world(self.gol_obj.world)
                time.sleep(0.05)

    def reset_game(self, widget):
        self.is_start = False

        for row in range(len(self.cells)):
            for column in range(len(self.cells[0])):
                self.cells[row][column].change_color(WHITE)

    def initialize_world(self):
        current_world = set()

        for row in range(len(self.cells)):
            for column in range(len(self.cells[0])):
                cell_style = self.cells[row][column].get_style()
                cell_color = cell_style.bg[gtk.STATE_NORMAL]

                if cell_color == BLACK:
                    current_world.add((row, column))

        self.gol_obj.change_world(current_world)

    def update_world(self, world):
        for row in range(len(self.cells)):
            for column in range(len(self.cells[0])):
                if (row, column) in world:
                    self.cells[row][column].change_color(BLACK)
                else:
                    self.cells[row][column].change_color(WHITE)
        self.window.show_all()

    def run(self):
        self.create_game()
        gtk.main()


class ColoredButton(gtk.EventBox):
    def __init__(self, widget=gtk.Label()):
        super(ColoredButton, self).__init__()
        self.widget = widget

        self.vbox = gtk.VBox(homogeneous=False, spacing=0)
        self.hbox = gtk.HBox(homogeneous=False, spacing=0)

        self.hbox.pack_start(self.vbox, expand=True, fill=False)
        self.vbox.pack_start(self.widget, expand=True, fill=False)

        self.frame = gtk.Frame()
        self.frame.add(self.hbox)

        self.add(self.frame)

        self.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.add_events(gtk.gdk.ENTER_NOTIFY_MASK)
        self.add_events(gtk.gdk.LEAVE_NOTIFY_MASK)

        self.set_can_focus(True)

        self.widget.set_alignment(xalign=0.5, yalign=0.5)

    def show(self):
        super(ColoredButton, self).show()
        self.hbox.show()
        self.vbox.show()
        self.frame.show()
        self.widget.show()

    def set_label(self, label):
        self.set_text(label)

    def set_text(self, text):
        self.widget.set_text(text)

    def change_color(self, color, state=gtk.STATE_NORMAL):
        if color is not None:
            current_color = self.style.bg[state]
            if color.red != current_color.red or \
               color.green != current_color.green or \
               color.blue != current_color.blue:
                self.modify_bg(state, color)

    def change_text_color(self, color, state=gtk.STATE_NORMAL):
        if color is not None:
            current_color = self.style.bg[state]
            if color.red != current_color.red or \
               color.green != current_color.green or \
               color.blue != current_color.blue:
                self.widget.modify_fg(gtk.STATE_NORMAL, color)


if __name__ == "__main__":
    gobject.threads_init()
    gol_obj = GameOfLife(WIDTH, HEIGHT)
    app = GameOfLifeGUI(gol_obj, WIDTH, HEIGHT)
    app.run()
