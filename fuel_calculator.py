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
        '''
          :return: This method validate entered data from user. And returns booleans for each input from user.
                   Also, method shows messages for valid or not valid type of input!
        '''
        self.fuels_list = ['gasoline', 'diesel', 'lpg', 'methane', 'dieselplus', 'gasoline98plus']
        self.input_fuel = ''
        self.input_consumption = 0
        self.input_distance = 0
        self.valid_type = False
        self.valid_consumption = False
        self.valid_distance = False

        # Validate type of fuel

        if self.fuel_type_item.get() != "" and self.fuel_type_item.get().lower() in self.fuels_list:
            self.input_fuel_msg = 'Correct input type!'
            self.input_fuel = self.fuel_type_item.get().lower()
            self.valid_type = True
        if not self.valid_type:
            self.input_fuel_msg = 'Incorrect fuel type!'
            self.message = messagebox.showwarning('Fuel type', 'Fuel type must be in the list')

        # Validate consumption of vehicle
        if self.consumption_item.get() != "":
            consumption = self.consumption_item.get()
            validate_consumption = re.match(r'(^|(?<=\s))-?(\d*)((\.|\,)\d+)?($|(?=\s))', consumption)
            if validate_consumption:
                consumption = consumption.replace(',', '.')
                if float(consumption) > 0:
                    self.input_consumption_msg = 'Correct input consumption!'
                    self.input_consumption = consumption
                    self.valid_consumption = True
        if not self.valid_consumption:
            self.input_consumption_msg = 'Incorrect consumption input!'
            self.message = messagebox.showwarning('Consumption',
                                                  'Consumption must be a number greater than zero!')
        # Validate distance for travel
        if self.distance_item.get() != "":
            distance = self.distance_item.get()
            validate_distance = re.match(r'(^|(?<=\s))-?(\d*)((\.|\,)\d+)?($|(?=\s))', distance)
            if validate_distance:
                distance = distance.replace(',', '.')
                if float(distance) > 0:
                    self.input_distance_msg = 'Correct input distance!'
                    self.input_distance = distance
                    self.valid_distance = True
        if not self.valid_distance:
            self.input_distance_msg = 'Incorrect distance input!'
            self.message = messagebox.showwarning('Distance',
                                                  'Distance must be a number greater than zero!')

        self.Check_data = self.input_fuel_msg, self.input_consumption_msg, self.input_distance_msg

        # Show messages about valid inputs in boxes  for each input data
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

        '''
        :return: If input data from user is invalid this method returns, a warning message.
                 If input data is validated as correct. Method returns information about selected type of fuel,
                 filled data from user about average consumption of vehicle and distance that
                 user want to travel.
        '''

        valid_input_data = False

        # Here we try to show the result if there is input data.

        try:
            if self.valid_type and self.valid_consumption and self.valid_distance:
                valid_input_data = True

                type_of_fuel = self.input_fuel
                average_consumption = float(self.input_consumption)
                travel_distance = float(self.input_distance)

                # This is web scrapping part that extract html data from target url
                target_url = f'https://bg.fuelo.net/fuel/type/{type_of_fuel}?lang=bg'
                response = requests.get(target_url)
                soup = BeautifulSoup(response.text, 'html.parser')
                html_output = soup.find_all('tbody')[-1].extract()
                html_to_string = str(html_output)
                fuel_stations = {}

                # List for messages from searching
                output_result_message = []

                # Filter needed information in extracted html data using RegExp
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

                # Prepare output message with chosen fuel sorted by price. Put in list with append() builtin.

                for station_name, products in sorted(fuel_stations.items(), key=lambda x: (x[1][1])):
                    station_number = list(fuel_stations).index(station_name)
                    brand, price = products[0], products[1]
                    output_result_message.append(
                        f'On fuel station {station_number + 1}: {station_name}\nThe amount of {brand} will cost {price:.2f}lv!\n')

        except AttributeError:
            valid_input_data = False

        if not valid_input_data:
            self.message = messagebox.showerror("Result",
                                                'Please enter a valid data for results or \nvalidate input data before click "SHOW RESULT" button!')
        else:
            def Result_window():
                """
                    :return: This method create a new popup window to show output data for searching

                    """
                # This is the part that creates a new window
                self.result_window = Toplevel()
                self.result_window.geometry("1024x768")
                self.result_window.title('Result of searching.')
                self.dollar_icon = ImageTk.PhotoImage(Image.open('dollar_logo.png'))
                self.logo = Label(self.result_window, image=self.dollar_icon, bg="white")
                self.logo.place(x=440, y=5)

                # This is the part that format the result of output data(like fonts, color, size etc.)
                self.frame3 = LabelFrame(self.result_window, text="TOP FIVE CHEAPEST GAS STATIONS", width=400,
                                         height=350,
                                         font=('Arial', 10, 'bold'),
                                         borderwidth=3, relief=RIDGE, highlightthickness=4, bg="white",
                                         highlightcolor="white",
                                         highlightbackground="white", fg="#248aa2")
                self.frame3.place(x=15, y=5)

                self.frame4 = LabelFrame(self.result_window, text="OTHER GAS STATIONS", width=450,
                                         height=750,
                                         font=('Arial', 10, 'bold'),
                                         borderwidth=3, relief=RIDGE, highlightthickness=4, bg="white",
                                         highlightcolor="white",
                                         highlightbackground="white", fg="#248aa2")
                self.frame4.place(x=560, y=5)

                self.cheapest_stations = Label(self.frame3, text='\n'.join(output_result_message[:5]),
                                               font=('arial', 10, 'bold'),
                                               bg="white")
                self.cheapest_stations.place(x=16, y=10)

                self.other_stations = Label(self.frame4, text='\n'.join(output_result_message[5:]),
                                            font=('arial', 10, 'bold'),
                                            bg="white")
                self.other_stations.place(x=16, y=10)

            Result_window()

    def Quit(self):
        '''
        :return: This method is an action from Exit Button, ask user to exit or not.
        '''

        self.message = messagebox.askquestion('Exit', "Do you want to exit the application?")
        if self.message == "yes":
            self.root.destroy()
        else:
            "return"

    def __init__(self):
        '''
        :return: This method crate: Main window, Result Buttons, Input Fields..
        '''

        # This part from __init__ create the main window.
        self.root = tk.Tk()
        self.root.geometry('500x300')
        self.root.title("Fuel calculator")
        self.root.maxsize(1920, 1080)
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

        # This part from __init__  create the fields for input data.
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

        # This part from __init__ create fields for output information about validate user inputs.

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

        # This part from __init__ create a Functional Buttons and connect them with their functions.

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
