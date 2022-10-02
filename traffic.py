import cv2
import keras
import numpy as np
import os
import sys
import tensorflow as tf
import time

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.3


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing set
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

    images = []
    labels = []

    # Get required paths and directories and loop over all items in each directory
    directory = os.listdir(f"{data_dir}")
    print(f"Checking {len(directory)} folders and retrieving the images inside")
    time.sleep(1)
    for sub in directory:
        if not sub.startswith('.'):
            sub_dirs = os.listdir(os.path.join(data_dir, sub))
            for item in sub_dirs:
                #  read images to memory, resize them accordingly and append images and labels to lists
                img = cv2.imread(os.path.join(data_dir, sub, item))
                resized = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT), interpolation=cv2.INTER_LINEAR)
                resized = resized/255
                images.append(resized)
                labels.append(int(sub))

    print(f"{len(images)} images and {len(labels)} labels read to memory, images resized")
    time.sleep(1)
    return images, labels


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    """
    A sequential model is appropriate for a plain stack of layers where each layer has exactly one input tensor
    and one output tensor. 
    """

    # Create sequential model
    magic_model_xxl = tf.keras.models.Sequential()

    # Add an input layer and Convolutional layers and Max-pooling layer. Small kernel of 3x3 is used to detect small
    # and local features
    magic_model_xxl.add(tf.keras.Input(shape=(30, 30, 3)))   # 30x30 RGB images
    magic_model_xxl.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu'))
    magic_model_xxl.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu'))
    magic_model_xxl.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

    #  magic_model_xxl.summary()

    # Add another convo maxpooling layer
    magic_model_xxl.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
    magic_model_xxl.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

    # Flatten units, add a dense layer and dropout
    magic_model_xxl.add(tf.keras.layers.Flatten())
    magic_model_xxl.add(tf.keras.layers.Dense(512, activation='relu'))
    magic_model_xxl.add(tf.keras.layers.Dropout(0.5))

    # Add an output layer
    magic_model_xxl.add(tf.keras.layers.Dense(NUM_CATEGORIES, activation='softmax'))

    magic_model_xxl.summary()
    time.sleep(1)
    print("compiling model \n optimizer='adam'\n loss='categorical_crossentropy' \n metrics=['accuracy']")
    time.sleep(0.5)
    magic_model_xxl.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return magic_model_xxl


if __name__ == "__main__":
    main()
