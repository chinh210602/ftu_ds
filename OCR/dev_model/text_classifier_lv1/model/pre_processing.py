
def PreProcessing(x, threshold = 30):
    "x: list -> return list" 

    re = []
    for x_i in x:
        if len(x_i) > threshold and (ord(x_i[0]) >= 48 and ord(x_i[0]) <= 57):
            x_i = x_i.split(maxsplit = 1)[1]
        re.append(x_i)
    return re