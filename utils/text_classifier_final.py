import pickle

def Classify(x):
    "x: np.array -> return np.array"
    filename = r"D:\Python_Project\DS_FTU\utils\models\model.pickle"

    model = pickle.load(open(filename, 'rb'))

    count_vectorizer = pickle.load(open(r"D:\Python_Project\DS_FTU\utils\models\count_vectorizer.pickle", "rb"))
    transform = pickle.load(open(r"D:\Python_Project\DS_FTU\utils\models\transform.pickle", "rb"))

    products = x["products"]

    labels_map = ["thực phẩm", "phương tiện đi lại", "gia dụng", "y tế", "giáo dục", "khác"]

    for i, product in enumerate(products):
        description = [product["description"]]
        description = count_vectorizer.transform(description)
        description = transform.transform(description)
        prediction = model.predict(description)[0]
        product["type"] = labels_map[prediction]
        products[i] = product
    x["products"] = products

    return x