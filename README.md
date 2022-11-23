# Crop-Doctor
Crop Disease Detector


## Description

For the billions of people on the planet to have access to food, agricultural loss must be minimised through early disease diagnosis. The development of plant disease detection techniques has the twin benefits of boosting crop output and decreasing pesticide use that isn't directed at the right illness. 
Therefore, ensuring food security requires disease detection as well as the development of better crop varieties. Manual examination by farmers or professionals has been the conventional method of disease detection, but this may be time-consuming and expensive, making it unfeasible for millions of small 
and medium-sized farms around the world.
This study uses deep convolutional networks to develop a method for identifying plant diseases based on the classification of leaf images. The created model is capable of recognizing 38 different types of plant diseases out of of 14 different plants with the ability to distinguish plant leaves from their 
surroundings.

## Leaf Image Classification

This process for building a model which can detect the disease assocaited with the leaf image. The key points to be followed are:

1. Data gathering

   The dataset taken was **"New Plant Diseases Dataset"**. It can be downloaded through the link "https://www.kaggle.com/vipoooool/new-plant-diseases-dataset". It is an Image dataset containing images of different healthy and unhealthy crop leaves.

2. Model building

   - I have used tensorflow for building the model.
   - I used two models:-
     1. Using Transfer learning VGG16 Architecture.
     2. Using resnet50 Architecture.

3. Training

   The model was trained by using variants of above layers mentioned in model building and by varying hyperparameters. The best model was able to achieve 98.42% of test accuracy.

4. Testing

   The model was tested on total 17572 images of 38 classes.<br/>
   The model used for prediction on sample images. It can be seen below:

## Details about the model

### The model will be able to detect `38` types of `diseases` of `14 Unique plants`

## Further Work:

- Implementing Image Localisation to find the excat position of the leaf affected .
- Building Recommender system for recommendation of proper presticides and control method for the disease.
- Implementing the appropriate management strategies like fungicide applications and pesticide applications could lead to early
  information on crop health and disease detection.This could facilitate the control of diseases and improve productivity.
- Userfriendly application for the farmers , text to speak , language change , and a mobile based application.
