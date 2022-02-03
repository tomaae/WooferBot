##########################################################################
#
#    WooferBot, an interactive BrowserSource Bot for streamers
#    Copyright (C) 2020  Tomaae
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
        if not path.isfile(self.mascotImages[action]["Image"]):
            self.log("Mascot image missing for action: {}".format(action))
            if action == "Idle":
                error = 2

            if error < 2:
                error = 1

        if action != "Idle":
            if "MouthHeight" not in self.mascotImages[action]:
                self.log(
                    "Mascot image mouth height missing for action: {}".format(action)
                )
                error = 2
            else:
                if self.mascotImages[action]["MouthHeight"] < 1:
                    self.log(
                        "Mascot image mouth height is too small for action: {}".format(
                            action
                        )
                    )
                    if error < 2:
                        error = 1

            if "Time" not in self.mascotImages[action]:
                self.log("Mascot image time missing for action: {}".format(action))
                error = 2
            else:
                if self.mascotImages[action]["Time"] < 100:
                    self.log(
                        "Mascot image time is too short for action: {}".format(action)
                    )
                    if error < 2:
                        error = 1

    #
    # Check mascot audio configuration
    #
    for action in self.mascotAudio:
        for idx, val in enumerate(self.mascotAudio[action]["Audio"]):
            if not path.isfile(self.mascotAudio[action]["Audio"][idx]):
                self.log("Mascot audio missing for action: {}".format(action))
                if error < 2:
                    error = 1

        if "Volume" not in self.mascotAudio[action]:
            self.log("Mascot audio volume missing for action: {}".format(action))
            error = 2
        else:
            if self.mascotAudio[action]["Volume"] > 1:
                self.log(
                    "Mascot audio volume value is invalid for action: {}".format(action)
                )
                if error < 2:
                    error = 1

    #
    # Check mascot other configuration
    #
    if "MascotMaxWidth" not in self.mascotStyles:
        self.log("Mascot MascotMaxWidth missing")
        error = 2
    else:
        if self.mascotStyles["MascotMaxWidth"] < 30:
            self.log("Mascot MascotMaxWidth is too small")
            if error < 2:
                error = 1

    #
    # Check default bindings
    #
    if "Image" not in self.PoseMapping["DEFAULT"]:
        self.log("Default pose mapping Image variable is missing.")
        error = 2
    else:
        if self.PoseMapping["DEFAULT"]["Image"] not in self.mascotImages:
            self.log("Default pose mapping Image reference does not exist.")
            error = 2

    if "Audio" not in self.PoseMapping["DEFAULT"]:
        self.log("Default pose mapping Audio variable is missing.")
        if error < 2:
            error = 1
    else:
        if self.PoseMapping["DEFAULT"]["Audio"] not in self.mascotAudio:
            self.log("Default pose mapping Audio reference does not exist.")
            if error < 2:
                error = 1

    #
    # Check other bindings
    #
    for action in self.PoseMapping:
        if "Image" not in self.PoseMapping[action]:
            self.log(
                "Pose mapping Image variable is missing for action: {}".format(action)
            )
            if error < 2:
                error = 1
        else:
            if self.PoseMapping[action]["Image"] not in self.mascotImages:
                self.log(
                    "Pose mapping Image reference does not exist for action: {}".format(
                        action
                    )
                )
                if error < 2:
                    error = 1

        if (
            "Audio" in self.PoseMapping[action]
            and self.PoseMapping[action]["Audio"] not in self.mascotAudio
        ):
            self.log(
                "Pose mapping Audio reference does not exist for action: {}".format(
                    action
                )
            )
            if error < 2:
                error = 1

    #
    # Check messages
    #
    for action in self.Messages:
        if not isinstance(self.Messages[action], list):
            self.log("Message is not a list: {}".format(action), error=True)

    for action in self.Enabled:
        if action == "autohost" or action == "anonsubgift":
            continue

        if action not in self.Messages:
            self.log("Message does not exist: {}".format(action), error=True)

    #
    # Check ScheduledMessages
    #
    for action in self.ScheduledMessages:
        if "Name" not in action:
            self.log("ScheduledMessages missing Name: {}".format(action), error=True)

        if not isinstance(action["Timer"], int):
            self.log(
                "ScheduledMessages Timer value is not a number: {}".format(
                    action["Name"]
                ),
                error=True,
            )

        if action["Timer"] == 0:
            self.log(
                "ScheduledMessages Timer value is 0: {}".format(action["Name"]),
                error=True,
            )

    #
    # Check Commands
    #
    for action in self.Commands:
        if not isinstance(self.Commands[action]["ViewerTimeout"], int):
            self.log(
                "Commands ViewerTimeout value is not a number: {}".format(action),
                error=True,
            )

        if not isinstance(self.Commands[action]["GlobalTimeout"], int):
            self.log(
                "Commands GlobalTimeout value is not a number: {}".format(action),
                error=True,
            )

    #
    # CustomBits
    #
    for action in self.CustomBits:
        if "Name" not in action:
            self.log("CustomBits missing Name: {}".format(action), error=True)

        if "From" not in action:
            self.log(
                "CustomBits is missing parameter From: {}".format(action["Name"]),
                error=True,
            )

        if not isinstance(action["From"], int):
            self.log(
                "CustomBits is From value is not a number: {}".format(action["Name"]),
                error=True,
            )

        if "To" not in action:
            self.log(
                "CustomBits is missing parameter From: {}".format(action["Name"]),
                error=True,
            )

        if not isinstance(action["To"], int):
            self.log(
                "CustomBits is To value is not a number: {}".format(action["Name"]),
                error=True,
            )

        if action["To"] == 0:
            self.log("CustomBits To value is 0: {}".format(action["Name"]), error=True)

        if action["From"] > action["To"]:
            self.log(
                "CustomBits From value is higher or equal to To: {}".format(
                    action["Name"]
                ),
                error=True,
            )

    #
    # CustomSubs
    #
    for action in self.CustomSubs:
        if "Name" not in action:
            self.log("CustomSubs missing Name: {}".format(action), error=True)

        if "From" not in action:
            self.log(
                "CustomSubs is missing parameter From: {}".format(action["Name"]),
                error=True,
            )

        if not isinstance(action["From"], int):
            self.log(
                "CustomSubs is From value is not a number: {}".format(action["Name"]),
                error=True,
            )

        if "To" not in action:
            self.log(
                "CustomSubs is missing parameter From: {}".format(action["Name"]),
                error=True,
            )

        if not isinstance(action["To"], int):
            self.log(
                "CustomSubs is To value is not a number: {}".format(action["Name"]),
                error=True,
            )

        if action["To"] == 0:
            self.log("CustomSubs To value is 0: {}".format(action["Name"]), error=True)

        if action["From"] > action["To"]:
            self.log(
                "CustomSubs From value is higher or equal to To: {}".format(
                    action["Name"]
                ),
                error=True,
            )

    if error == 2:
        self.log(
            "Mandatory dependencies are broken, see above.",
            error=True,
        )
