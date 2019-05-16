# Image recognition
from imageai.Prediction import ImagePrediction
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Image search
import requests

# Get path of current folder
execution_path = os.getcwd()

# Load image prediction stuff
prediction = ImagePrediction()
prediction.setModelTypeAsResNet()
prediction.setModelPath( execution_path + "/resnet50_weights_tf_dim_ordering_tf_kernels.h5")
prediction.loadModel()

# Loop through images in folder and get recognition
for filename in os.listdir(execution_path +"/img"):
    filenameRoot = filename.split('.')[0]
    print(filename)
    predictions, percentage_probabilities = prediction.predictImage(execution_path +"/img/" + filename, result_count=1)
    print(predictions[0] , " : " , percentage_probabilities[0])

    # get image
    query = predictions[0]
    r = requests.get("https://api.qwant.com/api/search/images",
        params={
            'count': 1,
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


    with open(execution_path + '/img/' + filenameRoot + '_result.jpg', 'wb') as handle:
        response = requests.get(urls[0], stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    print(urls[0])

    print("")
