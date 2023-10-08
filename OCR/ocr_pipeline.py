import os
import cv2
import argparse
import torch
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib
from .modules import Preprocess, Detection, OCR, Retrieval, Correction
from .tool.config import Config
from .tool.utils import natural_keys, visualize, find_highest_score_each_class
import time
from .dev_model.text_classifier_lv1.model import classify, post_processing, pre_processing

class OCRPipeline:
    def __init__(self, output, config, debug = False, do_retrieve= False, find_best_rotation = False):
        self.output = output
        self.debug = debug
        self.do_retrieve = do_retrieve
        self.find_best_rotation = find_best_rotation
        self.load_config(config)
        self.make_cache_folder()
        self.init_modules()
        

    def load_config(self, config):
        self.det_weight = config.det_weight
        self.ocr_weight = config.ocr_weight
        self.det_config = config.det_config
        self.ocr_config = config.ocr_config
        self.bert_weight = config.bert_weight
        self.class_mapping = {k:v for v,k in enumerate(config.retr_classes)}
        self.idx_mapping = {v:k for k,v in self.class_mapping.items()}
        self.dictionary_path = config.dictionary_csv
        self.retr_mode = config.retr_mode
        self.correction_mode = config.correction_mode

    def make_cache_folder(self):
        self.cache_folder = os.path.join(self.output, 'cache')
        os.makedirs(self.cache_folder,exist_ok=True)
        self.preprocess_cache = os.path.join(self.cache_folder, "preprocessed.jpg")
        self.detection_cache = os.path.join(self.cache_folder, "detected.jpg")
        self.crop_cache = os.path.join(self.cache_folder, 'crops')
        self.final_output = os.path.join(self.output, 'result.jpg')
        self.retr_output = os.path.join(self.output, 'result.txt')

    def init_modules(self):
        self.det_model = Detection(
            config_path=self.det_config,
            weight_path=self.det_weight)
        self.ocr_model = OCR(
            config_path=self.ocr_config,
            weight_path=self.ocr_weight)
        self.preproc = Preprocess(
            det_model=self.det_model,
            ocr_model=self.ocr_model,
            find_best_rotation=self.find_best_rotation)
  
        if self.dictionary_path is not None:
            self.dictionary = {}
            df = pd.read_csv(self.dictionary_path)
            for id, row in df.iterrows():
                self.dictionary[row.text.lower()] = row.lbl
        else:
            self.dictionary=None

        self.correction = Correction(
            dictionary=self.dictionary,
            mode=self.correction_mode)

        if self.do_retrieve:
            self.retrieval = Retrieval(
                self.class_mapping,
                dictionary=self.dictionary,
                mode = self.retr_mode,
                bert_weight=self.bert_weight)

    def start(self, img):
        # Document extraction
        img1 = self.preproc(img)

        if self.debug:
            saved_img = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
            cv2.imwrite(self.preprocess_cache, saved_img)

            boxes, img2  = self.det_model(
                img1,
                crop_region=True,
                return_result=True,
                output_path=self.cache_folder)
            saved_img = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)
            cv2.imwrite(self.detection_cache, saved_img)
        else:
            boxes = self.det_model(
                img1,
                crop_region=True,
                return_result=False,
                output_path=self.cache_folder)

        img_paths=os.listdir(self.crop_cache)
        img_paths.sort(key=natural_keys)
        img_paths = [os.path.join(self.crop_cache, i) for i in img_paths]
        
        texts = self.ocr_model.predict_folder(img_paths, return_probs=False)
        texts = self.correction(texts, return_score=False)
        texts = pre_processing.PreProcessing(texts, 25)
        texts = np.array(texts)

        predictions = classify.Classify(texts)
        output = post_processing.PostProcessing(texts, predictions)

        if self.do_retrieve:
            preds, probs = self.retrieval(texts)
        else:
            preds, probs = None, None

        visualize(
          img1, boxes, texts, 
          img_name = self.final_output, 
          class_mapping = self.class_mapping,
          labels = preds, probs = probs, 
          visualize_best=self.do_retrieve)

        if self.do_retrieve:
            best_score_idx = find_highest_score_each_class(preds, probs, self.class_mapping)
            with open(self.retr_output, 'w') as f:
                for cls, idx in enumerate(best_score_idx):
                    f.write(f"{self.idx_mapping[cls]} : {texts[idx]}\n")
        
        return output
 
if __name__ == '__main__':
    input = r"D:\Python_Project\DS_FTU\OCR\dev_model\text_classifier_lv1\data\mcocr2021\mcocr_public\mcocr_train_data\train_images\mcocr_public_145013adyee.jpg"
    output = "D:/Python_Project/DS_FTU/result_images"

    config = Config('./tool/config/configs.yaml')
    pipeline = OCRPipeline(output, config)
    img = cv2.imread(input)
    start_time = time.time()
    output = pipeline.start(img)
    
    print(output)
    end_time = time.time()

    print(f"Executed in {end_time - start_time} s")

