import tkinter as tk
import re
import requests
from tkinter import *
from time import gmtime, strftime, localtime
from PIL import ImageTk, Image
from tkinter import messagebox
from bs4 import BeautifulSoup


class FuelCalculator:

    def Check_data(self):
        self.fuels_list = ['gasoline', 'diesel', 'lpg', 'methane', 'dieselPlus', 'gasoline98plus']
        self.input_fuel = ''
        self.input_consumption = 0
        self.input_distance = 0

        if self.fuel_type_item.get() != "" and self.fuel_type_item.get().lower() in self.fuels_list:
            self.input_fuel_msg = 'Correct input type!'
            self.input_fuel = self.fuel_type_item.get().lower()
        else:
            self.input_fuel_msg = 'Incorrect fuel type!'
            self.message = messagebox.showerror('Fuel type', 'Fuel type must be in the list')

        if self.consumption_item.get() != "" and not self.consumption_item.get().isalpha():
            if float(self.consumption_item.get()) > 0:
                self.input_consumption_msg = 'Correct input consumption!'
                self.input_consumption = self.consumption_item.get()
        else:
            self.input_consumption_msg = 'Incorrect consumption input!'
            self.message = messagebox.showerror('Consumption',
                                                'Consumption must be a number greater than zero.\n And must have dot [ . ] for delimeter!')

        if self.distance_item.get() != "" and not self.distance_item.get().isalpha():
            if float(self.distance_item.get()) > 0:
                self.input_distance_msg = 'Correct input distance!'
                self.input_distance = self.distance_item.get()
        else:
            self.input_distance_msg = 'Incorrect distance input!'
            self.message = messagebox.showerror('Distance',
                                                'Distance must be a number greater than zero.\n And must have dot [ . ] for delimeter!')

        self.Check_data = self.input_fuel_msg, self.input_consumption_msg, self.input_distance_msg

        if self.check_fuel != "":
            self.check_fuel.delete(0, END)
            self.check_fuel.insert(END, self.Check_data[0])
        else:
            self.check_fuel.insert(END, self.Check_data[0])

        if self.check_consumption != "":
            self.check_consumption.delete(0, END)
            self.check_consumption.insert(END, self.Check_data[1])
        else:
            self.check_consumption.insert(END, self.Check_data[1])

        if self.check_distance != "":
            self.check_distance.delete(0, END)
            self.check_distance.insert(END, self.Check_data[2])
        else:
            self.check_distance.insert(END, self.Check_data[2])

    def Result(self):
        type_of_fuel, average_consumption, travel_distance = self.input_fuel, float(self.input_consumption), float(
            self.input_distance)
        message = ''

        target_url = f'https://bg.fuelo.net/fuel/type/{type_of_fuel}?lang=bg'

        response = requests.get(target_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        html_output = soup.find_all('tbody')[-1].extract()
        html_to_string = str(html_output)
        fuel_stations = {}

        for html_row in html_to_string.split('\n'):
            match_brand = re.findall(r'title="(?P<gas_station>.+)"\/><\/a> (?P<type>.+)<\/td>', html_row)
            match_price = re.findall(r'<td>(?P<price>.+) лв\.\/(кг|л)<\/td>', html_row)
            if match_brand:
                current_station = match_brand[0][0]
                current_fuel = match_brand[0][1]
                fuel_stations[current_station] = [current_fuel]
            if match_price:
                fuel_price = float(match_price[0][0].replace(',', '.'))
                consumed_fuel = travel_distance / average_consumption
                if type_of_fuel == 'methane':
                    fuel_price = fuel_price / 5.6
                total_price = fuel_price * consumed_fuel
                fuel_stations[current_station].append(total_price)

        for fuel_station, products in fuel_stations.items():
            brand, price = products[0], products[1]
            message += f'On fuel station: {fuel_station}\nThe amount of {brand} will cost {price:.2f}lv!\n'

        self.message = messagebox.showinfo("Result", message)

    def Quit(self):
        self.message = messagebox.askquestion('Exit', "Do you want to exit the application?")
        if self.message == "yes":
            self.root.destroy()
        else:
            "return"

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('500x300')
        self.root.title("Fuel calculator")
        self.root.maxsize(1024, 768)
        self.root.minsize(1024, 768)
        self.root['bg'] = "white"

        self.heading = Label(self.root, text="FUEL PRICE CALCULATOR", font=('verdana', 20, 'bold'), fg="#248aa2",
                             bg="white")
        self.heading.place(x=315, y=5)
        self.style1 = Label(self.root, bg="#000033", height=1, width=50)
        self.style1.place(x=0, y=60)
        self.style2 = Label(self.root, bg="#000033", height=1, width=105)
        self.style2.place(x=630, y=60)
        self.date = Label(self.root, text=strftime("%Y-%m-%d %H:%M:%S", localtime()), font=('verdana', 12, 'bold'),
                          bg="white")
        self.date.place(x=400, y=60)
        self.fuel_types = Label(self.root, text=f'Type of available fuels are:',
                                font=('verdana', 12, 'bold'),
                                bg="white")
        self.fuel_types.place(x=68, y=105)
        self.fuel_types = Label(self.root, text='Gasoline, Diesel, LPG, Methane, DieselPlus, Gasoline98plus',
                                font=('verdana', 13, 'bold'),
                                bg="white")
        self.fuel_types.place(x=68, y=135)

        self.car_icon = ImageTk.PhotoImage(Image.open('car.jpg'))
        self.logo = Label(self.root, image=self.car_icon, bg="white")
        self.logo.place(x=560, y=350)

        # ================== Items to for  input ===================
        self.frame1 = LabelFrame(self.root, text="NEEDED INFORMATION", width=800, height=170,
                                 font=('verdana', 10, 'bold'),
                                 borderwidth=3, relief=RIDGE, highlightthickness=4, bg="white", highlightcolor="white",
                                 highlightbackground="white", fg="#248aa2")
        self.frame1.place(x=75, y=180)

        self.fuel_type = Label(self.frame1, text="Please enter fuel type:", font=('verdana', 12, 'bold'), bg="white")
        self.fuel_type.place(x=16, y=10)
        self.fuel_type_item = Entry(self.frame1, width=25, borderwidth=3, relief=RAISED, bg="#ffdd88")
        self.fuel_type_item.place(x=560, y=10)

        self.consumption = Label(self.frame1, text="Please enter average consumption of vehicle in liters:",
                                 font=('verdana', 12, 'bold'), bg="white")
        self.consumption.place(x=16, y=55)
        self.consumption_item = Entry(self.frame1, width=25, borderwidth=3, relief=RAISED, bg="#ffdd88")
        self.consumption_item.place(x=560, y=55)

        self.distance = Label(self.frame1, text="Please enter distance in kilometers:", font=('verdana', 12, 'bold'),
                              bg="white")
        self.distance.place(x=16, y=100)
        self.distance_item = Entry(self.frame1, width=25, borderwidth=3, relief=RAISED, bg="#ffdd88")
        self.distance_item.place(x=560, y=100)

        # ============ Check data =================

        self.frame2 = LabelFrame(self.root, text="CHECK DATA", width=480, height=140,
                                 font=('verdana', 10, 'bold'), borderwidth=3, relief=RIDGE, highlightthickness=4,
                                 bg="white", highlightcolor="white", highlightbackground="white", fg="#248aa2")
        self.frame2.place(x=75, y=420)

        self.check_fuel_lb = Label(self.frame2, text="Fuel check:", font=('verdana', 10, 'bold'), bg="white")
        self.check_fuel_lb.place(x=3, y=1)
        self.check_fuel = Entry(self.frame2, width=45, borderwidth=4, relief=SUNKEN, bg="#ffdd88")
        self.check_fuel.place(y=1, x=170)

        self.check_consumption_lb = Label(self.frame2, text="Consumption check:", font=('verdana', 10, 'bold'),
                                          bg="white")
        self.check_consumption_lb.place(x=3, y=35)
        self.check_consumption = Entry(self.frame2, width=45, borderwidth=4, relief=SUNKEN, bg="#ffdd88")
        self.check_consumption.place(y=35, x=170)

        self.check_distance_lb = Label(self.frame2, text="Distance check:", font=('verdana', 10, 'bold'),
                                       bg="white")
        self.check_distance_lb.place(x=3, y=70)
        self.check_distance = Entry(self.frame2, width=45, borderwidth=4, relief=SUNKEN, bg="#ffdd88")
        self.check_distance.place(y=70, x=170)

        # ================== Functional  buttons ============
        self.Check_data_btn = Button(self.root, text="CHECK INPUT", relief=RAISED, borderwidth=2,
                                     font=('verdana', 10, 'bold'), bg='#248aa2', fg="white", command=self.Check_data)
        self.Check_data_btn.place(x=75, y=380)

        self.Result_btn = Button(self.root, text="SHOW RESULT", relief=RAISED, borderwidth=2,
                                 font=('arial', 20, 'bold'),
                                 bg='#248aa2', fg="white", command=self.Result)
        self.Result_btn.place(x=140, y=620)

        self.icon = ImageTk.PhotoImage(Image.open('exit.png'))
        self.Quit_btn = Button(self.root, image=self.icon, relief=RAISED, borderwidth=2, font=('verdana', 12, 'bold'),
                               bg='#248aa2', fg="white", padx=5, command=self.Quit)
        self.Quit_btn.place(x=963, y=735)

        self.root.mainloop()


if __name__ == '__main__':
    FuelCalculator()
