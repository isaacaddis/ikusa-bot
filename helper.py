'''
    Miscellaneous utility functions and constants
'''
import random

class Helper():
    def __init__(self):
        self.GREETINGS = ["Checking in :wave:!", "Greetings :cartwheel:!", "It's me again :information_desk_person:"]
    def get_random_greeting(self):
        return random.choice(self.GREETINGS)


