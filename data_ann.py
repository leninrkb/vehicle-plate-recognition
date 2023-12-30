from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator

# Parámetros
num_classes = 36
batch_size = 32
epochs = 10
input_shape = (28, 28, 1)

# Crear el modelo
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

# Compilar el modelo
model.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])

# Generador de imágenes
datagen = ImageDataGenerator(rescale=1./255)
train_generator = datagen.flow_from_directory(
    'ruta/a/tu/dataset',
    target_size=(28, 28),
    batch_size=batch_size,
    color_mode='grayscale',
    class_mode='categorical')

# Entrenar el modelo
model.fit_generator(
    train_generator,
    steps_per_epoch=1016 * num_classes // batch_size,
    epochs=epochs)
