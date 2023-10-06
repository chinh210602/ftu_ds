#Output {"text": "", "labels": []}

#Return {"date":"", "products": []}
from datetime import datetime, timedelta

data = {"text": "Hôm nay tôi mua 10 cá rán", "labels": ["B-date", "I-date", "O", "O", "amount", "B-type", "I-type"]}

def date_post_processing(date):
    if date == "Hôm nay" or "hôm nay": return datetime.today().strftime('%Y-%m-%d')
    elif date == "Hôm qua" or "hôm qua": return (datetime.today() - timedelta(days = 1)).strftime('%Y-%m-%d')
    else: return date

def post_processing(data):
    """
    input
    data: dict {"text": "", "labels": []}

    return
    dict {"date":"", "products": []}
    """

    texts = data["text"].split()
    labels = data["labels"][:len(texts)]

    items = []
    tmp_item = {"description": None,
                    "amount": None}
    for i, label in enumerate(labels):

        if label == "O": continue

        #Date 
        if label == "B-date":
            data = label

            if i + 1 < len(labels):
                if labels[i + 1] == "I-date":
                    date = texts[i] + " " + texts[i + 1]
        date_clean = date_post_processing(date)
        #Item
        if label == "B-type":
            tmp_item["description"] = texts[i]

            if i + 1 < len(labels):
                if labels[i + 1] == "I-type":
                    tmp_item["description"] = texts[i] + " " + texts[i + 1]
                
        #Amount
        if label == "amount":
            tmp_item["amount"] = texts[i]
        
        if tmp_item["amount"] and tmp_item["description"]: 
            items.append(tmp_item)
            tmp_item = {"description": None,
                        "amount": None}

    return {"date": date_clean,
            "products": items}

if __name__ == "__main__":
    print(post_processing(data))