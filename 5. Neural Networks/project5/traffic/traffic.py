import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )
    
    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images, labels = list(), list()
    
    for category_name in os.listdir(data_dir):
        # path to each category
        category_path = os.path.join(data_dir, category_name)
        for image_name in os.listdir(category_path):
            # Get each image path
            image_path = os.path.join(category_path, image_name)
            # anly files
            if not os.path.isfile(image_path): continue
            # Load Image with 3 Channels only (no alpha channel)
            image = cv2.imread(image_path)
            # Resizing
            image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT)) 
            # saving
            images.append(image)
            labels.append(int(category_name))

    return images, labels


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    # Create a Convolutional Neural Network Model
    model = tf.keras.models.Sequential([
        # Normalize images from [0..255] to [0..1]
        tf.keras.layers.Rescaling(1./255, input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        
        # learns 32 filters using 5x5 kernel
        tf.keras.layers.Conv2D(
            32, (3, 3), activation='relu'
        ),
        
        # 2x2 max polling
        tf.keras.layers.MaxPooling2D(
            pool_size=(2, 2)
        ),
        
        # learns 16 filters using 5x5 kernel
        tf.keras.layers.Conv2D(
            16, (3, 3), activation='relu'
        ),
        
        # 2x2 max polling
        tf.keras.layers.MaxPooling2D(
            pool_size=(2, 2)
        ), 
        
        # Flatten data
        tf.keras.layers.Flatten(),
        
        # Hidden Layer with 128 units and 20% dropout
        tf.keras.layers.Dense(
            128, activation='relu'
        ),
        tf.keras.layers.Dropout(0.2),
        
        # Output layer with all categories
        tf.keras.layers.Dense(
            NUM_CATEGORIES, activation='softmax'
        ) 
    ])
    # loss: 0.1027 - accuracy: 0.9762
    
    # Compile the model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model


if __name__ == "__main__":
    main()