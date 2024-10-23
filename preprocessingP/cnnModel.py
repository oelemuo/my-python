"""
This program evaluates a Convolutional Neural Network(CNN) for image classification task
using TensorFlow/Keras. Supposing that the model is trained on processing images

Functions:
- build_cnn_model(): Defines CNN structure
- train_model(train_data): Trains the CNN model with the provided training data.
"""
import os
from keras.src.legacy.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.python.keras.models import Sequential

# Preparing the image data
def load_data(data_dir, target_size=(64, 64), batch_size=32):
    """

    :param data_dir: Directory where image is stored
    :param target_size: The desired size which all images will be resized too
    :param batch_size: The size of the batches of data
    :return: A generator for the training data
    """
    datagen = ImageDataGenerator(rescale=1./255)
    train_data = datagen.flow_from_directory(
        data_dir, target_size=target_size,batch_size=batch_size,class_mode='binary'
    )
    return train_data

# Defining the CNN Model
def build_cnn_model(input_shape=(64, 64, 3)):
    """

    :param input_shape: Shape of input images
    :return: A compiled CNN model
    """

    model = Sequential()
    #Convolutional Layer
    model.add(Conv2D(32,(3,3), activation='relu', input_shape=input_shape))
    #MaxPooling layer
    model.add(MaxPooling2D(pool_size=(2,2)))

    # Flatten Layer (convert 2D feature maps to 1D)
    model.add(Flatten())

    # Output layer(A binary classification: 1 output Neuron with sigmoid activation
    # CNN architecture design based on Keras layers: https://keras.io/api/layers/
    model.add(Dense(units=1, activation='sigmoid'))

    # Compiling the CNN
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model

def train_model(model, train_data, epochs=10, steps_per_epoch=100):
    """

    :param model: The compiled CNN model
    :param train_data: preprocessing module including image_data_generator.py
    :param epochs: Numbers of epochs to train the model
    :param steps_per_epoch: Number of steps to train per epoch
    :return: taining history
    """
    history = model.fit(train_data, steps_per_epoch=steps_per_epoch, epochs=epochs)
    return history

if __name__ == "__main__":
    # load preprocessed image from the directory
    data_dir = 'C:/Users/obinn/Pictures/cnnModelTest'
    train_data = load_data(data_dir)

    # build the CNN model
    cnn_model = build_cnn_model()

    # train the CNN model on the image data
    history = train_model(cnn_model, train_data)

    # Step 4: Save the trained model using HDF5 format
    model_save_path = 'cnn_model.h5'
    cnn_model.save('cnn_model.h5', save_format='h5')
    print(f"Model saved to {model_save_path}")
