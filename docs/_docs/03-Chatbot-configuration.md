---
name: Chatbot configuration
anchor: chatbot-configuration
toc: 
 - name: Enable chatbot
   anchor: enable-chatbot
---
This section explains how to enable and setup chatbot.

### Enable chatbot
If you want to have WooferBot messages to appear in your chat, you have to enable chatbot.
<span class="icon idea">Note: You do not have to use special account for chatbot. If you dont, your main account will be used for chat messages.</span>

```
{
    "TwitchBotChannel": "",
    "TwitchBotOAUTH": "",
    "UseChatbot": false,
}
```
* <span class="icon settings">TwitchBotChannel</span> Bot twitch login.
* <span class="icon settings">TwitchBotOAUTH</span> How to obtain a Twitch OAUTH: <a class="icon twitch" href="https://www.twitchapps.com/tmi/" target="_blank">www.twitchapps.com/tmi/</a>
* <span class="icon settings">UseChatbot</span> (true/false) Enable chatbot.

<span class="icon idea">Never share your Twitch OAUTH with anyone. If someone has seen your OAUTH, generate a new one as soon as possible.</span>
