# Imports
import glob
import numpy as np
import os.path as path
from scipy import misc
import matplotlib.pyplot as plt

# IMAGE_PATH should be the path to the downloaded planesnet folder
IMAGE_PATH = '/Users/avdra/Desktop/GunNeuralNetData'
file_paths = glob.glob(path.join(IMAGE_PATH, '*.jpg'))

# Load the images
images = [misc.imread(path) for path in file_paths]
images = np.asarray(images)



# Get image size
image_size = np.asarray([images.shape[1], images.shape[2], images.shape[3]])
print(image_size)

# Scale
images = images / 255

# Read the labels from the filenames
n_images = images.shape[0]
labels = np.zeros(n_images)
for i in range(n_images):
    filename = path.basename(file_paths[i])[0]
    labels[i] = int(filename[0])

    # Split into test and training sets
TRAIN_TEST_SPLIT = 0.7

# Split at the given index
split_index = int(TRAIN_TEST_SPLIT * n_images)
shuffled_indices = np.random.permutation(n_images)
train_indices = shuffled_indices[0:split_index]
test_indices = shuffled_indices[split_index:]

# Split the images and the labels
x_train = images[train_indices, :, :, :]
y_train = labels[train_indices]
x_test = images[test_indices, :, :, :]
y_test = labels[test_indices]

# Imports
from keras.models import Sequential,load_model
from keras.layers import Activation, Dropout, Flatten, Dense, Conv2D, MaxPooling2D
from keras.callbacks import EarlyStopping, TensorBoard
from sklearn.metrics import accuracy_score, f1_score
from datetime import datetime





# Hyperparamater
N_LAYERS = 4


def cnn(size, n_layers):
    # INPUTS
    # size     - size of the input images
    # n_layers - number of layers
    # OUTPUTS
    # model    - compiled CNN

    # Define hyperparamters
    MIN_NEURONS = 5
    MAX_NEURONS = 120
    KERNEL = (3, 3)

    # Determine the # of neurons in each convolutional layer
    steps = np.floor(MAX_NEURONS / (n_layers + 1))
    nuerons = np.arange(MIN_NEURONS, MAX_NEURONS, steps)
    nuerons = nuerons.astype(np.int32)

    # Define a model
    model = Sequential()

    # Add convolutional layers
    for i in range(0, n_layers):
        if i == 0:
            shape = (size[0], size[1], size[2])
            model.add(Conv2D(nuerons[i], KERNEL, input_shape=shape))
        else:
            model.add(Conv2D(nuerons[i], KERNEL))

        model.add(Activation('relu'))

    # Add max pooling layer
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(MAX_NEURONS))
    model.add(Activation('relu'))
  model.add(Flatten())
    # Add output layer

    model.add(Activation('sigmoid'))

    # Compile the model
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    # Print a summary of the model
    model.summary()

    return model



# Instantiate the model
model = cnn(size=image_size, n_layers=N_LAYERS)


# Training hyperparamters
EPOCHS = 5
BATCH_SIZE = 10



# Early stopping callback
PATIENCE = 10
early_stopping = EarlyStopping(monitor='loss', min_delta=0, patience=PATIENCE, verbose=0, mode='auto')



# TensorBoard callback
LOG_DIRECTORY_ROOT = ''
now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
log_dir = "{}/run-{}/".format(LOG_DIRECTORY_ROOT, now)
tensorboard = TensorBoard(log_dir=log_dir, write_graph=True, write_images=True)

# Place the callbacks in a list
callbacks = [early_stopping, tensorboard]




# Train the model
model.fit(x_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=callbacks, verbose=0)


# Make a prediction on the test set
test_predictions = model.predict(x_test)
test_predictions = np.round(test_predictions)


# Report the accuracy
accuracy = accuracy_score(y_test, test_predictions)
print("Accuracy: " + str(accuracy))


imex=misc.imread('/Users/avdra/Desktop/GunNeuralNetData/1_9efe4acc6577181d47a18a7a92055029--survival-life-survival-weapons.jpg')

print(model.predict(np.asarray(imex.reshape((1, 200, 200, 3)))))







def saveModel(mod):
    #save model
    mod.save('model.h5')
    print("Current model saved")

saveModel(model)



def loadModel():
    # load json and create model
    fileName = "model.h5"
    print("Loading model from file: " + fileName + "...")
    return load_model(fileName)

m=loadModel()
