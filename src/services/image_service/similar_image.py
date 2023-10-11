from operator import itemgetter
import urllib.request
import numpy as np
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import os


class FeatureExtractor:
    def __init__(self):
        # # Use VGG-16 as the architecture, ImageNet for the weight
        # base_model = VGG16(weights='imagenet')
        # # Customize the model to return features from fully-connected layer
        # self.model = Model(inputs=base_model.input,
        #                    outputs=base_model.get_layer('fc1').output)
        pass

    def extract(self, image_url):
        img = load_img(image_url)
        img = img.resize((224, 224))  # VGG must take a 224x224 img as an input
        img = img.convert('RGB')  # Make sure img is color
        # To np.array. Height x Width x Channel. dtype=float32
        x = image.img_to_array(img)
        # (H, W, C)->(1, H, W, C), where the first elem is the number of img
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)  # Subtracting avg values for each pixel
        feature = self.model.predict(x)[0]  # (1, 4096) -> (4096, )
        return feature / np.linalg.norm(feature)


def eucledian_distance(x, y):
    eucl_dist = np.linalg.norm(x - y)
    return eucl_dist


Extractor = FeatureExtractor()


def get_most_similar(books, image_url, max_result_num):

    pred = Extractor.extract(img)

    books_and_scores = []
    for book in books:
        if not book.preds:
            cover_url = 'src/services/image_service/'+book.book_id+'.png'
            if not os.path.isfile():
                urllib.request.urlretrieve(book.cover, cover_url)

        cover_pred = Extractor.extract(img)
        score = eucledian_distance(pred, cover_pred)
        books_and_scores.append((book, score))

    books_and_scores.sort(key=itemgetter(1))
    return books_and_scores[:max_result_num]
