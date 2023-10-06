def calculate_percentage(array, n_round = 2):
    re = []
    total = sum(array)
    for a in array:
        re.append(round(a/total * 100, 2))
    
    return re