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

* `notebook.ipynb`: main Jupyter Notebook where all EDA and model training is carried out.
* `xception_v4_1_17_0.846.h5`: trained model in `notebook.ipynb`. learning rate, size inner and dropout parameters were optimized and were chosen best model with the checkpoint.
* `convert-model.py`: converts `xception_v4_1_17_0.846.h5` model to tflite model `jelly-model.tflite`.
* `lambda-function.py` contains the inference code for predictions. The script is formatted for deployment on Amazon Web Services' Lambda.
* `test.py`: testing the model
* `docker` is a folder that contains all of the necessary components for dockerization and deployment sections:
    * `Dockerfile` is the file necessary to create the Docker image.
    * `lambda-function.py` is a copy of the same file on the root project folder except for a changed library for deployment.
*`kubernetes` folder: includes gateway and model service/deployment .yaml files, pip environment files, docker images for gateway and model and testing file.

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
and comment other urls in `kubernetes/test.py`:

for kubernetes deployment:

Run .yaml files in kubernetes/kube-config/:

`kubectl apply -f filename.yaml`

* `model-deployment.yaml`
* `model-service.yaml`
* `gateway-deployment.yaml`
* `gateway-service.yaml`

and uncomment in `kubernetes/test.py`:
```
url = 'http://localhost:8080/predict'
```
and comment other urls.

for AWS EKS Cluster:

`eksctl create cluster -f eks-config.yml`

## Publishing the image to ECR

For EKS to work we need to provide the Docker images we will use for our deployments.

[We already explored how to upload a Docker image to ECR in Lesson 9](https://github.com/DataTalksClub/machine-learning-zoomcamp/tree/master/09-serverless). Below is a shortened explanation to create a repository and upload the images:

1. Create an ECR repository and login to it. We will use the name `mlzoomcamp-images` for it.
1. Create the remote URIs for the model and gateway images.
    * The URI prefix is the repo URI.
    * The URI suffix will be the names of the images but substituting the colons with dashes.
        * `zoomcamp-10-model:v1` becomes `zoomcamp-10-model-v1`
        * `zoomcamp-10-gateway:v2` becomes `zoomcamp-10-gateway-v2`
1. Tag the latest versions of your images with the remote URIs.
1. Push the images to ECR.

## Updating the deployment config files

We now need to modify both `model-deployment-yaml` and `gateway-deployment-yaml` so that the container specs point to the images hosted on ECR.

Simply edit the files and change the `.spec.template.spec.image` field to the images' remote URIs.

## Applying the deployments and services to EKS

Once `eksctl` finishes creating the cluster, `kubectl` should already be configured to work with it. You can test it with the following command:

```sh
kubectl get nodes
```

Once we've checked that `kubectl` displays the nodes (actually single node in this example) of our cluster, we can start applying and testing the deployments and services.

Let's begin with the model.

```sh
kubectl apply -f model-deployment.yaml
kubectl apply -f model-service.yaml
kubectl get pod # check if the pod is active
kubectl get service # check if service is working
```

We can also do port forwarding to test the service:

```sh
kubectl port-forward service/tf-serving-model 8500:8500
# on another terminal, run the gateway script locally
```

Let's now continue with the gateway.

```sh
kubectl apply -f gateway-deployment.yaml
kubectl apply -f gateway-service.yaml
kubectl get pod # check if the pod is active
kubectl get service # check if service is working
```

This time, the output of `kubectl get service` should show an external IP next to the gateway service.

Let's do port forwarding to test it:

```sh
kubectl port-forward service/gateway 8080:80
# on another terminal, run the test script locally
```

We can also telnet to the gateway service to test it. It's likely that you will not be able to telnet to it right after applying the service because the changes need to be propagated, but it should only take a few minutes. Do this after disabling port forwarding:

```sh
kubectl get service # copy the external url of the gateway service
telnet <url-of-the-gateway-service>
```

Finally, use the test script. Update the test script to point to the external URL of the gateway service.

> ***WARNING***: The gateway is open to everyone who has the URL. AWS will charge you for machine uptime and requests received. Leaving it as it is may result in unwanted charges. There are ways to limit access to the gateway but it falls outside the scope of this course.

After you're done with the cluster, you may delete it to avoid additional charges.

```sh
eksctl delete cluster --name mlzoomcamp-eks
```






