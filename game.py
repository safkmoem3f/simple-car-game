# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:56:33 2020
Author: Melinda Backström
"""

class Game:
    
    def __init__(self):
        self.speed = 50
        self.score = 0
        self.high_scores = {}
    
    def crash(self, car, obstacle):
        x = int(car[0] - obstacle[0])
        y = int(car[1] - obstacle[1])
        if x <= 70 and x >= -70 and y <= 200 and y >= -200:
            return True
        else:
            return False
       
    def add_score(self, name):
        if name not in self.high_scores:
            self.high_scores[name] = self.score
        elif name in self.high_scores.keys() and self.score > self.high_scores.get(name):
            self.high_scores[name] = self.score
        sorted_scores = {k : v for k, v in sorted(self.high_scores.items(), key = lambda item: item[1], reverse = True)}
        return sorted_scores