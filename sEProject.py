#UI for software engineering project

import Tkinter as tk
from Tkinter import *
import pandas as pd
from pandas import *
import numpy as np
from search import *
from csv_parser import *

#Title of UI
gui_title = Tk()

#frame
frame = Frame(gui_title)
frame.pack()
    
global df#Data Frame variable

def cases_show(cases_label):

    #

def onclick(args):

    if args == 0:
        close()

    elif args == 1:
        #entry getters
        stateGet = get(stateVar)
        countyGet = get(countyVar)
        #search function
        searchFunc(stateGet, countyGet)

    elif args == 2:
        gui_title.countyEntry.delete(0, END)
        gui_title.stateEntry.delete(0, END)
    
    elif args == 3:
        exportCSV_filepath = filedialog.asksaveasfilename(defaultextension = '.csv'
        df.to_csv(exportCSV_filepath, index = false, header = true)

    elif args == 4:
        exportJSON_filepath = filedialog.asksaveasfilename(defaultextension = '.json'
        df.to_json(exportJSON_filepath, index = false, header = true)

#buttons
close_button = Button(gui_title, text = "Close", command = lambda:onclick(0))
search_button = Button(gui_title, text = "Search", command = lambda:onclick(1))
clear_button = Button(gui_title, text = "Clear", command = lambda: onclick(2))
downloadJson_button = Button(gui_title, text = "Download JSON", command = lambda:onclick(3))
downloadCSV_button = Button(gui_title, text = "Dwonload CSv", command = lambda:onclick(4))

#labels so user knows where to input county and state
stateLabel = Label(gui_title, text = State, relief = RAISED)
stateLabell.pack()
countyLabel = Label(gui_title, text = County,relief = RAISED)
countyLabell.pack()

#text variables for user entires to be able to return
stateVar = StringVar()
countyVar = StringVar()

#user entries
stateEntry = Entry(gui_title, textvariable = "stateVar",bd =2)
stateEntry.pack()
countyEntry = Entry(gui_title, textvariable = "countyVar",bd =2)
countyEntry.pack()

search_button.pack()
clear_button.pack()
close_button.pack()

#shows the information that was looked up
cases_label = Label(gui_title, text = 'Total Cases')
cases_label.pack()
deaths_label = Label(gui_title, text = 'Total Deaths')
deaths_label.pack()
date_label = Label(gui_title, text = 'todays_date')
date_label.pack()


downloadJson_button.pack()
downloadJson_button.pack()

gui_title.mainloop()