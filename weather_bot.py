

import telebot
import requests as req
import json
import pandas as pd

my_weather_bot = telebot.TeleBot("TOKEN")

def kelvin_to_celcius_converter(temp_in_kelvin):
  temp_in_celcius = temp_in_kelvin - 273.15
  return temp_in_celcius


@my_weather_bot.message_handler(commands=['start'])
def send_welcome(message):
  
  print("message from:" + message.from_user.first_name)
  my_weather_bot.send_message(message.chat.id,"!!! WELCOME TO WEATHER ENQUIRY BOT !!! \n\n Enter a city name to know the weather report  !!!")
  

@my_weather_bot.message_handler(func=lambda m: True)
def echo_all(msg):
  
  print(msg.text)
  msg_text =  msg.text
  msg_text = msg_text.split()
  msg_text = pd.DataFrame(msg_text,columns = ["words"])
  
  try:
    data_of_cities = pd.read_csv("worldcities.csv")
    #print(data_of_cities.head())
    city = "" 

         
    for i in msg_text['words']:
      for j in data_of_cities['city_name']:
        if i.lower() == j.lower():
          city = i
        
        #print(city)    
           
        
         
    response = req.get("http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=3863ac39fc7b19ea442bbc9dfecd3ed3")
    response_text = json.loads(response.text)
    print(response_text)
    my_weather_bot.send_message(msg.chat.id,"the weather report of "+ city + "  is :"+"\n Temp  :  "+str(kelvin_to_celcius_converter(response_text["main"]["temp"]))+"°C" + "\nHumidity is :  "+ str(response_text["main"]["humidity"])+ "\n and Pressure is :  "+ str(response_text["main"]["pressure"])+" Pa")

  except Exception as e:
    my_weather_bot.send_message(msg.chat.id,"Wooops!I don't understand this.Just programmed to do one thing. Enter a city for details")
    print(e)

my_weather_bot.polling()







