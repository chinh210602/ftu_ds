import pickle 
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
from .utils.post_processing import post_processing
import json

class NLUPipeLine():
    def __init__(self, model_path, weights_path, tokenizer_path, maxlen = 9):
        with open(model_path, "r") as f:
            loaded_model = f.read()
        self.model = tf.keras.models.model_from_json(loaded_model)
        self.model.load_weights(weights_path)
        with open(tokenizer_path, "rb") as f:

            self.tokenizer = pickle.load(f)
        
        self.maxlen = maxlen

    def start(self, texts):
        mapping = {1: '<OOV>',
                    2: 'O',
                    3: 'B-date',
                    4: 'amount',
                    5: 'B-type',
                    6: 'I-date',
                    7: 'I-type'}

        tokenized_texts = self.tokenizer.texts_to_sequences(texts)
        X = pad_sequences(tokenized_texts, maxlen = self.maxlen, padding = "post")

        #X_tensor = tf.convert_to_tensor(X)

        predictions = list(tf.argmax(self.model.predict(X)[0], axis = 1).numpy())
        predictions = [mapping[x] for x in predictions if x != 0]
        output = {"text": texts[0], 
                    "labels": predictions}
        
        return post_processing(output)
    
