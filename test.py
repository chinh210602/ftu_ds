import customtkinter as ctk
data = {'date': '2020-08-09', 'products': [{'description': 'Dầu simply 1L NT', 'amount': 45000, 'type': 'thực phẩm'}, {'description': 'keo socola cá xinh việt thá NO', 'amount': 26000, 'type': 'thực phẩm'}, {'description': 'Bánh OREO 137g NT', 'amount': 13000, 'type': 'thực phẩm'}, {'description': 'keo ty to 70g Noi', 'amount': 10000, 'type': 'thực phẩm'}]}
def confirm_popup(data):
        fg_color = "white"
        main_font = "Calibri"
        columns = ["Mô tả", "Hạng mục", "Số tiền"]

        pop_up = ctk.CTkToplevel(fg_color = fg_color)
        pop_up.geometry("350x600")

        date = data["date"]
        products = data["products"]

        date_label = ctk.CTkLabel(pop_up,
                                  text = date,
                                  width = 350,
                                  height = 50,
                                  font = (main_font, 25))
        date_label.pack()
        columns_name_frame = ctk.CTkFrame(pop_up,
                                          width = 350,
                                          height = 50,
                                          fg_color = fg_color)
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
                         font = (main_font, 15),
                         fg_color = "grey").grid(row = 0, column = i, padx = 10)
            

        data_frame = ctk.CTkScrollableFrame(pop_up,
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
                         font = (main_font, 15))
            des.insert(0, product["description"])
            des.grid(row = i, column = 0, pady = 10)
            
            type_ = ctk.CTkEntry(data_frame,
                         height  = 45,
                         width = 100,
                         font = (main_font, 15))
            
            type_.insert(0, product["type"])
            type_.grid(row = i, column = 1, pady = 10)
            
            amount = ctk.CTkEntry(data_frame,
                         height  = 45,
                         width = 80,
                         font = (main_font, 15))
            amount.grid(row = i, column = 2, pady = 10)
            amount.insert(0, product["amount"])

        submit_button = ctk.CTkButton(pop_up,
                                      width = 100,
                                      height = 50,
                                      text = "Xác Nhận")
        submit_button.pack()

if __name__ == '__main__':
    app = ctk.CTk()
    confirm_popup(data)
    app.mainloop()