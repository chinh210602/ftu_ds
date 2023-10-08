import pickle

def Classify(x):
    "x: np.array -> return np.array"
    filename = r"D:\Python_Project\DS_FTU\OCR\dev_model\text_classifier_lv1\model\NB_v2.sav"

    model = pickle.load(open(filename, 'rb'))

    count_vectorizer = pickle.load(open(r"D:\Python_Project\DS_FTU\OCR\dev_model\text_classifier_lv1\utils\count_vectorizer.pickle", "rb"))
    transform = pickle.load(open(r"D:\Python_Project\DS_FTU\OCR\dev_model\text_classifier_lv1\utils\transform.pickle", "rb"))

    x_proccesed = count_vectorizer.transform(x)

    x_proccesed = transform.transform(x_proccesed)

    y_pred = model.predict(x_proccesed)

    return y_pred