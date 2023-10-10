from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk,ImageGrab
from tkinter import filedialog, messagebox
import os
import cv2
import customtkinter as ctk
from utils import sql, calculate_percentage, text_classifier_final, transform_data
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import numpy as np
from datetime import datetime, timedelta
import time
from OCR.ocr_pipeline import OCRPipeline
from OCR.tool.config import Config
from NLP.nlu_pipeline import NLUPipeLine

class MyGUI():
    def __init__(self):
        self.mysql = sql.MySQL("localhost", "root", "chinh210602")
        self.mysql.connect_database("ds_ftu")
        self.fg_color = "#faebd7"
        self.window_width = 414
        self.window_height = 896
        self.text_color = "black"
        self.main_font = "Helvetica"
        self.today = datetime.strptime('2023-09-12','%Y-%m-%d')
        try:
            config = Config('./OCR/tool/config/configs.yaml')
            self.ocr_pipeline = OCRPipeline(output = "./result_images",
                                            config = config)
            print("OCR modules loading completed")
        except Exception as error:
            print("OCR modules loading failed due to", error)

        try:
            self.nlu_pipeline = NLUPipeLine("./NLP/models/nlu_model_v1.json",
                                            "./NLP/models/nlu_weights_v1.h5",
                                            "./NLP/models/tokenizer_v1.pickle")
            print("NLU modules loading completed")
        except Exception as error:
            print("NLU modules loading failed due to", error)

        fb_logo = ctk.CTkImage(Image.open("./gui_images/logo/facebook.png"), size = (20,20))
        google_logo = ctk.CTkImage(Image.open("./gui_images/logo/google.png"), size = (20,20))
        apple_logo = ctk.CTkImage(Image.open("./gui_images/logo/apple.png"), size = (20,20))

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        
        self.root = ctk.CTk()
        main_logo = PhotoImage(file = "./gui_images/logo/main_logo.png")
        self.root.iconphoto(False, main_logo)
        self.root.title("Budget Buddy")
        

        login_frame = ctk.CTkFrame(self.root, 
                                   width = self.window_width, 
                                   height = self.window_height, 
                                   fg_color = self.fg_color)
        login_frame.grid(row = 0, column = 0)
        login_frame.grid_propagate(False)
        

        login_text = ctk.CTkLabel(login_frame, 
                     text = "LOGIN", 
                     fg_color = "#4f7942", 
                     width = self.window_width, 
                     height = 20,
                     text_color = "white",
                     corner_radius = 10,
                     font = (self.main_font, 30),
                     pady = 80)
        login_text.grid(pady = (0, 35), row = 0, column = 0)
    
        

        #Login box
        login_box = ctk.CTkFrame(login_frame,
                                 fg_color = self.fg_color,
                                 width = 300,
                                 height = 500)
        login_box.grid(row = 1, column = 0, pady = 35)


        email_text = ctk.CTkLabel(login_box, 
                                  text = "Email",
                                  text_color = self.text_color,
                                  font = (self.main_font, 13))
        email_text.grid(row = 0, column = 0, padx = (0, 180))

        self.email_box = ctk.CTkEntry(login_box,
                                 width = 230,
                                 height = 35)
        self.email_box.grid(row = 1, column = 0, pady = (0, 10))
       

        password_text = ctk.CTkLabel(login_box, 
                                  text = "Password",
                                  text_color = self.text_color,
                                  font = (self.main_font, 13))
        password_text.grid(row = 3, column = 0, padx = (0, 165))

        self.password_box = ctk.CTkEntry(login_box,
                                    width = 230,
                                    height = 35,
                                    show = "*")
        self.password_box.grid(row = 4, column = 0)
       

        forget_password_text = ctk.CTkLabel(login_box, 
                                  text = "Forget Your Password",
                                  text_color = self.text_color,
                                  font = (self.main_font, 11))
        forget_password_text.grid(row = 5, column = 0, padx = (0, 120), pady = (0, 10))

        login_button = ctk.CTkButton(login_box,
                                     text = "LOGIN",
                                     fg_color = "#507d2a",
                                     font = (self.main_font, 11),
                                     hover =True,
                                     corner_radius = 20,
                                     width = 80,
                                     command = self.check_login)
        login_button.grid(row = 6, column = 0, pady = 10)
        
        register_button = ctk.CTkButton(login_box,
                                     text = "SIGN UP",
                                     fg_color = "#507d2a",
                                     font = (self.main_font, 11),
                                     hover =True,
                                     corner_radius = 20,
                                     width = 90,
                                     command = self.register_frame)
        register_button.grid(row = 7, column = 0)

        ctk.CTkLabel(login_box, 
                    text = "OR",
                    text_color = self.text_color,
                    font = (self.main_font, 11)).grid(row = 8, column = 0, pady = 10)
        
        facebook_button = ctk.CTkButton(login_box,
                                     text = "Login with Facebook",
                                     fg_color = "#2a52be",
                                     font = (self.main_font, 13),
                                     corner_radius = 20,
                                     width = 230,
                                     height = 35,
                                     hover = False,
                                     image = fb_logo,
                                     compound = "left",
                                     border_spacing = 3)
        facebook_button.grid(row = 9, column = 0, pady = (10, 5))

        google_button = ctk.CTkButton(login_box,
                                     text = "Login with Google",
                                     fg_color = "white",
                                     text_color = self.text_color,
                                     font = (self.main_font, 13),
                                     corner_radius = 20,
                                     width = 230,
                                     height = 35,
                                     hover = False,
                                     image = google_logo,
                                     compound = "left",
                                     border_spacing = 4)
        google_button.grid(row = 10, column = 0, pady = 5)

        apple_button = ctk.CTkButton(login_box,
                                     text = "Login with Apple",
                                     fg_color = "white",
                                     text_color = self.text_color,
                                     font = (self.main_font, 13),
                                     corner_radius = 20,
                                     width = 230,
                                     height = 35,
                                     hover = False,
                                     image = apple_logo,
                                     compound = "left",
                                     border_spacing = 5)
        apple_button.grid(row = 11, column = 0, pady = 5)
            
        self.root.mainloop()

    def check_login(self):
        regis_dict = {"admin": {"password": "1", "user_name": "admin"}
        }
        self.user_email = self.email_box.get()
        self.user_password = self.password_box.get()
        if self.user_email in regis_dict:
            if self.user_password == regis_dict[self.user_email]["password"]:
                self.user_name = regis_dict[self.user_email]["user_name"]
                self.main_frame()
            else:
                print("Your password is incorrect")
        else: 
            print("You are not registed")

    def get_plot_option(self, option):
        self.plot_option = option
        
    def plot_main_frame(self, date, amount, master):
        fig = Figure(figsize = (7, 7),
                 dpi = 100)
        fig.patch.set_facecolor(self.fg_color)

        ax = fig.add_subplot(111)
        ax.plot(date, amount, color = "#445435", marker = "o")
        ax.set_facecolor(self.fg_color)
        ax.set_title("Chi Tiêu")
        ax.set_ylabel("Nghìn VND")
        ax.fill_between(date, amount, np.zeros(len(date)), color = "#CEDEBD", interpolate = True, alpha = 0.5)
        for key, spine in ax.spines.items():
            spine.set_visible(False)

        canvas = FigureCanvasTkAgg(fig,
                               master = master)  
        canvas.draw()
        canvas.get_tk_widget().pack()

    def plot_expense_frame(self, master, amount, labels):

        self.pie_color_dict = {"thực phẩm": "#2D87BB",
                      "gia dụng": "#64C2A6",
                      "phương tiện đi lại": "#AADEA7",
                      "y tế": "#E6F69D",
                      "giáo dục": "#FEAE65",
                      "khác": "#F66D44",
                      "None": "#67C587"}
        colors = []
        for label in labels:
            colors.append(self.pie_color_dict[label])
        
        fig = Figure(figsize = (9, 9),
                 dpi = 100)
        fig.patch.set_facecolor(self.fg_color)

        ax = fig.add_subplot(111)
        ax.pie(x = amount, 
               colors = colors, 
               radius = 1.5, 
               shadow = True,
               autopct='%1.1f%%')

        canvas = FigureCanvasTkAgg(fig,
                               master = master)  
        canvas.draw()
        canvas.get_tk_widget().pack(side = TOP, anchor = W)

    def legends_expense_frame(self, master, label, amount, percentage):

        legend = ctk.CTkFrame(master,
                               width = 310,
                               height = 90,
                               fg_color = self.pie_color_dict[label]
                               )
        legend.pack()
        legend.grid_propagate(False)
        legend.columnconfigure(0, weight=1)
        legend.columnconfigure(0, weight=4)

        if label == "thực phẩm": icon = ctk.CTkImage(Image.open("./gui_images/icons/food.png"), size = (50, 50))
        elif label == "gia dụng": icon = ctk.CTkImage(Image.open("./gui_images/icons/housing.png"), size = (50, 50))
        elif label == "phương tiện đi lại": 
            icon = ctk.CTkImage(Image.open("./gui_images/icons/car.png"), size = (50, 50))
            label = "phương tiện"
        elif label == "y tế": icon = ctk.CTkImage(Image.open("./gui_images/icons/pharmacy.png"), size = (50, 50))
        elif label == "giáo dục": icon = ctk.CTkImage(Image.open("./gui_images/icons/education.png"), size = (50, 50))
        else: icon = ctk.CTkImage(Image.open("./gui_images/icons/other.png"), size = (50, 50))

        legend_text = ctk.CTkLabel(legend,
                                     width = 100,
                                     height = 50,
                                     text = f"{amount}({percentage}%)",
                                     text_color = "black",
                                     font = (self.main_font, 23))
        legend_text.grid(row = 0, column = 1, sticky = E, pady = 10, padx = 20)

        legend_icon = ctk.CTkLabel(legend,
                                   width = 60, 
                                   height = 60,
                                   image = icon,
                                   text = label.title(),
                                   compound = 'top',
                                   font = (self.main_font, 12),
                                   wraplength = 90)
        legend_icon.grid(row = 0, column = 0, sticky = W, pady = 10, padx = 20)

    def format_date(self, date):
        if date == self.today: return "Hôm nay"
        else:
            return date.strftime("%d/%m/%y")
        
    def expense_frame_back_date(self):
        self.current_app_day -= timedelta(days = 1)
        self.expenses_frame(self.current_app_day)

    def expense_frame_next_date(self):
        self.current_app_day += timedelta(days = 1)
        self.expenses_frame(self.current_app_day)
    
    def function_buttons(self, master, row = 0, column = 0, padx = 0, pady = 0, columnspan = 0):
        expences_img = ctk.CTkImage(Image.open("./gui_images/buttons/expense.png"), size = (40,40))
        account_img = ctk.CTkImage(Image.open("./gui_images/buttons/account.png"), size = (40,40))
        income_img = ctk.CTkImage(Image.open("./gui_images/buttons/income.png"), size = (40,40))
        setting_img = ctk.CTkImage(Image.open("./gui_images/buttons/setting.png"), size = (40,40))
        pad_x = 24
        pad_y = 6
        fg_color = "#F9F1D0"
        function_frame = ctk.CTkFrame(master, 
                                   width = self.window_width, 
                                   height = 80, 
                                   fg_color = fg_color)
        function_frame.grid(row = row, column = column, padx = padx, pady = pady, columnspan = columnspan, sticky = S)
        function_frame.grid_propagate(False)

        expense_button = ctk.CTkButton(function_frame,
                                       image = expences_img,
                                       width = 45,
                                       height = 45,
                                       hover = False,
                                       fg_color = "#F9F1D0",
                                       text = "",
                                       border_width = 0,
                                       command = lambda: self.expenses_frame(self.today))
        
        expense_button.grid(row = 0, column = 0, pady = (pad_y, 0), padx = pad_x)

        expense_text = ctk.CTkLabel(function_frame,
                                    text = "Chi tiêu",
                                    text_color = "#8FA37D",
                                    font = (self.main_font, 13),
                                    fg_color = "#F9F1D0",
                                    height = 5)
        
        expense_text.grid(row = 1, column = 0, padx = pad_x)
        
        account_button = ctk.CTkButton(function_frame,
                                       image = account_img,
                                       width = 45,
                                       height = 45,
                                       hover = False,
                                       fg_color = "#F9F1D0",
                                       text = "",
                                       border_width = 0,
                                       command = self.account_frame)
        
        account_button.grid(row = 0, column = 1, pady = (pad_y, 0), padx = pad_x)

        account_text = ctk.CTkLabel(function_frame,
                                    text = "Ví cá nhân",
                                    text_color = "#8FA37D",
                                    font = (self.main_font, 13),
                                    fg_color = "#F9F1D0",
                                    height = 5)
        
        account_text.grid(row = 1, column = 1, padx = pad_x)

        income_button = ctk.CTkButton(function_frame,
                                       image = income_img,
                                       width = 45,
                                       height = 45,
                                       hover = False,
                                       fg_color = "#F9F1D0",
                                       text = "",
                                       border_width = 0,
                                       command = self.income_frame)
        
        income_button.grid(row = 0, column = 3, pady = (pad_y, 0), padx = pad_x)

        income_text = ctk.CTkLabel(function_frame,
                                    text = "Thu nhập",
                                    text_color = "#8FA37D",
                                    font = (self.main_font, 13),
                                    fg_color = "#F9F1D0",
                                    height = 5)
        
        income_text.grid(row = 1, column = 3, padx = pad_x)

        setting_button = ctk.CTkButton(function_frame,
                                       image = setting_img,
                                       width = 45,
                                       height = 45,
                                       hover = False,
                                       fg_color = "#F9F1D0",
                                       text = "",
                                       border_width = 0,
                                       command = self.setting_frame)
        
        setting_button.grid(row = 0, column = 4, pady = (pad_y, 0), padx = pad_x)

        setting_text = ctk.CTkLabel(function_frame,
                                    text = "Cài đặt",
                                    text_color = "#8FA37D",
                                    font = ("Calibri", 13),
                                    fg_color = "#F9F1D0",
                                    height = 5)
        
        setting_text.grid(row = 1, column = 4, padx = pad_x)


    def main_back_button(self, master, before_frame, row = 0, column = 0, columnspan = 1): 
        back_button = ctk.CTkButton(master,
                                    width = 40,
                                    height = 40,
                                    text = "",
                                    hover = False,
                                    image = self.back_arrow,
                                    fg_color = self.fg_color,
                                    command = before_frame)
        back_button.grid(row = 0, column = 0, sticky = NW, padx = 5, pady = 5, columnspan = columnspan)

    def expense_input_function_buttons(self, master, frame_name, padx = 0, pady = 0):
        types = ["NLP", "Bill Scan", "Voice"]

        for i, type_ in enumerate(types):
            if type_ == "NLP": function = self.NLP_frame
            elif type_ == "Bill Scan": function = self.OCR_frame
            else: function = self.voice_frame

            if type_ == frame_name:
                button_i = ctk.CTkButton(master,
                                   width = 100,
                                   height = 25,
                                   text = type_,
                                   fg_color = "#5E7449",
                                   text_color = "white",
                                   font = (self.main_font, 15),
                                   hover = False)
                button_i.grid(row = 1, column = i + 1, padx = padx, pady = pady)
            
            else:
                button_i = ctk.CTkButton(master,
                                   width = 100,
                                   height = 25,
                                   text = type_,
                                   fg_color = "#D9D9D9",
                                   text_color = "black",
                                   font = (self.main_font, 15),
                                   hover = False,
                                   command = function)
                button_i.grid(row = 1, column = i + 1, padx = padx, pady = pady)

    def chat_bubble(self, master, from_user, text, row = 0, column = 0, pady = 0, padx = 0):
        bot_box_color = "#DCE8FF"
        user_box_color = "#4399FF"
        if from_user == False:
            bot_avatar = ctk.CTkLabel(master,
                                    image = self.bot_ava,
                                    height = 40,
                                    width = 40,
                                    text = "",
                                    fg_color = "white")
            bot_avatar.grid(row = row, column = column, sticky = S, padx = padx, pady = pady)

            bot_text = ctk.CTkLabel(master,
                                    text = text,
                                    width = 200,
                                    height = 50,
                                    wraplength = 200,
                                    font = (self.main_font, 15),
                                    fg_color = bot_box_color,
                                    corner_radius = 10)
            bot_text.grid(row = row, column = column + 1, rowspan = 1, sticky = NW, padx = padx, pady = pady)

        else:
            self.user_input_expense_nlu = [text]
            user_avatar = ctk.CTkLabel(master,
                                    image = self.user_ava,
                                    height = 40,
                                    width = 40,
                                    text = "",
                                    fg_color = "white")
            user_avatar.grid(row = row, column = column, sticky = S, padx = padx, pady = pady)

            user_text = ctk.CTkLabel(master,
                                    text = text,
                                    width = 200,
                                    height = 50,
                                    wraplength = 200,
                                    font = (self.main_font, 15),
                                    fg_color = user_box_color,
                                    corner_radius = 10)
            user_text.grid(row = row, column = column - 1, rowspan = 1, sticky = NE, padx = padx, pady = pady)

            self.chat_bubble(master,
                             from_user = False, text = "Cảm ơn bạn đã nhập thông tin, xin vui lòng xác nhận lại",
                             row = row + 1, column = column - 2, pady = 10)

            output = text_classifier_final.Classify(self.nlu_pipeline.start(self.user_input_expense_nlu))
            self.confirm_popup(output)
        
    def display_image(self, master, filename): 

        if filename:
            image = ctk.CTkImage(Image.open(filename), size = (300 ,500))
            ctk.CTkLabel(master,
                         text = "",
                         image = image).pack()
    def get_image_and_process(self, filename):
        ocr_input = cv2.imread(filename)
        self.ocr_result = text_classifier_final.Classify(self.ocr_pipeline.start(ocr_input))
        self.confirm_popup(self.ocr_result)

    def manually_expense_icon_display(self, master, label, current = False, row = 0, column = 0):
        mapping = {"thực phẩm": self.food_icon,
                   "gia dụng": self.housing_icon,
                   "phương tiện đi lại": self.car_icon,
                   "y tế": self.medical_icon,
                   "giáo dục": self.education_icon,
                   "khác": self.other_icon}
        
        if label == "phương tiện đi lại": text = "phương tiện"
        else: text = label
        if current:
            ctk.CTkButton(master,
                        width = 40,
                        height = 40,
                        image = mapping[label],
                        hover = False,
                        text = text.title(),
                        compound = "top",
                        fg_color = "#67C587").grid(column = column, row = row, pady = 20, padx = 20)
            self.current_expense_type = label
        else:
            ctk.CTkButton(master,
                        width = 40,
                        height = 40,
                        image = mapping[label],
                        hover = False,
                        text = text.title(),
                        compound = "top",
                        fg_color = "#D9D9D9",
                        command = lambda: self.manually_expense_icon_display(master, label, True, row = row, column = column)).grid(column = column, row = row, pady = 20, padx = 20)

    def submit_expense_manually(self):
        date = self.date_input_box_expense.get()
        description = self.note_input_box_expense.get()
        amount = self.price_input_box_expense.get()

        query = f"""
                INSERT INTO spending(date, description, amount, type)
                VALUES ('{date}', '{description}', {amount}, '{self.current_expense_type}');
                """
        try:    
            self.mysql.execute_query(query)
        
            confirm_popup = messagebox.showinfo("Xác nhận", "Thông tin của bạn đã được nhập")
            self.manually_expense_frame()
        except:
            confirm_popup = messagebox.showinfo("Xác nhận", "Không thành công hãy thử lại")

    def submit_income(self):
        date = self.date_input_box_income.get()
        description = self.note_input_box_income.get()
        amount = self.price_input_box_income.get()

        query = f"""
                INSERT INTO income(date, description, amount)
                VALUES ('{date}', '{description}', {amount});
                """
        try:    
            self.mysql.execute_query(query)
        
            confirm_popup = messagebox.showinfo("Xác nhận", "Thông tin của bạn đã được nhập")
            self.income_frame()
        except:
            confirm_popup = messagebox.showinfo("Xác nhận", "Không thành công hãy thử lại")

    def submit_popup(self, data):
        query = f"""
                INSERT INTO spending(date, description, amount, type)
                VALUES (%s, %s, %s, %s);
                """
        val = transform_data.transform_data(data)
        self.mysql.execute_list_query(query, val)
        self.pop_up.withdraw()

    def confirm_popup(self, data):
        columns = ["Mô tả", "Hạng mục", "Số tiền"]

        self.pop_up = ctk.CTkToplevel(fg_color = self.fg_color)
        self.pop_up.geometry("350x600")

        date = data["date"]
        products = data["products"]

        date_label = ctk.CTkLabel(self.pop_up,
                                  text = date,
                                  width = 350,
                                  height = 50,
                                  font = (self.main_font, 25))
        date_label.pack()
        columns_name_frame = ctk.CTkFrame(self.pop_up,
                                          width = 350,
                                          height = 50,
                                          fg_color = self.fg_color)
        columns_name_frame.pack()
        columns_name_frame.columnconfigure(0, weight = 1)
        columns_name_frame.columnconfigure(1, weight = 1)
        columns_name_frame.columnconfigure(2, weight = 1)
        columns_name_frame.grid_propagate(False)

        for i, column in enumerate(columns):
            ctk.CTkLabel(columns_name_frame,
                         text = column,
                         height = 45,
                         width = 100,
                         font = (self.main_font, 15),
                         fg_color = "grey").grid(row = 0, column = i, padx = 10)
            

        data_frame = ctk.CTkScrollableFrame(self.pop_up,
                                            width = 350,
                                            height = 400,
                                            )
        data_frame.pack()

        data_frame.columnconfigure(0, weight = 1)
        data_frame.columnconfigure(1, weight = 1)
        data_frame.columnconfigure(2, weight = 1)

        for i, product in enumerate(products):
            des = ctk.CTkEntry(data_frame,
                         height  = 45,
                         width = 120,
                         font = (self.main_font, 15))
            des.insert(0, product["description"])
            des.grid(row = i, column = 0, pady = 10)
            
            type_ = ctk.CTkEntry(data_frame,
                         height  = 45,
                         width = 100,
                         font = (self.main_font, 15))
            
            type_.insert(0, product["type"])
            type_.grid(row = i, column = 1, pady = 10)
            
            amount = ctk.CTkEntry(data_frame,
                         height  = 45,
                         width = 80,
                         font = (self.main_font, 15))
            amount.grid(row = i, column = 2, pady = 10)
            amount.insert(0, product["amount"])

        submit_button = ctk.CTkButton(self.pop_up,
                                      width = 100,
                                      height = 50,
                                      text = "Xác Nhận",
                                      command = lambda: self.submit_popup(data))
        submit_button.pack(pady = 10)
    def main_frame(self):
        """
        Master frame: main_frame
        Child frame: [top_frame, current_balance_frame, checkbox_frame, plot_frame, function_frame]
        """

        self.day = 1
        self.total_balance = 10000000
        self.daily_check = {"Mon": None,
                            "Tue": None,
                            "Wed": None,
                            "Thu": None,
                            "Fri": None,
                            "Sat": None,
                            "Sun": None}
        self.bot_ava = ctk.CTkImage(Image.open("./gui_images/avatar/chatbot.png"), size = (30,30))
        self.user_ava = ctk.CTkImage(Image.open("./gui_images/avatar/user.png"), size = (30,30))
        self.back_arrow = ctk.CTkImage(Image.open("./gui_images/buttons/main_back_arrow.png"), size = (40,40))
        checked_checkbox = ctk.CTkImage(Image.open("./gui_images/checkboxes/checked_checkbox_2.png"), size = (15,15))
        unchecked_checkbox = ctk.CTkImage(Image.open("./gui_images/checkboxes/unchecked_checkbox.png"), size = (8,8))
        noti_bell = ctk.CTkImage(Image.open("./gui_images/noti_bell/noti_bell.png"), size = (40,40))
        self.plot_dropdown = ["Hằng Ngày", "Hằng Tuần", "Hằng Tháng"]
        self.plot_option = "Hằng Ngày"


        plot_date, plot_amount = self.mysql.get_annually_spending(freq = self.plot_option,
                                                                  from_ = "2023-09-12",
                                                                  to = "2023-09-18")
        for day in self.daily_check:
            if day in plot_date:
                self.daily_check[day] = True
            else: self.daily_check[day] = False

        main_frame = ctk.CTkFrame(self.root, 
                                   width = self.window_width, 
                                   height = self.window_height, 
                                   fg_color = self.fg_color)
        main_frame.grid(row = 0, column = 0)
        main_frame.grid_propagate(False)

        top_frame = ctk.CTkFrame(main_frame,
                                 width = self.window_width,
                                 height = 130,
                                 corner_radius = 10,
                                 fg_color = "#4f7942")
        top_frame.grid(row = 0, column = 0, pady = (0, 10))
        top_frame.grid_propagate(False)

        hello_text = ctk.CTkLabel(top_frame, 
                     text = f"Xin Chào, {self.user_name}", 
                     fg_color = "#4f7942", 
                    #  width = self.window_width, 
                    #  height = 20,
                    text_color = "white",
                    #  corner_radius = 10,
                    font = ("Calibri", 30))
                    #  pady = 80,
                    #  anchor = "w",
                    #  justify = "left")
        hello_text.grid(padx = (30, 10), pady = 40, row = 0, column = 0)

        noti_bell = ctk.CTkButton(top_frame,
                                  image = noti_bell,
                                  text = "",
                                  border_spacing = 0,
                                  height = 30,
                                  width = 30,
                                  fg_color = "#4f7942",
                                  hover = False)
        noti_bell.grid(row = 0, column = 1, padx = (70, 0), pady = 40)
        
        
        #Current Balance Box
        current_balance_frame = ctk.CTkFrame(main_frame,
                                       width = 350,
                                       height = 100,
                                       fg_color = "white",
                                       corner_radius = 30)
        current_balance_frame.grid(row = 1, column = 0, pady = 10)
        current_balance_frame.pack_propagate(False)

        current_balance_text = ctk.CTkLabel(current_balance_frame,
                                            text = "Số Dư Tài Khoản",
                                            text_color = "#5D7B41",
                                            font = ("Calibri", 15),
                                            anchor = "w",
                                            justify = "left"
                                            )
    
        current_balance_text.pack(side=TOP, anchor=NW, padx = 20, pady = 5)

        current_balance_number = ctk.CTkLabel(current_balance_frame,
                                            text = f"{self.total_balance} VND",
                                            text_color = "#5D7B41",
                                            font = ("Calibri", 25),
                                            anchor = "center")
        current_balance_number.pack()

        update_text = ctk.CTkLabel(current_balance_frame,
                                   text = f"Cập nhật {self.day} ngày trước",
                                   text_color = "grey",
                                   font = ("Calibri", 10))
        update_text.pack()

        daily_text = ctk.CTkLabel(main_frame,
                                   text = "Điểm Danh Hằng Ngày",
                                   text_color = "#5D7B41",
                                   font = ("Calibri", 15))
        
        daily_text.grid(column = 0, row = 2, pady = (20, 0))

        #Check box
        checkbox_frame = ctk.CTkFrame(main_frame,
                                       width = 265,
                                       height = 60,
                                       fg_color = self.fg_color,
                                       corner_radius = 30)
        checkbox_frame.grid(row = 3, column = 0)
        checkbox_frame.grid_propagate(False)
    

        for i, day in enumerate(self.daily_check):
            #Place text
            ctk.CTkLabel(checkbox_frame,
                         text = day,
                         text_color = "grey",
                         font = ("Calibri", 13)).grid(row = 1, column = i, padx = 8)
            
            #Place the checkmark based on value of self.dailycheck[day]
            if self.daily_check[day]:
                ctk.CTkLabel(checkbox_frame,
                            image = checked_checkbox,
                            text = "").grid(row = 2, column = i, pady = 3)
                
            else: 
                ctk.CTkLabel(checkbox_frame,
                            image = unchecked_checkbox,
                            text = "").grid(row = 2, column = i)

        #Plot
        plot_frame = ctk.CTkFrame(main_frame,
                                  fg_color = self.fg_color,
                                  height = 239,
                                  width = 350)
        plot_frame.grid(row = 4, column = 0, pady = (10, 5))
        plot_frame.pack_propagate(False)

        drop_down_plot = ctk.CTkOptionMenu(plot_frame,
                                           values = self.plot_dropdown,
                                           command = self.get_plot_option,
                                           width = 100,
                                           height = 15,
                                           fg_color = "#445435",
                                           text_color = "white",
                                           dropdown_fg_color = self.fg_color,
                                           font = ("Calibri", 13))
        drop_down_plot.pack(side=TOP, anchor=NE, pady = 5, padx = 5)

        self.plot_main_frame(plot_date, plot_amount, plot_frame)

        #Function bar
        self.function_buttons(main_frame, row = 5, columnspan = 2)

    def register_frame(self):
        register_frame = ctk.CTkFrame(self.root, 
                                   width = self.window_width, 
                                   height = self.window_height, 
                                   fg_color = self.fg_color)
        register_frame.grid(row = 0, column = 0)
        register_frame.grid_propagate(False)

        register_text = ctk.CTkLabel(register_frame, 
                     text = "LOGIN", 
                     fg_color = "#4f7942", 
                     width = self.window_width, 
                     height = 20,
                     text_color = "white",
                     corner_radius = 10,
                     font = ("Calibri", 30),
                     pady = 80)
        register_text.grid(pady = (0, 35), row = 0, column = 0)
    
    def expenses_frame(self, day):
        self.current_app_day = day
        small_back_arrow = ctk.CTkImage(Image.open("./gui_images/buttons/small_arrow.png"), size = (20,20))
        small_next_arrow = ctk.CTkImage(Image.open("./gui_images/buttons/small_arrow.png").transpose(Image.FLIP_LEFT_RIGHT), size = (20,20))


        amount, labels = self.mysql.get_daily_expenses_by_type(self.current_app_day)

        main_expenses = ctk.CTkFrame(self.root, 
                                   width = self.window_width, 
                                   height = self.window_height, 
                                   fg_color = self.fg_color)
        main_expenses.grid(row = 0, column = 0)
        main_expenses.grid_propagate(False)


        self.main_back_button(main_expenses, self.main_frame)

        frame_title = ctk.CTkLabel(main_expenses,
                                   width = 200,
                                   height = 40,
                                   text = "Chi Tiêu",
                                   fg_color = self.fg_color,
                                   font = (self.main_font, 27),
                                   text_color = "#445435")
        frame_title.grid(row = 0, column = 1, columnspan = 3, padx = (0, 50))

        ai_data_input = ctk.CTkButton(main_expenses,
                                      width = 150,
                                      height = 25,
                                      text = "Tự động",
                                      hover = False,
                                      fg_color = "#D9D9D9",
                                      font = (self.main_font, 14),
                                      text_color = "black",
                                      command = self.NLP_frame)
        ai_data_input.grid(row = 1, column = 1, columnspan = 1)

        manual_data_input = ctk.CTkButton(main_expenses,
                                      width = 150,
                                      height = 25,
                                      text = "Thủ công",
                                      hover = False,
                                      fg_color = "#D9D9D9",
                                      font = (self.main_font, 14),
                                      text_color = "black",
                                      command = self.manually_expense_frame)
        manual_data_input.grid(row = 1, column = 2, padx = (0, 40))

        padding_frame = ctk.CTkFrame(main_expenses,
                                     width = 60,
                                     height = 10,
                                     fg_color = self.fg_color)
        padding_frame.grid(row = 1, column = 4, padx = (0, 5))

        display_date_frame = ctk.CTkFrame(main_expenses,
                                          width = 200,
                                          height = 50,
                                          fg_color = "#D9D9D9",
                                          corner_radius = 30)
        
        display_date_frame.grid(row = 2, column = 1, columnspan = 3, pady = (15, 0), padx = (0, 55))
        display_date_frame.grid_propagate(False)

        current_day_text = ctk.CTkLabel(display_date_frame,
                                        text = self.format_date(self.current_app_day),
                                        text_color = "#445435",
                                        fg_color = "#D9D9D9",
                                        height = 40,
                                        width = 100,
                                        font = (self.main_font, 20))
        current_day_text.grid(row = 0, column = 1, padx = (10, 0), pady = 3)

        day_back_arrow = ctk.CTkButton(display_date_frame,
                                       text = "",
                                       image = small_back_arrow,
                                       height = 20,
                                       width = 20,
                                       fg_color = "#D9D9D9",
                                       hover = False,
                                       command = self.expense_frame_back_date)
        
        day_back_arrow.grid(row = 0, column = 0, pady = 3, padx = (5, 0))

        if self.current_app_day != self.today:
            day_next_arrow = ctk.CTkButton(display_date_frame,
                                        text = "",
                                        image = small_next_arrow,
                                        height = 20,
                                        width = 20,
                                        fg_color = "#D9D9D9",
                                        hover = False,
                                        command = self.expense_frame_next_date)
            
            day_next_arrow.grid(row = 0, column = 3, pady = 3, padx = (5, 0))

        #Plot frame
        plot_frame = ctk.CTkFrame(main_expenses,
                                  fg_color = "white",
                                  height = 180,
                                  width = 400)
        plot_frame.grid(row = 3, column = 0, columnspan = 4, padx = (7, 0))
        plot_frame.pack_propagate(False)

        self.plot_expense_frame(plot_frame, amount, labels)

        #Legend frame
        legend_frame = ctk.CTkScrollableFrame(main_expenses,
                                  fg_color = self.fg_color,
                                  height = 280,
                                  width = 330)
        legend_frame.grid(row = 4, column = 0, columnspan = 4, padx = 7)
        
        #Calculate pertentage
        
        percentage = calculate_percentage.calculate_percentage(amount, 1)


        for i, label in enumerate(labels):
            self.legends_expense_frame(legend_frame,
                                    label,
                                    amount = amount[i],
                                    percentage = percentage[i])
        #Function buttons
        self.function_buttons(main_expenses,
                              row = 5,
                              columnspan = 4)

    def account_frame(self):
        pass

    def income_frame(self):
        
        main_income_frame = ctk.CTkFrame(self.root, 
                                   width = self.window_width, 
                                   height = self.window_height, 
                                   fg_color = self.fg_color)
        main_income_frame.grid(row = 0, column = 0)
        main_income_frame.grid_propagate(False)
        main_income_frame.columnconfigure(0, weight = 1)
        main_income_frame.columnconfigure(1, weight = 3)
        main_income_frame.columnconfigure(2, weight = 1)
        
        self.main_back_button(main_income_frame, self.main_frame, columnspan = 2)
        frame_title = ctk.CTkLabel(main_income_frame,
                                   text = "Thu Nhập",
                                   height = 40,
                                   width = 100,
                                   font = (self.main_font, 20),
                                   text_color = "#445435")
        frame_title.grid(row = 0, column = 1)

        #Input frame
        input_frame = ctk.CTkFrame(main_income_frame,
                                   width = 350,
                                   height = 180,
                                   fg_color = self.fg_color)
        input_frame.grid(row = 1, column = 1)
        input_frame.grid_propagate(False)

        date_input_text = ctk.CTkLabel(input_frame,
                                  width = 100,
                                  height = 30,
                                  fg_color = self.fg_color,
                                  text = "Ngày",
                                  font = (self.main_font, 20),
                                  text_color = "#445435")
        date_input_text.grid(row = 0, column = 0, sticky = NW, padx = 10, pady = 10)

        self.date_input_box_income = ctk.CTkEntry(input_frame,
                                      width = 200,
                                      height = 30,
                                      fg_color = "#D9D9D9")
        self.date_input_box_income.grid(row = 0, column = 1, sticky = NE, padx = 10, pady = 10)

        note_input_text = ctk.CTkLabel(input_frame,
                                  width = 100,
                                  height = 30,
                                  fg_color = self.fg_color,
                                  text = "Mô tả",
                                  font = (self.main_font, 20),
                                  text_color = "#445435")
        note_input_text.grid(row = 1, column = 0, sticky = NW, padx = 10, pady = 15)

        self.note_input_box_income = ctk.CTkEntry(input_frame,
                                      width = 200,
                                      height = 30,
                                      fg_color = "#D9D9D9")
        self.note_input_box_income.grid(row = 1, column = 1, sticky = NE, padx = 10, pady = 15)

        price_input_text = ctk.CTkLabel(input_frame,
                                  width = 100,
                                  height = 30,
                                  fg_color = self.fg_color,
                                  text = "Số tiền",
                                  font = (self.main_font, 20),
                                  text_color = "#445435")
        price_input_text.grid(row = 2, column = 0, sticky = NW, padx = 10, pady = 15)

        self.price_input_box_income = ctk.CTkEntry(input_frame,
                                      width = 200,
                                      height = 30,
                                      fg_color = "#D9D9D9")
        self.price_input_box_income.grid(row = 2, column = 1, sticky = NE, padx = 10, pady = 15)

        submit_button = ctk.CTkButton(main_income_frame,
                                      width = 90,
                                      height = 40,
                                      text = "Nhập",
                                      command = self.submit_income)
        submit_button.grid(row = 4, column = 1, pady = 10)

    def setting_frame(self):
        pass

    def NLP_frame(self):
        main_NLP = ctk.CTkFrame(self.root, 
                                   width = self.window_width, 
                                   height = self.window_height, 
                                   fg_color = self.fg_color)
        main_NLP.grid(row = 0, column = 0)
        main_NLP.grid_propagate(False)

        main_NLP.columnconfigure(0, weight = 1)
        main_NLP.columnconfigure(1, weight = 2)
        main_NLP.columnconfigure(2, weight = 2)
        main_NLP.columnconfigure(3, weight = 2)
        main_NLP.columnconfigure(4, weight = 1)


        self.main_back_button(main_NLP, lambda: self.expenses_frame(self.today))

        self.expense_input_function_buttons(main_NLP, "NLP")

        padding_frame = ctk.CTkFrame(main_NLP,
                                     width = 60,
                                     height = 10,
                                     fg_color = self.fg_color)
        padding_frame.grid(row = 0, column = 4, padx = (0, 5))

        boxchat_frame = ctk.CTkFrame(main_NLP,
                                     width = 400,
                                     height = 500,
                                     fg_color = self.fg_color)
        boxchat_frame.grid(row = 2, column = 0, columnspan = 5, sticky = EW, padx = (5, 0), pady =10)
        boxchat_frame.grid_propagate(False)
        
        boxchat_frame.columnconfigure(0, weight = 1)
        boxchat_frame.columnconfigure(1, weight = 4)
        boxchat_frame.columnconfigure(2, weight = 1)

        self.chat_bubble(boxchat_frame,
                         from_user = False,
                         text = "Xin hãy tâm sự với tôi về chi tiêu của bạn",
                         pady = 10,
                         row = 0,
                         column = 0)
        
        self.chat_bubble(boxchat_frame,
                         from_user = False,
                         text = "Hãy nói theo mẫu câu này để tôi có thể hiểu bạn tốt hơn",
                         pady = 10,
                         row = 1,
                         column = 0)

        self.chat_bubble(boxchat_frame,
                         from_user = False,
                         text = "Hôm nay tôi mua 50000 thịt bò. Hôm qua tôi mua hết 10000 rau (Ngăn cách các câu bằng dấu chấm)",
                         pady = 10,
                         row = 2,
                         column = 0)
        
        user_chat_box = ctk.CTkEntry(main_NLP,
                                     width = 300,
                                     height = 50
                                     )
        user_chat_box.grid(row = 3, column = 1, columnspan = 3)

        submit_button = ctk.CTkButton(main_NLP,
                                      width = 50,
                                       height = 50, 
                                       text = "Gửi",
                                       command = lambda: self.chat_bubble(boxchat_frame,
                                                                    from_user = True,
                                                                  text = user_chat_box.get(),
                                                                    column = 2,
                                                                    row = 3))
        submit_button.grid(row = 3, column = 4)
        
    def OCR_frame(self):
        main_OCR = ctk.CTkFrame(self.root, 
                                   width = self.window_width, 
                                   height = self.window_height, 
                                   fg_color = self.fg_color)
        main_OCR.grid(row = 0, column = 0)
        main_OCR.grid_propagate(False)
        
        main_OCR.columnconfigure(0, weight = 1)
        main_OCR.columnconfigure(1, weight = 2)
        main_OCR.columnconfigure(2, weight = 2)
        main_OCR.columnconfigure(3, weight = 2)
        main_OCR.columnconfigure(4, weight = 1)

        padding_frame = ctk.CTkFrame(main_OCR,
                                     width = 60,
                                     height = 10,
                                     fg_color = self.fg_color)
        padding_frame.grid(row = 0, column = 4, padx = (0, 5))

        self.main_back_button(main_OCR, lambda: self.expenses_frame(self.today))

        self.expense_input_function_buttons(main_OCR, "Bill Scan")

        capture_frame = ctk.CTkFrame(main_OCR,
                                     width = 300,
                                     height = 500,
                                     fg_color = "grey")
        
        capture_frame.grid(row = 2, column = 1, columnspan = 3, pady = 10)

        filename = filedialog.askopenfilename(initialdir=os.getcwd(),title="Select Image",filetypes=(("JPG",'*.jpg'),\
        ('PNG','*.png'),('all type','*.*')))
        self.display_image(capture_frame, filename)

        submit_button = ctk.CTkButton(main_OCR,
                                     width = 100,
                                     height = 50,
                                     hover = False,
                                     text = "Quét",
                                     command = lambda: self.get_image_and_process(filename))
        
        submit_button.grid(row = 3, column = 1, columnspan = 3)

    def voice_frame(self):
        record_icon = ctk.CTkImage(Image.open("./gui_images/buttons/microphone.png"), size = (150,150))
        green_circle = ctk.CTkImage(Image.open("./gui_images/buttons/green_circle.png"), size = (270, 270))
        sound_wave = ctk.CTkImage(Image.open("./gui_images/icons/sound_wave.png"), size = (300, 50))
        main_voice = ctk.CTkFrame(self.root, 
                                   width = self.window_width, 
                                   height = self.window_height, 
                                   fg_color = self.fg_color)
        main_voice.grid(row = 0, column = 0)
        main_voice.grid_propagate(False)

        main_voice.columnconfigure(0, weight = 1)
        main_voice.columnconfigure(1, weight = 2)
        main_voice.columnconfigure(2, weight = 2)
        main_voice.columnconfigure(3, weight = 2)
        main_voice.columnconfigure(4, weight = 1)

        padding_frame = ctk.CTkFrame(main_voice,
                                     width = 60,
                                     height = 10,
                                     fg_color = self.fg_color)
        padding_frame.grid(row = 0, column = 4, padx = (0, 5))

        self.main_back_button(main_voice, lambda: self.expenses_frame(self.today))

        self.expense_input_function_buttons(main_voice, "Voice")

        voice_title = ctk.CTkLabel(main_voice,
                                   text = "Hãy nói với tôi",
                                   text_color = "#445435",
                                   width = 250,
                                   height = 60,
                                   font = (self.main_font, 30))
        voice_title.grid(row = 2, column = 1, columnspan = 3)

        green_circle = ctk.CTkLabel(main_voice,
                                     text = "",
                                     width = 300,
                                     height = 300,
                                     image = green_circle)
        green_circle.grid(row = 3, column = 1, columnspan = 3)
        green_circle.pack_propagate(False)

        record_button = ctk.CTkButton(green_circle,
                                      text = "",
                                      width = 150,
                                       height = 150,
                                       image = record_icon,
                                       hover = False,
                                       fg_color = "#CEDEBD")
        record_button.pack(fill = "none", expand = True)

        sound_wave = ctk.CTkLabel(main_voice,
                                  width = 350, 
                                  height = 60,
                                  image = sound_wave,
                                  text = "",
                                  fg_color = self.fg_color)
        sound_wave.grid(row = 4, column = 1, columnspan = 3)

        voice_example = ctk.CTkLabel(main_voice,
                                     width = 350,
                                     height = 100,
                                     text = "VD: Hôm nay tôi mua năm mươi nghìn xăng",
                                     font = (self.main_font, 15))
        
        voice_example.grid(row = 5, column = 1, columnspan = 3)
        
    def manually_expense_frame(self):
        self.food_icon = ctk.CTkImage(Image.open("./gui_images/icons/food.png"), size = (40, 40))
        self.housing_icon = ctk.CTkImage(Image.open("./gui_images/icons/housing.png"), size = (40, 40))
        self.car_icon = ctk.CTkImage(Image.open("./gui_images/icons/car.png"), size = (40, 40))
        self.medical_icon = ctk.CTkImage(Image.open("./gui_images/icons/pharmacy.png"), size = (40, 40))
        self.education_icon =  ctk.CTkImage(Image.open("./gui_images/icons/education.png"), size = (40, 40))
        self.other_icon = ctk.CTkImage(Image.open("./gui_images/icons/other.png"), size = (40, 40))


        main_manualy_expense = ctk.CTkFrame(self.root, 
                                   width = self.window_width, 
                                   height = self.window_height, 
                                   fg_color = self.fg_color)
        main_manualy_expense.grid(row = 0, column = 0)
        main_manualy_expense.grid_propagate(False)
        main_manualy_expense.columnconfigure(0, weight = 1)
        main_manualy_expense.columnconfigure(1, weight = 3)
        main_manualy_expense.columnconfigure(2, weight = 1)

        self.main_back_button(main_manualy_expense, lambda: self.expenses_frame(self.today), columnspan = 2)

        #Input frame
        input_frame = ctk.CTkFrame(main_manualy_expense,
                                   width = 350,
                                   height = 180,
                                   fg_color = self.fg_color)
        input_frame.grid(row = 1, column = 1)
        input_frame.grid_propagate(False)

        date_input_text = ctk.CTkLabel(input_frame,
                                  width = 100,
                                  height = 30,
                                  fg_color = self.fg_color,
                                  text = "Ngày",
                                  font = (self.main_font, 20),
                                  text_color = "#445435")
        date_input_text.grid(row = 0, column = 0, sticky = NW, padx = 10, pady = 10)

        self.date_input_box_expense = ctk.CTkEntry(input_frame,
                                      width = 200,
                                      height = 30,
                                      fg_color = "#D9D9D9")
        self.date_input_box_expense.grid(row = 0, column = 1, sticky = NE, padx = 10, pady = 10)

        note_input_text = ctk.CTkLabel(input_frame,
                                  width = 100,
                                  height = 30,
                                  fg_color = self.fg_color,
                                  text = "Mô tả",
                                  font = (self.main_font, 20),
                                  text_color = "#445435")
        note_input_text.grid(row = 1, column = 0, sticky = NW, padx = 10, pady = 15)

        self.note_input_box_expense = ctk.CTkEntry(input_frame,
                                      width = 200,
                                      height = 30,
                                      fg_color = "#D9D9D9")
        self.note_input_box_expense.grid(row = 1, column = 1, sticky = NE, padx = 10, pady = 15)

        price_input_text = ctk.CTkLabel(input_frame,
                                  width = 100,
                                  height = 30,
                                  fg_color = self.fg_color,
                                  text = "Số tiền",
                                  font = (self.main_font, 20),
                                  text_color = "#445435")
        price_input_text.grid(row = 2, column = 0, sticky = NW, padx = 10, pady = 15)

        self.price_input_box_expense = ctk.CTkEntry(input_frame,
                                      width = 200,
                                      height = 30,
                                      fg_color = "#D9D9D9")
        self.price_input_box_expense.grid(row = 2, column = 1, sticky = NE, padx = 10, pady = 15)

        danhmuc_text = ctk.CTkLabel(main_manualy_expense,
                                    width = 100,
                                    height = 80,
                                    text = "Danh mục",
                                    text_color = "#445435",
                                    font = (self.main_font, 25))
        danhmuc_text.grid(row = 2, column = 1, sticky = W, pady = (20, 0))

        #Danh muc frame

        danhmuc_frame = ctk.CTkFrame(main_manualy_expense,
                                   width = 350,
                                   height = 250,
                                   fg_color = self.fg_color)
        danhmuc_frame.grid(row = 3, column = 1, pady = (0, 10))
        danhmuc_frame.grid_propagate(False)

        self.manually_expense_icon_display(danhmuc_frame, "thực phẩm")
        self.manually_expense_icon_display(danhmuc_frame, "gia dụng", row = 0, column = 1)
        self.manually_expense_icon_display(danhmuc_frame, "phương tiện đi lại", row = 0, column = 2)
        self.manually_expense_icon_display(danhmuc_frame, "y tế", row = 1, column = 0)
        self.manually_expense_icon_display(danhmuc_frame, "giáo dục", row = 1, column = 1)
        self.manually_expense_icon_display(danhmuc_frame, "khác", row = 1, column = 2)

        #Submit button
        submit_button = ctk.CTkButton(main_manualy_expense,
                                      width = 90,
                                      height = 40,
                                      text = "Nhập",
                                      command = self.submit_expense_manually)
        submit_button.grid(row = 4, column = 1, pady = 10)
if __name__ == "__main__":
    my_app = MyGUI()
    