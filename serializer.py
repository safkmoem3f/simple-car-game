# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:56:33 2020
Author: Melinda Backström
"""

import pickle

class Serializer:

    def __init__(self, filename, item):
        self.filename = filename
        self.item = item

    def deserialize(self):
        file = None
        try:
            file = open('data/' + self.filename, 'br')
            item = pickle.load(file)
            if item != None and isinstance(item, type(self.item)):
                self.item = item
        except IOError as error:
            print(error)
        finally:
            if file:
                file.close()
        return self.item

    def serialize(self):
        file = None
        try:
            file = open('data/' + self.filename, 'bw+')
            pickle.dump(self.item, file)
        except IOError as error:
            print(error)
        finally:
            if file:
                file.close()
