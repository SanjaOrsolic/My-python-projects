from tkinter import*
import datetime as dt
import locale
import requests
import json
from bs4 import BeautifulSoup


#-----Dohvat podataka

def get_weather_data(api_key, city_id):  
    api_url = "http://api.openweathermap.org/data/2.5/weather"  
    params = {  
        "id": city_id,  
        "units": "metric",  
        "appid": api_key  
    }  
    response = requests.get(api_url, params=params)  
    data = response.json()  
    return data  
  
api_key = "c94a2499bf7fc730cc0e2d7777112526"  
city_id = "3186294"  # Žu 
  
podaci = get_weather_data(api_key, city_id)  
#print(podaci)
  
temperature = podaci["main"]["temp"]  
city = podaci["name"]  
humidity = podaci["main"]["humidity"]  
wind_speed = podaci["wind"]["speed"]
vrijeme_ikona=podaci['weather'][0]['description']
 
import time  
import threading  
  
def get_hourly_weather_data():  
    while True:  
        data = get_weather_data(api_key, city_id)  
        time.sleep(3600)  # wait one hour  
  
thread = threading.Thread(target=get_hourly_weather_data)  
thread.start()


filename_json = 'weather_Zu.json'
with open(filename_json, 'w') as file:
    json.dump(podaci, file, indent=4)


#-------GUI


root=Tk()
root.geometry("700x750")
root.title("Smart Mirror")
root.config(bg="#2f3e46")
root.resizable(False,False)


#-----Datum i vrijeme
locale.setlocale(locale.LC_TIME, 'hr_HR')
datum=dt.datetime.now()
lijepi_datum=datum.strftime("%d. %B %Y.")
dan=datum.strftime("%A")
dan_prikaz=dan.capitalize()

def vrijeme():
    sat=time.strftime("%H:%M:%S")
    sat_prikaz=Label(root, text=sat, font=("Comic Sans MS", 24), fg="white", bg="#2f3e46",padx=10)
    sat_prikaz.place(x=50, y=60)
    root.after(1000,vrijeme)
vrijeme()

#-----Datum i vrijeme GUI
datum_prikaz=Label(root, text=(f"{dan_prikaz},  {lijepi_datum}"), font=("Comic Sans MS", 14), fg="white", bg="#2f3e46")
datum_prikaz.place(x=20,y=20)



#----- Temperatura i vrijeme GUI
grad=Label(root, text=f"{city} ",font=("Comic Sans MS", 16), fg="white", bg="#2f3e46")
grad.place(x=450,y=20)
temp_text=Label(root,text="Temperatura:",font=("Comic Sans MS", 12), fg="white", bg="#2f3e46")
temp_text.place(x=580,y=30)
temp_prikaz=Label(root,text=f"{round(temperature)} °C",font=("Comic Sans MS", 18), fg="white", bg="#2f3e46")
temp_prikaz.place(x=610,y=55)
tlak_zraka_text=Label(root,text="Brzina vjetra:",font=("Comic Sans MS", 12), fg="white", bg="#2f3e46")
tlak_zraka_text.place(x=580,y=90)
brzina_vjetra_prikaz=Label(root,text=f"{round(wind_speed,1)} m/s",font=("Comic Sans MS", 14), fg="white", bg="#2f3e46")
brzina_vjetra_prikaz.place(x=610,y=120)
vlaznost_text=Label(root,text="Vlaznost:",font=("Comic Sans MS", 12), fg="white", bg="#2f3e46")
vlaznost_text.place(x=610,y=150)
vlaznost_prikaz=Label(root,text=f"{round(humidity)} %",font=("Comic Sans MS", 14), fg="white", bg="#2f3e46")
vlaznost_prikaz.place(x=630,y=180)


if vrijeme_ikona=="few clouds" or vrijeme_ikona=="scattered clouds":
    few_clouds=PhotoImage(file="few_clouds.png").subsample(30)
    few_clouds_prikaz=Label(root, image=few_clouds,bg="#2f3e46")
    few_clouds_prikaz.place(x=430,y=60)
elif vrijeme_ikona=="clear sky":
    clear_sky=PhotoImage(file="clear_sky.png").subsample(3)
    clear_sky_prikaz=Label(root, image=clear_sky,bg="#2f3e46")
    clear_sky_prikaz.place(x=430,y=60)
elif vrijeme_ikona=="moderate rain" or vrijeme_ikona=="light rain" or vrijeme_ikona=="heavy intensity rain":
    rain=PhotoImage(file="rain.png").subsample(4)
    rain_prikaz=Label(root, image=rain,bg="#2f3e46")
    rain_prikaz.place(x=430,y=60)
elif vrijeme_ikona=="broken clouds" or vrijeme_ikona=="overcast clouds":
    clouds=PhotoImage(file="clouds.png").subsample(4)
    clouds_prikaz=Label(root, image=clouds,bg="#2f3e46")
    clouds_prikaz.place(x=430,y=60)
else:
    pass

#----- Vijest dana

url_vijesti="https://www.index.hr/"
response=requests.get(url_vijesti)
soup_vijesti=BeautifulSoup(response.text, "html.parser")
vijest=soup_vijesti.find("h2",class_="title").text


raspored=Label(root,text="Vijest dana:",font=("Comic Sans MS", 12), fg="white", bg="#2f3e46")
raspored.place(x=20,y=520)
crta=Label(root,text="_____________________",font=("Comic Sans MS", 10), fg="white", bg="#2f3e46",padx=0,pady=0)
crta.place(x=20,y=545)

vijest_prikaz1=Label(root,text=vijest,font=("Comic Sans MS", 12), fg="white", bg="#2f3e46",wraplength=250, justify=LEFT)
vijest_prikaz1.place(x=20,y=570)




#----- Poruka
poruka=Label(root,text="Podijelite svoj osmijeh sa svijetom. To je simbol prijateljstva i mira.",font=("Comic Sans MS", 14), fg="white", bg="#2f3e46")
poruka.place(x=50, y=700)

root.mainloop()