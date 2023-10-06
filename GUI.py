from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk,ImageGrab
from tkinter import filedialog,messagebox
import os
import cv2

def import_image():
    
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),title="Select Image",filetypes=(("JPG",'*.jpg'),\
    ('PNG','*.png'),('all type','*.*')))
    if filename:
        img = cv2.imread(filename)
        print(img)

        # display image in newframe
        image_frame = Frame(main_screen)
        image_frame.pack()
        image_label = Label(image_frame, image=img)
        image_label.image = img
        image_label.pack()

def capture_frame_and_save():
    # save content in image coordinate to it's frame
    x = main_screen.winfo_rootx() + image_frame.winfo_x()
    y = main_screen.winfo_rooty() + image_frame.winfo_y()
    x1 = x + image_frame.winfo_width()
    y1 = y + image_frame.winfo_height()
    captured_image = ImageGrab.grab(bbox=(x, y, x1, y1))

#     # save pop up
#     file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")])

#     # success popup
#     if file_path:
#         captured_image.save(file_path)

#     messagebox.showinfo("Success", "Image saved successfully!")

#def get_text():
    #global expense_box
    #expense_text = expense_box.get('1.0','end-1c')
    #print(expense_text)

#def clear_text():
   # global expense_box
    #expense_box.delete('1.0','end')


def expense():
    global expense_box
    expense_window = Toplevel(main_screen)
    expense_window.title('Expense')
    expense_window.geometry("390x844")
    Label(expense_window, text=f"xxxxx", font=("Calibri", 15)).pack(pady=10)

    expense_submit = Button(expense_window, text="Import", width=10,command=import_image)
    expense_submit.pack(pady=10)

    expense_clear = Button(expense_window, text="Save", width=10,command=lambda: capture_frame_and_save())
    expense_clear.pack(pady=20)
    
def retrieve_input():
    inputValue=text_box.get("1.0",'end-1c')
    
def open_main_window():
    username = username_entry.get()
    login_window = Toplevel(main_screen)
    login_window.title("Main Window")
    login_window.geometry("390x844")
    
    options = ["By Day", "By Month", "By Year"]
    combo_var = StringVar()
    combo_var.set(options[0])
    combo_box = ttk.Combobox(login_window, values=options, textvariable=combo_var)
    combo_box.pack(pady=5)
    
    Label(login_window, text=f"Welcome, {username}!", font=("Calibri", 15)).pack(pady=10)
    #Expense Button
    expense_button = Button(login_window, text="Expenses", width=10,command = lambda: open_expense_window())
    expense_button.pack(pady=10)
    
    #Income Button
    expense_button = Button(login_window, text="Income", width=10)
    expense_button.pack(pady=10)
    
#NLP page
def open_NLP_window():
    global text_box
    global login_window
    username = username_entry.get()
    password = password_entry.get()

    login_window = Toplevel(main_screen)
    login_window.title("NLP Window")
    login_window.geometry("390x844")
    
    Label(login_window, text=f"Welcome, {username}!", font=("Calibri", 15)).pack(pady=10)


    combo_label = Label(login_window, text="Select an option:")
    combo_label.pack()
    
    text_label = Label(login_window, text="Enter text:")
    text_label.pack()
    text_box = Text(login_window, height=5, width=30)
    text_box.pack(pady=5)
    
    # Submit button
    NLP_submit_button = Button(login_window, text="Submit", width=10,command=lambda : retrieve_input())
    NLP_submit_button.pack(pady=10)

    #Button deposit
    

    # Daily checkin
    # check_var_mon = IntVar()
    # check_var_tue = IntVar()
    # check_var_wed = IntVar()
    # check_var_thu = IntVar()
    # check_var_fri = IntVar()
    # check_var_sat = IntVar()
    # check_var_sun = IntVar()
    
    # Checkbutton(login_window, text="Mon", variable=check_var_mon, width=5).pack(side=LEFT)
    # Checkbutton(login_window, text="Tue", variable=check_var_tue, width=5).pack(side=LEFT)
    # Checkbutton(login_window, text="Wed", variable=check_var_wed, width=5).pack(side=LEFT)
    # Checkbutton(login_window, text="Thu", variable=check_var_thu, width=5).pack(side=LEFT)
    # Checkbutton(login_window, text="Fri", variable=check_var_fri, width=5).pack(side=LEFT)
    # Checkbutton(login_window, text="Sat", variable=check_var_sat, width=5).pack(side=LEFT)
    # Checkbutton(login_window, text="Sun", variable=check_var_sun, width=5).pack(side=LEFT)

def open_expense_window():
    expense_window = Toplevel(main_screen)
    expense_window.title("Expense Window")
    expense_window.geometry("390x844")

    Label(expense_window, text = "Expenses", font=("Calibri", 15)).pack()

    Button(expense_window, text = "Bill Scan", width = 10, command = lambda: import_image()).pack()

    Button(expense_window, text = "Text", width = 10, command = lambda: open_NLP_window()).pack()

######## LOGIN FRAME 

main_screen = Tk()
main_screen.geometry("390x844")
main_screen.title("Login")

Label(text="Choose Login or Register", bg="#CEDEBD", width="300", height="2", font=("Calibri", 13)).pack()
Label(text="").pack()

# Username Entry
username_label = Label(main_screen, text="Username:")
username_label.pack()
username_entry = Entry(main_screen, width=30)  
username_entry.pack(pady=5)

# Password Entry
password_label = Label(main_screen, text="Password:")
password_label.pack()
password_entry = Entry(main_screen, width=30, show="*")  
password_entry.pack(pady=10)


button_width = 150
button_height = 30

# get window dimensions
window_width = main_screen.winfo_reqwidth()
window_height = main_screen.winfo_reqheight()

# Calculate button coordinates to center them in the window
button_x = (window_width - button_width) // 2 
button_y = (window_height - button_height) // 2 


login_button = Button(text="Login", height="2", width="30",command=open_main_window)
#login_button.place(x=button_x+23, y=button_y + 150)
login_button.pack()


register_button = Button(text="Register", height="2", width="30")
#register_button.place(x=button_x+23, y=button_y + 200)  
register_button.pack()

main_screen.mainloop()
