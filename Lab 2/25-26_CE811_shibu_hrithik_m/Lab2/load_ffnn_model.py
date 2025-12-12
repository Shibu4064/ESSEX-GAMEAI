import tensorflow as tf
import os, contextlib
import pandas as pd  
import tensorflow as tf
print("TensorFlow version", tf.__version__)

# load model back in:
keras_model=tf.keras.models.load_model('ModelIris.keras')

# print model summary information:
keras_model.summary()

c=0
for layer in keras_model.layers:
   c+=1
   if isinstance(layer, tf.keras.layers.Conv2D) or isinstance(layer, tf.keras.layers.Dense):
     print("Layer",c,"Activation Function",layer.activation.__name__)
     

# run the neural network on the test set:
inputs_val=pd.read_csv('datasets'+os.path.sep+'iris_test.csv',usecols = [0,1,2,3],skiprows = None,header=None).values
labels_val = pd.read_csv('datasets'+os.path.sep+'iris_test.csv',usecols = [4],skiprows = None ,header=None).values.reshape(-1)

predictions = tf.math.argmax(keras_model(inputs_val),axis=1)
accuracy=tf.reduce_mean(tf.cast(tf.equal(predictions,labels_val),tf.float32)).numpy()     
print("Accuracy of saved model on test set",accuracy)
