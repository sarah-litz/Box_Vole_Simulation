

''' function for displaying a countdown for some event in the terminal '''

import time 
import sys


def countdown_for_current_event(timeinterval, event): 
    print("\r")
    while timeinterval:
        mins, secs = divmod(timeinterval, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        sys.stdout.write(f"\r{timer} remaining to {event}")
        time.sleep(1)
        timeinterval -= 1
    print('\n')

def countdown_until_event(timeinterval, event): 
    print("\r")
    while timeinterval:
        mins, secs = divmod(timeinterval, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        sys.stdout.write(f"\r{timer} until {event}  ")
        time.sleep(1)
        timeinterval -= 1
    print('\n')