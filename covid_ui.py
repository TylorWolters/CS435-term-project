# UI for software engineering project

from tkinter import *
from csv_downloader import *
from csv_parser import *
from search import *

# Title of UI
gui_title = Tk()
gui_title.title("Covid Visualizer")

# window grid
gui_title.rowconfigure(0, minsize=50)
gui_title.columnconfigure([0, 1], minsize=50)

# to see which radio button is selected when search/ gets a value
radio_value = IntVar()

global data  # Data Frame variable
global label  # tracks which data set is being used for the map


def radio_data(args):
    # radio button data
    global data
    global label

    if args == 1:
        data = case_data
        label = "cases"

    elif args == 2:
        data = death_data
        label = "deaths"

    else:
        data = population_data


def onclick(args):
    global data
    global label

    if args == 0:
        # close
        gui_title.destroy()

    elif args == 1:
        # search function

        if (len(stateEntry.get()) == 0):

            if (len(countyEntry.get()) == 0):

                generate_map(data, label)

            else:
                pass  # search function requires a state entry to search for a county

        elif (len(countyEntry.get()) == 0):

            data = search_df(data, state=stateEntry.get())
            generate_map(data, label)

        else:
            data = search_df(data, state=stateEntry.get(), county=countyEntry.get())
            generate_map(data, label)

    elif args == 2:
        countyEntry.delete(0, END)
        stateEntry.delete(0, END)
        radio_value.set(0)

    elif args == 3:
        export_data(data, "json")

    elif args == 4:
        export_data(data, "csv")


# buttons
close_button = Button(gui_title, text="Close", command=lambda: onclick(0))
search_button = Button(gui_title, text="Search", command=lambda: onclick(1))
clear_button = Button(gui_title, text="Clear", command=lambda: onclick(2))
downloadJson_button = Button(gui_title, text="Download JSON", command=lambda: onclick(3))
downloadCSV_button = Button(gui_title, text="Download CSV", command=lambda: onclick(4))
case_radio_button = Radiobutton(gui_title, text="Cases", variable=radio_value, value=1, command=lambda: radio_data(1))
death_radio_button = Radiobutton(gui_title, text="Deaths", variable=radio_value, value=2, command=lambda: radio_data(2))

# labels so user knows where to input county and state
stateLabel = Label(gui_title, text="State")
stateLabel.grid(row=1, column=1, sticky=E)
countyLabel = Label(gui_title, text="County")
countyLabel.grid(row=2, column=1, sticky=E)

# user entries
stateEntry = Entry(gui_title)
stateEntry.grid(row=1, column=2)
countyEntry = Entry(gui_title)
countyEntry.grid(row=2, column=2)

# button positions
search_button.grid(row=1, column=5)
clear_button.grid(row=2, column=5)
downloadJson_button.grid(row=18, column=2)
downloadCSV_button.grid(row=18, column=4)
close_button.grid(row=20, column=3)
case_radio_button.grid(row=1, column=3)
death_radio_button.grid(row=2, column=3)

gui_title.mainloop()