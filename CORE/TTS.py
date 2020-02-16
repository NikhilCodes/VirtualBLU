#!/usr/bin/env python3
#
# Author : Nikhil Nayak (nikhil.nixel@gmail.com)
# Usage  : .py
# 

import os

if os.name == 'nt':
    from win32com.client import constants as _constants
    from win32com.client import gencache
    import win32com.client
    import pythoncom
    import time
    import sys
    import _thread

    # gencache.EnsureModule('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 0, 5, 0)

    _voice = win32com.client.Dispatch("SAPI.SpVoice")


    def say(phrase, mode=1):
        _voice.Speak(phrase, mode)


    def stop_talking():
        _voice.Speak("", 3)
else:
    def say(phrase, mode=1):
        pass


    def stop_talking():
        pass

if __name__ == '__main__':
    say('Hello World!')
    print('Speaking')
