'''
Anthony Cieri
Dec. 29, 2022

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

SPACER_CHARACTER = 0
REPEAT_TIMEOUT   = 0.5
INTERNAL_COMMAND_CHAR = '~'
NULL_COMMAND = ['']

KEYBOARD_PATH = '/dev/input/by-id/usb-Razer_Razer_Tartarus_V2-if01-event-kbd'
KEYBOARD_NAME = 'Razer Razer Tartarus V2'
keyboard = evdev.InputDevice(KEYBOARD_PATH)
keyboard.grab()

'''
this is what maps all of the keys to commands
left is the keycode, right is the command it trggers
to find key codes on a random keyboard, see commented code below
commands with arguments must be made into a list
replace NULL_COMMAND with your command
'''
CODE_TO_COMMAND_MAP = {
    # 1st row
     2 : ['firefox'],               # 01
     3 : ['nautilus'],              # 02
     4 : ['gedit', '--new-window'], # 03
     5 : ['gnome-terminal'],        # 04
     6 : ['code'],                  # 05

    # 2nd row
    15 : ['inkscape'], # 06
    16 : ['discord'],  # 07
    17 : ['gimp'],     # 08
    18 : ['krita'],    # 09
    19 : ['gnome-tweaks'], # 10
    
    # 3rd row
    58 : ['firefox', 'pearson.com'],           # 11
    30 : ['firefox', 'mail.google.com'],       # 12
    31 : ['firefox', 'bright.uvic.ca'],        # 13
    32 : ['firefox', 'en.wikipedia.org'],      # 14
    33 : ['firefox', 'desmos.com/calculator'], # 15
    
    # 4th row
    42 : ['firefox', 'youtube.com'],        # 16
    44 : ['firefox', 'spotify.com'],        # 17
    45 : ['firefox', 'github.com'],         # 18
    46 : ['firefox', 'wiki.archlinux.org'], # 19

    # button
    56 : ['~close-program'], # button

    # d pad
    103 : ['amixer', 'set', 'Master', '5%+'], # up
    105 : NULL_COMMAND,                       # left
    106 : NULL_COMMAND,                       # right
    108 : ['amixer', 'set', 'Master', '5%-'], # down

    # bottom
    57 : NULL_COMMAND, # bottom (20)

    # other
     0 : NULL_COMMAND # spacer, not a physical key
}


# inital values
this_code     = SPACER_CHARACTER
last_code     = SPACER_CHARACTER
last_out_code = SPACER_CHARACTER
command       = NULL_COMMAND
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

    two would be:
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
    this_code = event.code
    command   = CODE_TO_COMMAND_MAP[this_code]

    # get time of keycode, usec is an int, it must be moved after the decimal point
    current_time = event.sec + (event.usec * (10 ** -6))

    # input filters
    last_code_spacer = last_code == SPACER_CHARACTER
    repeated         = this_code == last_out_code and (current_time - last_time) < REPEAT_TIMEOUT
    is_null          = command   == NULL_COMMAND

    # update last_code
    last_code = this_code

    if first_code:
        first_code = False
        continue

    if last_code_spacer:
        continue

    if repeated:
        continue

    if is_null:
        continue

    # The input is good
    if command[0][0] == INTERNAL_COMMAND_CHAR:
        # read commands, continue if invalid
        if command[0] == '~close-program':
            break
        else:
            continue
    else:
        last_out_code = this_code
        last_time     = current_time

    # run the command
    subprocess.Popen(command)

# shutdown
subprocess.Popen('gnome-terminal')
subprocess.Popen('gnome-terminal')
subprocess.Popen('gnome-terminal')
