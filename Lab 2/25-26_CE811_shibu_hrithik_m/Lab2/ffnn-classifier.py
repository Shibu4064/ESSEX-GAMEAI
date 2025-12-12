import pandas as pd
import os
os.environ["KERAS_BACKEND"] = "tensorflow"

#Load CSV files for iris datasets
inputs_train=pd.read_csv('datasets/iris_train.csv',usecols = [0,1,2,3],skiprows = None,header=None).values
labels_train = pd.read_csv('datasets/iris_train.csv',usecols = [4],skiprows = None ,header=None).values.reshape(-1)
inputs_val=pd.read_csv('datasets/iris_test.csv',usecols = [0,1,2,3],skiprows = None,header=None).values
labels_val = pd.read_csv('datasets/iris_test.csv',usecols = [4],skiprows = None ,header=None).values.reshape(-1)
print("Data loaded (shapes only)", inputs_train.shape, labels_train.shape, inputs_val.shape, labels_val.shape)
# Data loaded (shapes only) (120, 4) (120,) (30, 4) (30,)

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

num_inputs=4 # how many inputs does your neural network have?
num_outputs=3 # It needs 3 outputs because there are 3 types of flowers being categorised.

# Define Sequential model with 3 layers, architecture "numinputs-10-10-3", with tanh on all non final layers
model = keras.Sequential(name="my_neural_network") 
model.add(layers.Input(shape=(num_inputs,)))
model.add(layers.Dense(10,activation='tanh'))
model.add(layers.Dense(10,activation='tanh'))
model.add(layers.Dense(num_outputs,activation='softmax'))
#TODO finish model definition here...

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',# hint:remember this a classification problem!
    metrics=['accuracy'] # This allows the training process to keep track of how many flowers are being classified correctly.
)
history = model.fit(
    inputs_train,
    labels_train,
    batch_size=32,
    epochs=120,
    validation_data=(inputs_val, labels_val),
)
model.summary()
model.save('ModelIris.keras')
import matplotlib.pyplot as plt
plt.plot(history.history["accuracy"], label="Training Accuracy")
plt.plot(history.history["val_accuracy"],label="Validation Set Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.grid()
plt.show()
