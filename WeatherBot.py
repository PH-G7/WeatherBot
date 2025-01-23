from TwitchWebsocket import TwitchWebsocket
import json, requests, random, logging

from enum import Enum, auto
from Log import Log # type: ignore
Log(__file__)

from Settings import Settings # type: ignore

class ResultCode(Enum):
    SUCCESS = auto()
    ERROR = auto()

class TwitchWeather:
    def __init__(self):
        # Initialize variables
        self.host = None
        self.port = None
        self.chan = None
        self.nick = None
        self.auth = None
        self.api_key = None
        self.home = None

        # Fill uninitialized variables using settings.txt
        self.update_settings()

        # Instantiate TwitchWebsocket instance with correct params
        self.ws = TwitchWebsocket(host=self.host, 
                                  port=self.port,
                                  chan=self.chan,
                                  nick=self.nick,
                                  auth=self.auth,
                                  callback=self.message_handler,
                                  capability=None,
                                  live=True)
        
        # Start the websocket connection
        self.ws.start_bot()
        
    def update_settings(self):
        # Fill previously initialised variables with data from the settings.txt file
        self.host, self.port, self.chan, self.nick, self.auth, self.api_key, self.home = Settings().get_settings()

    def message_handler(self, m):
        try:
            if m.type == "366":
                logging.info(f"Successfully joined channel: #{m.channel}")
            
            elif m.type == "PRIVMSG":
                # Listen for command
                if m.message.startswith("!wxinfo"):
                    self.ws.send_message("The weather bot can do the following commands: !wx for full weather report, !wxtemp, !wxchill for wind chill, !wxpress for pressure, !wxhumid, !wxvis for visibility, !wxwind, !wxcloud for cloud cover, !wxrain for rain rate, or !wxsnow for snow rate. Name a specific city after the command to get the weather for that city or leave it blank to get weather for the streamer's location.")
                        
                # Command for just temperature
                elif m.message.startswith("!wxtemp"):
                    split_message = m.message.split()

                    # If city params are passed
                    if len(split_message) > 1:
                        location = " ".join(split_message[1:])

                        # Get the output as well as the return code
                        out, _code = self.fetch_temp(location)
                        
                        # Send messages to Twitch chat
                        # Because in all cases, error or success, 
                        # we want to output `out` to chat, we ignore `_code` for now.
                        self.ws.send_message(out)
                    
                    # If no city is provided the home city will be used
                    elif len(split_message) == 1:
                        location = self.home
                        
                        out, _code = self.fetch_temp(location)
                        
                        self.ws.send_message(out)
                        
                # Command for just wind chill
                elif m.message.startswith("!wxchill"):
                    split_message = m.message.split()

                    # If city params are passed
                    if len(split_message) > 1:
                        location = " ".join(split_message[1:])

                        # Get the output as well as the return code
                        out, _code = self.fetch_feelslike(location)
                        
                        # Send messages to Twitch chat
                        # Because in all cases, error or success, 
                        # we want to output `out` to chat, we ignore `_code` for now.
                        self.ws.send_message(out)
                    
                    # If no city is provided the home city will be used
                    elif len(split_message) == 1:
                        location = self.home
                        
                        out, _code = self.fetch_feelslike(location)
                        
                        self.ws.send_message(out)
                        
                # Command for just pressure
                elif m.message.startswith("!wxpress"):
                    split_message = m.message.split()

                    # If city params are passed
                    if len(split_message) > 1:
                        location = " ".join(split_message[1:])

                        # Get the output as well as the return code
                        out, _code = self.fetch_pressure(location)
                        
                        # Send messages to Twitch chat
                        # Because in all cases, error or success, 
                        # we want to output `out` to chat, we ignore `_code` for now.
                        self.ws.send_message(out)
                    
                    # If no city is provided the home city will be used
                    elif len(split_message) == 1:
                        location = self.home
                        
                        out, _code = self.fetch_pressure(location)
                        
                        self.ws.send_message(out)
                        
                # Command for just humidity
                elif m.message.startswith("!wxhumid"):
                    split_message = m.message.split()

                    # If city params are passed
                    if len(split_message) > 1:
                        location = " ".join(split_message[1:])

                        # Get the output as well as the return code
                        out, _code = self.fetch_humidity(location)
                        
                        # Send messages to Twitch chat
                        # Because in all cases, error or success, 
                        # we want to output `out` to chat, we ignore `_code` for now.
                        self.ws.send_message(out)
                    
                    # If no city is provided the home city will be used
                    elif len(split_message) == 1:
                        location = self.home
                        
                        out, _code = self.fetch_humidity(location)
                        
                        self.ws.send_message(out)

                # Command for just visibility
                elif m.message.startswith("!wxvis"):
                    split_message = m.message.split()

                    # If city params are passed
                    if len(split_message) > 1:
                        location = " ".join(split_message[1:])

                        # Get the output as well as the return code
                        out, _code = self.fetch_visibility(location)
                        
                        # Send messages to Twitch chat
                        # Because in all cases, error or success, 
                        # we want to output `out` to chat, we ignore `_code` for now.
                        self.ws.send_message(out)
                    
                    # If no city is provided the home city will be used
                    elif len(split_message) == 1:
                        location = self.home
                        
                        out, _code = self.fetch_visibility(location)
                        
                        self.ws.send_message(out)

                # Command for just wind
                elif m.message.startswith("!wxwind"):
                    split_message = m.message.split()

                    # If city params are passed
                    if len(split_message) > 1:
                        location = " ".join(split_message[1:])

                        # Get the output as well as the return code
                        out, _code = self.fetch_wind(location)
                        
                        # Send messages to Twitch chat
                        # Because in all cases, error or success, 
                        # we want to output `out` to chat, we ignore `_code` for now.
                        self.ws.send_message(out)
                    
                    # If no city is provided the home city will be used
                    elif len(split_message) == 1:
                        location = self.home
                        
                        out, _code = self.fetch_wind(location)
                        
                        self.ws.send_message(out)

                # Command for just temperature
                elif m.message.startswith("!wxcloud"):
                    split_message = m.message.split()

                    # If city params are passed
                    if len(split_message) > 1:
                        location = " ".join(split_message[1:])

                        # Get the output as well as the return code
                        out, _code = self.fetch_cloud(location)
                        
                        # Send messages to Twitch chat
                        # Because in all cases, error or success, 
                        # we want to output `out` to chat, we ignore `_code` for now.
                        self.ws.send_message(out)
                    
                    # If no city is provided the home city will be used
                    elif len(split_message) == 1:
                        location = self.home
                        
                        out, _code = self.fetch_cloud(location)
                        
                        self.ws.send_message(out)

                # Command for rain rate
                elif m.message.startswith("!wxrain"):
                    split_message = m.message.split()

                    # If city params are passed
                    if len(split_message) > 1:
                        location = " ".join(split_message[1:])

                        # Get the output as well as the return code
                        out, _code = self.fetch_rain(location)
                        
                        # Send messages to Twitch chat
                        # Because in all cases, error or success, 
                        # we want to output `out` to chat, we ignore `_code` for now.
                        self.ws.send_message(out)
                    
                    # If no city is provided the home city will be used
                    elif len(split_message) == 1:
                        location = self.home
                        
                        out, _code = self.fetch_rain(location)
                        
                        self.ws.send_message(out)

                # Command for snow rate
                elif m.message.startswith("!wxsnow"):
                    split_message = m.message.split()

                    # If city params are passed
                    if len(split_message) > 1:
                        location = " ".join(split_message[1:])

                        # Get the output as well as the return code
                        out, _code = self.fetch_snow(location)
                        
                        # Send messages to Twitch chat
                        # Because in all cases, error or success, 
                        # we want to output `out` to chat, we ignore `_code` for now.
                        self.ws.send_message(out)
                    
                    # If no city is provided the home city will be used
                    elif len(split_message) == 1:
                        location = self.home
                        
                        out, _code = self.fetch_snow(location)
                        
                        self.ws.send_message(out)

                # For full weather
                elif m.message.startswith("!wx"):
                    split_message = m.message.split()

                    # If city params are passed
                    if len(split_message) > 1:
                        location = " ".join(split_message[1:])

                        # Get the output as well as the return code
                        out, _code = self.fetch_weather(location)
                        
                        # Send messages to Twitch chat
                        # Because in all cases, error or success, 
                        # we want to output `out` to chat, we ignore `_code` for now.
                        self.ws.send_message(out)
                    
                    # If no city is provided the home city will be used
                    elif len(split_message) == 1:
                        location = self.home
                        
                        out, _code = self.fetch_weather(location)
                        
                        self.ws.send_message(out)

        except Exception as e:
            logging.exception(e)

    def deg_to_compass(self, num):
        val=int((num/22.5)+.5)
        arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
        return arr[(val % 16)]
           

    def fetch_weather(self, location):
        # Construct URL and get result
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}"
        data = requests.get(url).json()

        # In case the city is not found
        if data['cod'] == '404':
            return data['message'].capitalize(), ResultCode.ERROR

        # If successful
        elif data['cod'] == 200:
            celcius = float(data["main"]["temp"]) - 273.15
            fahrenheit = celcius * 1.8 + 32
            humidity = float(data["main"]["humidity"])
            description = data["weather"][0]["description"]
            out = f"{celcius:.1f}°C/{fahrenheit:.0f}°F, {humidity:.1f}% humidity, with {description}."
            
            return out, ResultCode.SUCCESS
        
        # If some other error (eg. api limit exceeded)
        else:
            if 'cod' in data:
                out = f"Error with code {data['cod']} encountered."
            else:
                out = "Unknown error encountered"
            return out, ResultCode.ERROR
            
    def fetch_temp(self, location):
        # Construct URL and get result
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}"
        data = requests.get(url).json()

        # In case the city is not found
        if data['cod'] == '404':
            return data['message'].capitalize(), ResultCode.ERROR

        # If successful
        elif data['cod'] == 200:
            celcius = float(data["main"]["temp"]) - 273.15
            fahrenheit = celcius * 1.8 + 32
            out = f"The current temperatue is {celcius:.1f}°C/{fahrenheit:.0f}°F."
            
            return out, ResultCode.SUCCESS
        
        # If some other error (eg. api limit exceeded)
        else:
            if 'cod' in data:
                out = f"Error with code {data['cod']} encountered."
            else:
                out = "Unknown error encountered"
            return out, ResultCode.ERROR            
    
    def fetch_feelslike(self, location):
        # Construct URL and get result
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}"
        data = requests.get(url).json()

        # In case the city is not found
        if data['cod'] == '404':
            return data['message'].capitalize(), ResultCode.ERROR

        # If successful
        elif data['cod'] == 200:
            celcius = float(data["main"]["feels_like"]) - 273.15
            fahrenheit = celcius * 1.8 + 32
            out = f"The wind chill is {celcius:.1f}°C/{fahrenheit:.0f}°F."
            
            return out, ResultCode.SUCCESS
        
        # If some other error (eg. api limit exceeded)
        else:
            if 'cod' in data:
                out = f"Error with code {data['cod']} encountered."
            else:
                out = "Unknown error encountered"
            return out, ResultCode.ERROR

    def fetch_pressure(self, location):
        # Construct URL and get result
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}"
        data = requests.get(url).json()

        # In case the city is not found
        if data['cod'] == '404':
            return data['message'].capitalize(), ResultCode.ERROR

        # If successful
        elif data['cod'] == 200:
            hPa = float(data["main"]["sea_level"])
            inHg = hPa * .02953
            hPaGrnd = float(data["main"]["grnd_level"])
            inHgGrnd = hPaGrnd * .02953
            out = f"The pressure is {hPa:.0f}hPa/{inHg:.2f}in Hg at sea level {hPaGrnd:.0f}hPa/{inHgGrnd:.2f}in Hg at ground level."
            
            return out, ResultCode.SUCCESS
        
        # If some other error (eg. api limit exceeded)
        else:
            if 'cod' in data:
                out = f"Error with code {data['cod']} encountered."
            else:
                out = "Unknown error encountered"
            return out, ResultCode.ERROR    

    def fetch_humidity(self, location):
        # Construct URL and get result
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}"
        data = requests.get(url).json()

        # In case the city is not found
        if data['cod'] == '404':
            return data['message'].capitalize(), ResultCode.ERROR

        # If successful
        elif data['cod'] == 200:
            humidity = float(data["main"]["humidity"])
            out = f"The humidity is {humidity:.0f}%."
            
            return out, ResultCode.SUCCESS
        
        # If some other error (eg. api limit exceeded)
        else:
            if 'cod' in data:
                out = f"Error with code {data['cod']} encountered."
            else:
                out = "Unknown error encountered"
            return out, ResultCode.ERROR           

    def fetch_visibility(self, location):
        # Construct URL and get result
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}"
        data = requests.get(url).json()

        # In case the city is not found
        if data['cod'] == '404':
            return data['message'].capitalize(), ResultCode.ERROR

        # If successful
        elif data['cod'] == 200:
            visibilitykm = float(data["visibility"])/1000
            visibilitymi = visibilitykm * 0.621371
            if visibilitykm == 10:
                out = "Visibility is greater than 10km/6.2mi."
            else:
                out = f"Visibility is {visibilitykm:.1f}km/{visibilitymi:.1f}mi."
            
            return out, ResultCode.SUCCESS
        
        # If some other error (eg. api limit exceeded)
        else:
            if 'cod' in data:
                out = f"Error with code {data['cod']} encountered."
            else:
                out = "Unknown error encountered"
            return out, ResultCode.ERROR  

    def fetch_wind(self, location):
        # Construct URL and get result
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}"
        data = requests.get(url).json()

        # In case the city is not found
        if data['cod'] == '404':
            return data['message'].capitalize(), ResultCode.ERROR

        # If successful
        elif data['cod'] == 200:
            if "gust" in data["wind"]:
                speedkmh = float(data["wind"]["speed"])*3.6
                speedmih = speedkmh * 0.621371
                degree = float(data["wind"]["deg"])
                direction = self.deg_to_compass(degree)
                gustkmh = float(data["wind"]["gust"])*3.6
                gustmih = gustkmh * 0.621371
                out = f"The wind is blowing from {degree:.0f}° ({direction}) at {speedmih:.1f} mi/h ({speedkmh:.1f} km/h) gusting to {gustmih:.1f} mi/h ({gustkmh:.1f} km/h)."
            else:
                speedkmh = float(data["wind"]["speed"])*3.6
                speedmih = speedkmh * 0.621371
                degree = float(data["wind"]["deg"])
                direction = self.deg_to_compass(degree)
                out = f"The wind is blowing from {degree:.0f}° ({direction}) at {speedmih:.1f} mi/h ({speedkmh:.1f} km/h)."
            return out, ResultCode.SUCCESS
        
        # If some other error (eg. api limit exceeded)
        else:
            if 'cod' in data:
                out = f"Error with code {data['cod']} encountered."
            else:
                out = "Unknown error encountered"
            return out, ResultCode.ERROR  

    def fetch_cloud(self, location):
        # Construct URL and get result
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}"
        data = requests.get(url).json()

        # In case the city is not found
        if data['cod'] == '404':
            return data['message'].capitalize(), ResultCode.ERROR

        # If successful
        elif data['cod'] == 200:
            cloudcover = float(data["clouds"]["all"])
            out = f"The current cloud cover is {cloudcover:.0f}%."
            
            return out, ResultCode.SUCCESS
        
        # If some other error (eg. api limit exceeded)
        else:
            if 'cod' in data:
                out = f"Error with code {data['cod']} encountered."
            else:
                out = "Unknown error encountered"
            return out, ResultCode.ERROR  

    def fetch_rain(self, location):
        # Construct URL and get result
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}"
        data = requests.get(url).json()

        # In case the city is not found
        if data['cod'] == '404':
            return data['message'].capitalize(), ResultCode.ERROR

        # If successful
        elif data['cod'] == 200:
            if "rain" in data:
                rainratemmh = float(data["rain"]["1h"])
                rainrateinh = rainratemmh*0.0393701
                out = f"The current rain rate is {rainrateinh:.2f} in/h ({rainratemmh:.0f} mm/h)."
            else:
                out = "It is not currently raining at this location."
            
            return out, ResultCode.SUCCESS
        
        # If some other error (eg. api limit exceeded)
        else:
            if 'cod' in data:
                out = f"Error with code {data['cod']} encountered."
            else:
                out = "Unknown error encountered"
            return out, ResultCode.ERROR 

    def fetch_snow(self, location):
        # Construct URL and get result
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}"
        data = requests.get(url).json()

        # In case the city is not found
        if data['cod'] == '404':
            return data['message'].capitalize(), ResultCode.ERROR

        # If successful
        elif data['cod'] == 200:
            if "snow" in data:
                snowratemmh = float(data["snow"]["1h"])
                snowrateinh = snowratemmh*0.0393701
                out = f"The current snow rate is {snowrateinh:.1f} in/h ({snowratemmh:.0f} mm/h)."
            else:
                out = "It is not currently snowing at this location."
            
            return out, ResultCode.SUCCESS
        
        # If some other error (eg. api limit exceeded)
        else:
            if 'cod' in data:
                out = f"Error with code {data['cod']} encountered."
            else:
                out = "Unknown error encountered"
            return out, ResultCode.ERROR              

if __name__ == "__main__":
    TwitchWeather()
