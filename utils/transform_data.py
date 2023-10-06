def transform_data(data):
    date = data["date"]
    items = data["products"]

    re = []

    for item in items:
        des = item["description"]
        type_ = item["type"]
        amount = item["amount"]
 
        re.append((date, des, amount, type_))

    return re