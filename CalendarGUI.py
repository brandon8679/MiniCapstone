import tkinter
import calendar
import time
from tkinter import ttk
import requests
import json


def update(y, m, tx, curdate):  # generate calendar with right colors
    calstr = calendar.month(y, m)
    tx.configure(state=tkinter.NORMAL)
    tx.delete('0.0', tkinter.END)  # remove previous calendar
    tx.insert(tkinter.INSERT, calstr)



    for i in range(2, 9):
        tx.tag_add("others", '{}.0'.format(i), '{}.end'.format(i))  # tag days for coloring
        if len(tx.get('{}.0'.format(i), '{}.end'.format(i))) == 20:
            tx.tag_add("sun", '{}.end-2c'.format(i), '{}.end'.format(i))
    tx.tag_config("sun", foreground="#ff0000 ")
    tx.tag_config("others", foreground="#000")
    tx.tag_add("head", '1.0', '1.end')
    if curdate[0] == y and curdate[1] == m:
        index = tx.search(str(curdate[2]), '2.0')  # search for today's date
        tx.tag_add("cur", index, '{}+2c'.format(index))  # highlight today's date
        tx.tag_config("cur", background="blue", foreground="white")
    tx.tag_config("hasnote", background="white")
    tx.tag_config("head", font='helvetica 12', foreground="#0d8241", justify=tkinter.CENTER)
    tx.configure(state=tkinter.DISABLED)  # make text view not editable
    underLineTextUpdate(tx)

def readNotes():
    with open("Notes", "r") as noteDoc:
        noteText = noteDoc.readlines()
        for i in noteText:
            splitted = i.split(",")
            notes[splitted[0]] = splitted[1]
            print(notes)

def underLineTextUpdate(tx):
    keyslist = notes.keys()
    month, year = calendar.month(yearInt, monthInt).split("\n")[0].split(" ")[-2:]
    for i in keyslist:
        m,d,y = i.split(" ")
        if m == month and y == year:
            index = tx.search(d, '2.0')  # search for today's date
            tx.tag_add("hasnote", index, '{}+2c'.format(index))  # highlight today's date


top = tkinter.Tk()
top.title("Calendar")
top.minsize(200, 200)
top.maxsize(250, 250)
curtime = time.localtime()
year = tkinter.StringVar()
month = tkinter.StringVar()
yearInt = curtime[0]
monthInt = curtime[1]
# dateInt = curtime[2]
notes = {}


HLayout = ttk.PanedWindow(top, orient=tkinter.HORIZONTAL)
ctx = tkinter.Text(top, padx=10, pady=10, bg="#f3e9ae", relief=tkinter.FLAT, height=9,
                   width=20)  # text view to passing to functions

readNotes()






def nextb():  # on click next button
    global monthInt, yearInt, ctx, curtime
    monthInt += 1
    if monthInt > 12:
        monthInt = monthInt % 12
        yearInt += 1
    update(yearInt, monthInt, ctx, curtime)


def prevb():  # on click previous button
    global monthInt, yearInt, ctx, curtime
    monthInt -= 1
    if monthInt < 1:
        monthInt = 12
        yearInt -= 1
    update(yearInt, monthInt, ctx, curtime)


def addNote():
    global monthInt, yearInt, ctx, curtime, notes
    print("If you would like to read a note, type, r followed by the date as Month Day Year \n"
          "If you would like to write a note, type, w followed by the date as Month Day Year \n"
          "Type a for weather")
    userIn = input()
    userInsplit = userIn.split(" ")
    if len(userInsplit) > 2:
        key = userInsplit[1] + " " + userInsplit[2] + " " + userInsplit[3]
    else:
        key = None
    if userInsplit[0] == "w":
        note = open("Notes", "a+")
        print("Type what you wish to add as a note")
        userNote = input()
        note.write("\n" + key + "," + userNote)
        note.close()
        notes.update({key : userNote})
        underLineTextUpdate(ctx)


    elif userInsplit[0] == "r":
        print(notes[key])
    elif userInsplit[0] == "a":
        Weather()
    else:
        print("No valid input")
def toFaren(temp):
    return str(int((temp - 273.15)*(9/5)+32))

def Weather():
    api_key = "6baf5ffca81a36d2950b3c0a7c6c0bb2"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # Give city name
    city_name = input("Enter city name : ")
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)

    x = response.json()

    if x["cod"] != "404":

        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]

        z = x["weather"]

        weather_description = z[0]["description"]

        # print following values
        print(" Temperature (in Fahrenheit) = " +
              toFaren(current_temperature) +
              "\n atmospheric pressure (in hPa unit) = " +
              str(current_pressure) +
              "\n humidity (in percentage) = " +
              str(current_humidiy) +
              "\n description = " +
              str(weather_description))

    else:
        print(" City Not Found ")


update(yearInt, monthInt, ctx, curtime)  # for first run, generate calendar
underLineTextUpdate(ctx)
prev = ttk.Button(HLayout, text="<<", command=prevb)
nex = ttk.Button(HLayout, text=">>", command=nextb)
addNote = ttk.Button(HLayout, text = "Add/Read Note", command = addNote)
menubar = tkinter.Menu(top, relief=tkinter.FLAT)
top.config(menu=menubar)
prev.pack(side=tkinter.LEFT)
nex.pack(side=tkinter.RIGHT)
addNote.pack(side=tkinter.BOTTOM)
ctx.pack()
HLayout.pack()
top.mainloop()
