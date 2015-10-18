#!/usr/bin/env python3
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
Gst.init(None)

import time, threading, urllib.request, urllib.error, json, os

from gi.repository import Notify
Notify.init("Maximum")

#import curses
#stdscr = curses.initscr()
#curses.noecho(); curses.cbreak(); stdscr.keypad(1); curses.curs_set(0)

def print_t(delay):
    global info
    global e
    current_t = None
    fetched_t = None
    while True:
        try:
            req = urllib.request.urlopen('http://maximum.ru/currenttrack.aspx?station=maximum')
            data = json.loads(req.readall().decode('utf-8'))
            fetched_t = data["Current"]["Artist"] + " - " + data["Current"]["Song"]
        except urllib.error.URLError as e:
            print(e.reason)
            os._exit(1)
        except urllib.error.HTTPError as e:
            print(e)
            print(e.args)
            os._exit(1)
            
        if fetched_t == current_t:
            pass
        else:
            current_t = fetched_t
            info.update("Maximum", current_t, None)
            info.show()

        time.sleep(delay)

#def show_notification(track):
#    bubble.update("Playing", track)
#    bubble.show

def play():
    music_uri = 'http://maximum.fmtuner.ru'
    player = Gst.ElementFactory.make('playbin', None)
    player.set_property('uri', music_uri)
    player.set_state(Gst.State.PLAYING)

info = Notify.Notification.new("Maximum","Sang", None)
t = threading.Thread(target=print_t, args=(3,))
t.daemon = True
t.start()
#_thread.start_new_thread(print_t, (3,))
play()

#stdscr.addstr(20,2,"Hit 'q' to quit")
#stdscr.move(0,20)
#key = ''
#while key != ord('q'):
#    key = stdscr.getch()
#curses.endwin()


#while True:
#print ('Press enter to quit...')
time.sleep(1)
input('Press Enter to quit')
info.close()
del t
os._exit(0)
