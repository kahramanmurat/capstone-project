# Dataset Description
_Original dataset [found here](https://www.kaggle.com/datasets/anshtanwar/jellyfish-types)_

This dataset contains 900 images of jellyfish belonging to six different categories and species: mauve stinger jellyfish, moon jellyfish, barrel jellyfish, blue jellyfish, compass jellyfish, and lion’s mane jellyfish. You can apply ML techniques to gain insights into jellyfish classification, species identification, and color analysis.

1. `Moon jellyfish (Aurelia aurita)`: Common jellyfish with four horseshoe-shaped gonads visible through the top of its translucent bell. It feeds by collecting medusae, plankton, and mollusks with its tentacles.
2. `Barrel jellyfish (Rhizostoma pulmo)`: Largest jellyfish found in British waters, with a bell that can grow up to 90 cm in diameter. It feeds on plankton and small fish by catching them in its tentacles.
3. `Blue jellyfish (Cyanea lamarckii)`: Large jellyfish that can grow up to 30 cm in diameter. It feeds on plankton and small fish by catching them in its tentacles.
4. `Compass jellyfish (Chrysaora hysoscella)`: Named after the brown markings on its bell that resemble a compass rose. It feeds on plankton and small fish by catching them in its tentacles.
5. `Lion’s mane jellyfish (Cyanea capillata)`: Largest jellyfish in the world, with a bell that can grow up to 2 meters in diameter and tentacles that can reach up to 30 meters in length. It feeds on plankton and small fish by catching them in its tentacles.
6. `Mauve stinger (Pelagia noctiluca)`: Small jellyfish with long tentacles and warty structures on its bell full of stinging cells. It feeds on other small jellyfish and oceanic sea squirts.

This dataset contains three folders:

* train (150 images each)
* test (~7 images each)
* validation (~7 images each)

# Problem Description

Jellyfish classification: Use machine learning techniques to classify jellyfish images into different categories based on their physical characteristics. For my capstone project, I chose to focus on Deep Learning.

Due to the limited size of the dataset, the project exclusively depends on Transfer Learning for extracting features from images.

1 CNN architectures were used:
* `Xception`: one of the most popular architectures available on Keras.

# Files & Testing

There are 3 types deployments:

1. Local deployment

   For testing:
      * Build the docker image `capstone/Dockerfile`
      ```
      docker build -t jelly-model .
      ```
      * Run the docker image:
      ```
      docker run -it --rm -p 8080:8080 jelly-model:latest
      ```
      * Run the pthon file `capstone/test.py` and use the url `url = 'http://localhost:8080/2015-03-31/functions/function/invocations'`

2. Serverless AWS Lambda and API Gateway Deployment

   use the url `url="https://5oph9792mi.execute-api.us-east-1.amazonaws.com/test/predict"`
   `Note`: API Gateway is restricted to only my ip information so it may not work due to restricted ip
   
3. Kubernetes deployment (Local and AWS ECR/EKS)
For local testing:

* Build and Run the docker image inside the `kubernetes` folder.

`image-model.dockerfile`:
* Build: `docker build -t jelly-model:xception-v4-001 -f image-model.dockerfile .`
      
`image-gateway.dockerfile`:
* Build: `docker build -t jelly-model-gateway:001 -f image-gateway.dockerfile .`

Finally Run the docker compose file `docker-compose.yaml`

You can run and test locally:

Comment in `gateway.py`:
```
    <!-- url='https://images.theconversation.com/files/513157/original/file-20230302-28-r91z9l.jpg?ixlib=rb-1.1.0&rect=10%2C0%2C6699%2C4466&q=45&auto=format&w=926&fit=clip'
    response = predict(url)
    print(response) -->

```
Uncomment in `gateway.py`:
```
app.run(debug=True, host='0.0.0.0', port=9696)
```

and uncomment in `kubernetes/test.py`:
```
url = 'http://localhost:9696/predict'
```




* `notebook.ipynb`: main Jupyter Notebook where all EDA and model training is carried out.
* `xception_v4_1_17_0.846.h5`: trained model in `notebook.ipynb`. learning rate, size inner and dropout parameters were optimized and were chosen best model with the checkpoint.
* `convert-model.py`: converts `xception_v4_1_17_0.846.h5` model to tflite model `jelly-model.tflite`.
* `lambda-function.py` contains the inference code for predictions. The script is formatted for deployment on Amazon Web Services' Lambda.
* `test.py`: testing the model
* `docker` is a folder that contains all of the necessary components for dockerization and deployment sections:
    * `Dockerfile` is the file necessary to create the Docker image.
    * `lambda-function.py` is a copy of the same file on the root project folder except for a changed library for deployment.
*`kubernetes` folder: includes gateway and model service/deployment .yaml files, pip environment files, docker images for gateway and model and testing file.




