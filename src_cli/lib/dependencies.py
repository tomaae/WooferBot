##########################################################################
#
#    WooferBot, an interactive BrowserSource Bot for streamers
#    Copyright (C) 2019  Tomaae
#    (https://wooferbot.com/)
#
#    This file is part of WooferBot.
#
#    WooferBot is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
##########################################################################

from os import path
from sys import exit


# ---------------------------
#   CheckSettingsDependencies
# ---------------------------
def CheckSettingsDependencies(self):
    error = 0

    #
    # Check mascot images configuration
    #
    for action in self.mascotImages:
        if not path.isfile(self.mascotImages[action]['Image']):
            print("Mascot image missing for action: {}".format(action))
            if action == "Idle":
                error = 2

            if error < 2:
                error = 1

        if action != 'Idle':
            if 'MouthHeight' not in self.mascotImages[action]:
                print("Mascot image mouth height missing for action: {}".format(action))
                error = 2
            else:
                if self.mascotImages[action]['MouthHeight'] < 1:
                    print("Mascot image mouth height is too small for action: {}".format(action))
                    if error < 2:
                        error = 1

            if 'Time' not in self.mascotImages[action]:
                print("Mascot image time missing for action: {}".format(action))
                error = 2
            else:
                if self.mascotImages[action]['Time'] < 100:
                    print("Mascot image time is too short for action: {}".format(action))
                    if error < 2:
                        error = 1

    #
    # Check mascot audio configuration
    #
    for action in self.mascotAudio:
        for idx, val in enumerate(self.mascotAudio[action]['Audio']):
            if not path.isfile(self.mascotAudio[action]['Audio'][idx]):
                print("Mascot audio missing for action: {}".format(action))
                if error < 2:
                    error = 1

        if 'Volume' not in self.mascotAudio[action]:
            print("Mascot audio volume missing for action: {}".format(action))
            error = 2
        else:
            if self.mascotAudio[action]['Volume'] > 1:
                print("Mascot audio volume value is invalid for action: {}".format(action))
                if error < 2:
                    error = 1

    #
    # Check mascot other configuration
    #
    if 'MascotMaxWidth' not in self.mascotStyles:
        print("Mascot MascotMaxWidth missing")
        error = 2
    else:
        if self.mascotStyles['MascotMaxWidth'] < 30:
            print("Mascot MascotMaxWidth is too small")
            if error < 2:
                error = 1

    #
    # Check default bindings
    #
    if 'Image' not in self.PoseMapping['DEFAULT']:
        print("Default pose mapping Image variable is missing.")
        error = 2
    else:
        if self.PoseMapping['DEFAULT']['Image'] not in self.mascotImages:
            print("Default pose mapping Image reference does not exist.")
            error = 2

    if 'Audio' not in self.PoseMapping['DEFAULT']:
        print("Default pose mapping Audio variable is missing.")
        if error < 2:
            error = 1
    else:
        if self.PoseMapping['DEFAULT']['Audio'] not in self.mascotAudio:
            print("Default pose mapping Audio reference does not exist.")
            if error < 2:
                error = 1

    #
    # Check other bindings
    #
    for action in self.PoseMapping:
        if 'Image' not in self.PoseMapping[action]:
            print("Pose mapping Image variable is missing for action: {}".format(action))
            if error < 2:
                error = 1
        else:
            if self.PoseMapping[action]['Image'] not in self.mascotImages:
                print("Pose mapping Image reference does not exist for action: {}".format(action))
                if error < 2:
                    error = 1

        if 'Audio' in self.PoseMapping[action] and self.PoseMapping[action]['Audio'] not in self.mascotAudio:
            print("Pose mapping Audio reference does not exist for action: {}".format(action))
            if error < 2:
                error = 1

    #
    # Check messages
    #
    for action in self.Messages:
        if not isinstance(self.Messages[action], list):
            print("Message is not a list: {}".format(action))
            exit(1)

    for action in self.Enabled:
        if action == 'autohost' or action == 'anonsubgift':
            continue

        if action not in self.Messages:
            print("Message does not exist: {}".format(action))
            exit(1)

    #
    # Check ScheduledMessages
    #
    for action in self.ScheduledMessages:
        if 'Name' not in action:
            print("ScheduledMessages missing Name: {}".format(action))
            exit(1)

        if not isinstance(action['Timer'], int):
            print("ScheduledMessages Timer value is not a number: {}".format(action['Name']))
            exit(1)

        if action['Timer'] == 0:
            print("ScheduledMessages Timer value is 0: {}".format(action['Name']))
            exit(1)

    #
    # Check Commands
    #
    for action in self.Commands:
        if not isinstance(self.Commands[action]['ViewerTimeout'], int):
            print("Commands ViewerTimeout value is not a number: {}".format(action))
            exit(1)

        if not isinstance(self.Commands[action]['GlobalTimeout'], int):
            print("Commands GlobalTimeout value is not a number: {}".format(action))
            exit(1)

    #
    # CustomBits
    #
    for action in self.CustomBits:
        if 'Name' not in action:
            print("CustomBits missing Name: {}".format(action))
            exit(1)

        if 'From' not in action:
            print("CustomBits is missing parameter From: {}".format(action['Name']))
            exit(1)

        if not isinstance(action['From'], int):
            print("CustomBits is From value is not a number: {}".format(action['Name']))
            exit(1)

        if 'To' not in action:
            print("CustomBits is missing parameter From: {}".format(action['Name']))
            exit(1)

        if not isinstance(action['To'], int):
            print("CustomBits is To value is not a number: {}".format(action['Name']))
            exit(1)

        if action['To'] == 0:
            print("CustomBits To value is 0: {}".format(action['Name']))
            exit(1)

        if action['From'] > action['To']:
            print("CustomBits From value is higher or equal to To: {}".format(action['Name']))
            exit(1)

    #
    # CustomSubs
    #
    for action in self.CustomSubs:
        if 'Name' not in action:
            print("CustomSubs missing Name: {}".format(action))
            exit(1)

        if 'From' not in action:
            print("CustomSubs is missing parameter From: {}".format(action['Name']))
            exit(1)

        if not isinstance(action['From'], int):
            print("CustomSubs is From value is not a number: {}".format(action['Name']))
            exit(1)

        if 'To' not in action:
            print("CustomSubs is missing parameter From: {}".format(action['Name']))
            exit(1)

        if not isinstance(action['To'], int):
            print("CustomSubs is To value is not a number: {}".format(action['Name']))
            exit(1)

        if action['To'] == 0:
            print("CustomSubs To value is 0: {}".format(action['Name']))
            exit(1)

        if action['From'] > action['To']:
            print("CustomSubs From value is higher or equal to To: {}".format(action['Name']))
            exit(1)

    if error == 2:
        print("Mandatory dependencies are broken, see above.")
        exit(1)
