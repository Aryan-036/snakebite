import tensorflow as tf
import numpy as np
import joblib
from PIL import Image

snake_model = tf.keras.models.load_model("models/snake_model.h5")
symptom_model = joblib.load("models/symptom_model.pkl")

classes = ["cobra","krait","viper","non_venomous"]

def predict_snake_image(image):

    img = image.resize((224,224))
    img = np.array(img)/255.0
    img = np.expand_dims(img,axis=0)

    prediction = snake_model.predict(img)
    index = np.argmax(prediction)

    return classes[index]

def predict_symptoms(symptoms):

    pred = symptom_model.predict([symptoms])

    return pred[0]

def final_prediction(snake_name=None,snake_image=None,symptoms=None):

    if snake_name:
        return snake_name.lower()

    if snake_image:
        return predict_snake_image(snake_image)

    if symptoms:
        return predict_symptoms(symptoms)

    return "Unknown"

def get_first_aid(snake_type):

    advice = {

    "cobra":[
    "Keep victim calm",
    "Immobilize the limb",
    "Seek medical help immediately"
    ],

    "krait":[
    "Keep victim still",
    "Avoid movement",
    "Transport to hospital urgently"
    ],

    "viper":[
    "Clean wound",
    "Immobilize limb",
    "Seek urgent treatment"
    ],

    "non_venomous":[
    "Wash wound with soap",
    "Apply antiseptic",
    "Monitor swelling"
    ]
    }

    return advice.get(snake_type,["Seek medical help"])