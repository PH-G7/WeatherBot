# WeatherBot
A more advanced version of [TwitchWeather](https://github.com/tomaarsen/TwitchWeather) by tomaarsen.

---

# Explanation

When the bot has started, it will listen to chat messages in the channel listed in the settings.txt file. Whenever a user types `!wx <city>` or one of the other commands in chat, the bot will respond with precise weather information in that city. If the user doesn't provide a city, the home city set in settings.txt will be used.

---

# Usage
Commands:
<pre><b>!wx (general weather report)<br>!wxtemp (temperature)<br>!wxchill (windchill)<br>!wxpress (air pressure)<br>!wxhumid (humidity)<br>!wxvis (visibility)<br>!wxwind (wind speed, direction,  gust)<br>!wxcloud (cloud cover)<br>!wxrain (rain rate)<br>!wxsnow (snow rate)<br>!wxinfo (info message that explains how the bot works)</b></pre>

---

# Settings
This bot is controlled by a settings.txt file, which looks like:
```
{
    "Host": "irc.chat.twitch.tv",
    "Port": 6667,
    "Channel": "#<channel>",
    "Nickname": "<name>",
    "Authentication": "oauth:<auth>",
    "OWMKey": "<OpenWeatherMap api key>"
    "Home": "<Home Location>"
}
```

| **Parameter**        | **Meaning** | **Example** |
| -------------------- | ----------- | ----------- |
| Host                 | The URL that will be used. Do not change.                         | "irc.chat.twitch.tv" |
| Port                 | The Port that will be used. Do not change.                        | 6667 |
| Channel              | The Channel that will be connected to.                            | "#ph__g" |
| Nickname             | The Username of the bot account.                                  | "phg_bot" |
| Authentication       | The OAuth token for the bot account.                              | "oauth:pivogip8ybletucqdz4pkhag6itbax" |
| OWMKey | The OpenWeatherMap API Key. Get your own free key [here](https://openweathermap.org/appid). | "9a8nec2aydmm5q6kjr01ajm5zvgjcyv0" |
| Home                 | The location you want to use for the default weather location     | "Los Angeles, CA, US" |

*Note that the example OAuth token is not an actual token, nor is the OWMKey an actual API key, but merely a generated string to indicate what it might look like.*

I got my real OAuth token from https://twitchtokengenerator.com/.

---

# Requirements
* [Python 3.6+](https://www.python.org/downloads/)
* [TwitchWebsocket](https://github.com/CubieDev/TwitchWebsocket) by tomaarsen
