'''
Anthony Cieri
Dec. 27, 2022

Python script that takes Razer Tartarus V2 key inputs and runs commands
This can work for any keyboard with some tweaks and experimentation


This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>. 
'''

import evdev
import subprocess

# keyboard_path = evdev.InputDevice('/dev/input/by-id/usb-Razer_Razer_Tartarus_V2-if01-event-kbd')
KEYBOARD_PATH = '/dev/input/by-id/usb-Razer_Razer_Tartarus_V2-if01-event-kbd'
KEYBOARD_NAME = 'Razer Razer Tartarus V2'
keyboard = evdev.InputDevice(KEYBOARD_PATH)
keyboard.grab()

# this is what maps all of the keys to commands
# left is the keycode, right is the command it trggers
# to find key codes on a random keyboard, see commented code below
# commands with arguments must be made into a list
code_to_command_map = {
    # 1st row
     2 : 'firefox',         # 01
     3 : 'nautilus',        # 02
     4 : ['gedit', '--new-window'], # 03
     5 : 'gnome-terminal',  # 04
     6 : 'code',            # 05

    # 2nd row
    15 : '',                # 06
    16 : '',                # 07
    17 : '',                # 08
    18 : '',                # 09
    19 : '',                # 10
    
    # 3rd row
    58 : '',                # 11
    30 : '',                # 12
    31 : '',                # 13
    32 : '',                # 14
    33 : '',                # 15
    
    # 4th row
    42 : '',                # 16
    44 : '',                # 17
    45 : '',                # 18
    46 : '',                # 19

    # button
    56 : '',                # button

    # d pad
    103 : ['amixer', 'set', 'Master', '5%+'], # up
    105 : '',               # left
    106 : '',               # right
    108 : ['amixer', 'set', 'Master', '5%-'], # down

    # bottom
    57 : '',                # bottom

    # other
     0 : ''                 # spacer, not a physical key
}


SPACER_CHARACTER = 0
REPEAT_TIMEOUT   = 0.5

code          = SPACER_CHARACTER
last_code     = SPACER_CHARACTER
last_out_code = SPACER_CHARACTER
last_time     = 0.0
first_code    = True

for event in keyboard.read_loop():
    '''
    ignore keys if they are spacers
    the last code is a spacer (happens when a key is held down and other
    unwanted times)
    or if a valid code is repeated under the time interval

    structure of a key press seemed to be:
    4
    code
    0

    2 would be:
    4
    code 1
    0
    4
    code 2
    0

    this is why the program filters out codes if last_code == SPACER_CHARACTER
    this may not be necessary for every keyboard
    '''

    # get keycode
    code = event.code

    # get time of keycode, usec is an int, it must be moved after the decimal point
    current_time = event.sec + (event.usec * (10 ** -6))


    code_is_spacer      = code      == SPACER_CHARACTER
    last_code_is_spacer = last_code == SPACER_CHARACTER

    if code_is_spacer or last_code_is_spacer or first_code:
        # I cannot come up with a more elegant way to do this
        first_code = False
        command = ''
    elif ((current_time - last_time) > REPEAT_TIMEOUT) or (code != last_out_code):
        last_out_code = code
        last_time = current_time
        command = code_to_command_map[code]

        # this line will print out the keycode
        # uncomment for keymapping
        # print(code)

    last_code = code

    # this code runs the commands
    # comment out for keymapping
    if command != '':
        # a subprocess is created so the script can continue to run even if
        # a program that uses the terminal is opened
        subprocess.Popen(command)
