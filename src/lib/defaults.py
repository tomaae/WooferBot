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

defaults_root = {
    "TwitchOAUTH": "",
    "TwitchBotOAUTH": "",
    "UseChatbot": False,
    "CurrentMascot": "malamute",
    "AlignMascot": "left",
    "HostMessage": "is now hosting you.",
    "AutohostMessage": "is auto hosting you",
    "FollowMessage": "Thank you for the follow!",
    "MinBits": 0,
    "AutoShoutout": False,
    "AutoShoutoutTime": 10,
    "ShoutoutAccess": "mod",
    "GlobalVolume": 0.2,
    "NanoleafEnabled": False,
    "NanoleafIP": "",
    "NanoleafToken": "",
    "HueEnabled": False,
    "HueIP": "",
    "HueToken": "",
    "YeelightEnabled": False,
}

defaults_enabled = {
    "new_chatter": True,
    "greet": True,
    "follow": True,
    "raid": True,
    "host": True,
    "autohost": True,
    "sub": True,
    "resub": True,
    "subgift": True,
    "anonsubgift": True,
    "bits": True,
    "lurk": True,
    "shoutout": True,
}

defaults_styles = {
    "BackgroundColor": "#fefeff",
    "BorderColor": "#69656c",
    "BorderWidth": 4,
    "BorderRadius": 4,
    "BorderStrokeColor": "#ffffff",
    "TextFontFamily": "Fira Sans",
    "TextSize": 22,
    "TextWeight": 900,
    "TextColor": "#69656c",
    "HighlightTextSize": 24,
    "HighlightTextSpacing": 3,
    "HighlightTextColor": "#ca5c67",
    "HighlightTextStrokeColor": "#8e4148",
    "HighlightTextShadowColor": "#fc938f",
    "HighlightTextShadowOffset": 3,
}

defaults_messages = {
    "new_chatter": ["Oh? {sender} is new here. Welcome~ ^..^"],
    "follow": ["Oh? We have a new friend! Welcome {sender} ^..^"],
    "sub": [
        "[Hello;Hi;Hey;Hewwo;Ello] {sender}, thank you for becoming our best friend ^..^"
    ],
    "resub": [
        "[Hello;Hi;Hey;Hewwo;Ello] {sender}, thank you for being our best friend for {months} months ^..^"
    ],
    "subgift": [
        "[Hello;Hi;Hey;Hewwo;Ello] {sender}, thank you for gifting a sub to {recipient} ^..^"
    ],
    "bits": ["Yay~! {sender} just gave me {bits} treats ^..^"],
    "raid": ["Oh? Is it a raid? {sender} raid?? Did they bring lots of treats??! ^..^"],
    "host": [
        "Oh? Do I spy a host from {sender}?? Come on over and don't forget to bring treats! ^..^"
    ],
    "greet": [
        "[Hello;Hi;Hey;Hewwo;Ello] {sender}, can I have some treats please?",
        "[Hello;Hi;Hey;Hewwo;Ello] {sender}!? Are you here to pet me? Or to give me wet food? Either one is fine, just let me know! ^..^",
    ],
    "lurk": [
        "Sit back, get some snacks and enjoy you lurk {sender}. But please share some with me~ ^..^"
    ],
    "unlurk": ["Welcome back {sender}, can I have a treats now? Pretty please~ ^..^"],
    "shoutout": ["Please checkout {recipient}, they're a fantastic streamer"],
}

defaults_activities = {
    "Game": [" and they were last playing {activity}"],
    "Art": [" and they were last streaming Art"],
    "Makers and Crafting": [" and they were last streaming Makers and Crafting"],
    "Food & Drink": [" and they were last streaming Food & Drink"],
    "Music & Performing Arts": [
        " and they were last streaming Music & Performing Arts"
    ],
    "Beauty & Body Art": [" and they were last streaming Beauty & Body Art"],
    "Science & Technology": [
        " and they were last streaming Science & Technology activities"
    ],
    "Just Chatting": [" and they were last chatting"],
    "Travel & Outdoors": [" and they were last streaming Travel & Outdoors activities"],
    "Sports & Fitness": [" and they were last streaming Sports & Fitness activities"],
    "Tabletop RPGs": [" and they were last playing IRL Tabletop RPG"],
    "Special Events": [" and they were last streaming a Special Event"],
    "Talk Shows & Podcasts": [" and they were last streaming a Talk Show or Podcast"],
    "ASMR": [" and they were last streaming ASMR"],
}

defaults_scheduledmessages = {
    "Timer": 30,
    "MinLines": 0,
    "Enabled": False,
    "Command": "",
    "Image": "",
}

defaults_commands = {
    "Image": "",
    "Script": "",
    "Enabled": False,
    "ViewerOnce": False,
    "ViewerTimeout": 0,
    "GlobalTimeout": 0,
    "Aliases": [],
    "Hotkey": [],
}

defaults_custombits = {
    "From": 0,
    "To": 0,
}

defaults_customsubs = {
    "From": 0,
    "To": 0,
    "Tier": "",
}

defaults_posemapping_hue = {
    "Brightness": 50,
    "Color": "#ffffff",
}

defaults_posemapping_yeelight = {
    "Brightness": 50,
    "Color": "#ffffff",
    "Transition": True,
    "TransitionTime": 1000,
}
