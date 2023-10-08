from datetime import datetime

def ConvertLabel(y, label_dict):
    "np.array -> np.array"
    return y.map(lambda x: label_dict[x])

def PostProcessing(x, y_pred):
    """
    x: np.array
    y: np.array

    return dictionary
    """
    re = []
    for x, y_pred in zip(x, y_pred):
        if y_pred == 4:
            continue
        
        re.append((x, y_pred))
    cart = {"date": None, "products": []}
    temp = {"description": None, "amount": None}

    for element in re:

        if element[1] == 1:
            temp["description"] = element[0]

        elif element[1] == 3 and temp["description"]:
            amount = element[0]
            if len(amount) > 3:

                if amount[-4] == ".": amount_clean = amount.replace(".", "")

                elif amount[-4] == ",": amount_clean = amount.replace(",", "")
                
            
            temp["amount"] = int(amount_clean)
            cart["products"].append(temp)
            temp = {"description": None, "amount": None}

        elif element[1] == 0:
            #Ngày bán: x/x/x
            #x/x/x-t:t
            #x-x-x
            #x-x-x-t:t
            date = element[0]
            date = date.split(": ")
            if len(date) >= 2: date_clean = date[1][0:10]
            else: date_clean = date[0]
            date_clean = datetime.strptime(date_clean, "%d/%m/%Y").strftime("%Y-%m-%d")

            if date_clean == "Hôm nay": date_clean = datetime.today()
            cart["date"] = date_clean
        

    return cart