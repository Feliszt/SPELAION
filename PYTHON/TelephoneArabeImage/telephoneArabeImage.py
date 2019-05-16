# Image recognition
from imageai.Prediction import ImagePrediction
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Image search
import requests

# Other
import time
import random

# Load image prediction stuff
prediction = ImagePrediction()
prediction.setModelTypeAsResNet()
prediction.setModelPath("../resnet50_weights_tf_dim_ordering_tf_kernels.h5")
prediction.loadModel()

for i in range(2, 50):
    filename = str(i-1) + ".jpg"

    # get recognition of image
    predictions, percentage_probabilities = prediction.predictImage("img/" + filename, result_count=1)
    query = predictions[0]

    print(str(i))
    print(query)

    # Search the web for the first image
    r = requests.get("https://api.qwant.com/api/search/images",
        params={
            'count': 50,
            'q': query,
            't': 'images',
            'safesearch': 0,
            'locale': 'en_US',
            'uiv': 4
        },
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
    )
    response = r.json().get('data').get('result').get('items')
    urls = [r.get('media') for r in response]
    url = random.choice(urls)

    print(url)
    print("")

    # Save image
    with open('img/' + str(i) + '.jpg', 'wb') as handle:
        response = requests.get(url, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)

    time.sleep(2)
