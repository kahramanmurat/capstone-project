FROM tensorflow/serving:2.7.0

COPY jelly-model /models/jelly-model/1
ENV MODEL_NAME="jelly-model"