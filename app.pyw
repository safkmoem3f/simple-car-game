# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 16:53:04 2020
Author: Melinda Backström
"""

import tkinter as tk
from tkinter import messagebox
import random
from game import Game
from serializer import Serializer
from PIL import Image, ImageTk, ImageFilter


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.overrideredirect(True)
        self.geometry('650x400+{}+{}'.format(int(self.winfo_screenwidth() / 3.5), int(self.winfo_screenheight() / 5)))
        font_style = 'Verdana 9 bold'

        # Logo picture
        self.__picture = ImageTk.PhotoImage(Image.open('images/simple_car_game_logo.png').resize((500, 260), Image.ANTIALIAS))
        self.logo = tk.Label(self, image = self.__picture)
        self.logo.place(relx = .52, rely = .48, anchor = tk.CENTER)

        # Start Button
        self.start_button = tk.Button(self, text = 'Start game', font = font_style, height = 2, width = 10, command = lambda: GameWindow())
        self.start_button.place(relx = .4, rely = .82, anchor = tk.CENTER)

        # Exit Button
        self.exit_button = tk.Button(self, text = 'Exit', font = font_style, height = 2, width = 10, command = lambda: self.destroy())
        self.exit_button.place(relx = .6, rely = .82, anchor = tk.CENTER)


class GameWindow(tk.Toplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.overrideredirect(True)
        self.geometry("{0}x{1}".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.focus_force()
        self.__game = Game()     
        self.game_canvas = tk.Canvas(self, width = 1000, height = 600)
        self.game_canvas.place(relx = .45, rely = .5, anchor = tk.CENTER)
        self.how_to_play = 'Move the car left and right with your arrow keys. Avoid the obtacles!\nPress ENTER to start.'

        # Logo
        self.__picture = ImageTk.PhotoImage(Image.open('images/simple_car_game_logo.png').resize((200, 100), Image.ANTIALIAS))
        self.logo = tk.Label(self, image = self.__picture)
        self.logo.place(relx = .075, rely = .09, anchor = tk.CENTER)

        # Background
        self.background_image = ImageTk.PhotoImage(Image.open('images/road.png'))
        self.background_image_blur = ImageTk.PhotoImage(Image.open('images/road.png').convert('RGB').filter(ImageFilter.BLUR))
        self.background_blur = self.game_canvas.create_image(510, 200, anchor = tk.CENTER, image = self.background_image_blur)

        # Obstacle
        self.obstacle1_image = ImageTk.PhotoImage(Image.open('images/obstacle1.png'))
        self.obstacle2_image = ImageTk.PhotoImage(Image.open('images/obstacle2.png'))
        self.obstacle3_image = ImageTk.PhotoImage(Image.open('images/obstacle3.png'))
        self.obstacles = [self.obstacle1_image, self.obstacle2_image, self.obstacle3_image]

        # Moving car
        self.car_image = ImageTk.PhotoImage(Image.open('images/car_image.png'))
        self.car_image_blurred = ImageTk.PhotoImage(Image.open('images/car_image.png').filter(ImageFilter.BLUR))
        self.car_blur = self.game_canvas.create_image(500, 500, anchor = tk.CENTER, image = self.car_image_blurred)

        # Exit button
        self.pause_game_button = tk.Button(self, text = 'Quit', font = 'Verdana 9 bold', height = 2, width = 12, command = lambda: self.quit())
        self.pause_game_button.place(relx = .89, rely = .82, anchor = tk.CENTER)

        # Information Screen
        self.info = self.game_canvas.create_text(300 , 100, fill = 'white' , font = 'Verdana 10', text = self.how_to_play)
        self.bind('<Return>', self.start)

        # High Score List
        try:
            self.__game.high_scores = Serializer('high_scores.dat', self.__game.high_scores).deserialize()
        except:
            self.__game.high_scores = {}
        self.high_score = tk.Label(self, text = 'High Scores', font = 'Verdana 20')
        self.high_score.place(relx = .89, rely = .18, anchor = tk.CENTER)
        self.high_score_list = tk.StringVar()
        self.high_score_list.set('\n'.join("{}\t\t{}".format(k, v) for k, v in self.__game.high_scores.items()))
        self.high_score_list_label = tk.Label(self, textvariable = self.high_score_list, font = 'Verdana 14')
        self.high_score_list_label.place(relx = .89, rely = .30, anchor = tk.CENTER)

    def start(self, event):
        self.game_canvas.delete(self.info)
        self.background = self.game_canvas.create_image(510, 200, anchor = tk.CENTER, image = self.background_image)
        self.car = self.game_canvas.create_image(500, 500, anchor = tk.CENTER, image = self.car_image)
        self.bind('<Left>', self.move_car)
        self.bind('<Right>', self.move_car)
        self.game_canvas.delete(self.car_blur)
        self.game_canvas.delete(self.background_blur)
        self.obstacle = self.game_canvas.create_image(random.randint(100, 900), -100, anchor = tk.CENTER, image = random.choice(self.obstacles))
        self.crash()

    def quit(self):
        new = tk.messagebox.askquestion("Quit", "New Game?")
        if new == 'yes':
            self.focus_force()
            self.start('<Return>')
            self.high_score_list.set('\n'.join("{}\t\t{}".format(k, v) for k, v in self.__game.high_scores.items()))
            self.__game.score = 0
            self.__game.speed = 50
        else:
            GameWindow.destroy(self)

    def save_score(self):
        if len(self.__game.high_scores) < 10 or self.__game.score > int(min(self.__game.high_scores.values())):
                name = tk.simpledialog.askstring(title = 'Score: {}'.format(self.__game.score), prompt = 'Enter name: ')
                if name != 'None':
                    sorted_scores = self.__game.add_score(name)
        Serializer('high_scores.dat', sorted_scores).serialize()
        self.quit()

    def move_car(self, event):
        if event.keysym == 'Left':
            self.game_canvas.move(self.car, -20, 0)
        elif event.keysym == 'Right':
            self.game_canvas.move(self.car, 20, 0)
        else:
            print('Something went wrong', event)

    def crash(self):
        if self.game_canvas.coords(self.obstacle)[1] <= 600:
            self.game_canvas.move(self.obstacle, 0, 10)
            self.move = self.game_canvas.after((self.__game.speed), self.crash)
            if self.__game.crash(self.game_canvas.coords(self.car), self.game_canvas.coords(self.obstacle)):
                self.game_canvas.after_cancel(self.move)
                self.save_score()
            else:
                self.__game.score += 1
        else:
            if self.__game.speed >= 10:
                self.game_canvas.delete(self.obstacle)
                self.__game.speed -= 1
                self.obstacle = self.game_canvas.create_image(random.randint(100, 900), -100, anchor = tk.CENTER, image = random.choice(self.obstacles))
                self.crash()
            else:
                self.__game.speed = 10
                self.game_canvas.delete(self.obstacle)
                self.obstacle = self.game_canvas.create_image(random.randint(100, 900), -100, anchor = tk.CENTER, image = random.choice(self.obstacles))
                self.crash()


if __name__ == "__main__":
    Application().mainloop()
