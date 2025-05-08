from tensorflow.keras import layers, models # type: ignore
import tensorflow as tf


def build_cnn_model(trace_length=300, num_classes=16):
    input_shape = (trace_length, 1)

    model = models.Sequential()
    model.add(layers.Input(shape=input_shape))

    # Optional: Add Gaussian noise layer for robustness
    model.add(layers.GaussianNoise(0.01))

    # Conv Block 1
    model.add(layers.Conv1D(filters=32, kernel_size=7, strides=1, padding='same'))
    model.add(layers.BatchNormalization())
    model.add(layers.ReLU())
    model.add(layers.MaxPooling1D(pool_size=2))

    # Conv Block 2
    model.add(layers.Conv1D(filters=64, kernel_size=5, strides=1, padding='same'))
    model.add(layers.BatchNormalization())
    model.add(layers.ReLU())
    model.add(layers.MaxPooling1D(pool_size=2))

    # Conv Block 3
    model.add(layers.Conv1D(filters=128, kernel_size=3, strides=2, padding='same'))
    model.add(layers.BatchNormalization())
    model.add(layers.ReLU())

    # Conv Block 4
    model.add(layers.Conv1D(filters=256, kernel_size=3, strides=2, padding='same'))
    model.add(layers.BatchNormalization())
    model.add(layers.ReLU())

    # Global Average Pooling
    model.add(layers.GlobalAveragePooling1D())

    # Dense layers
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(0.2))

    model.add(layers.Dense(num_classes, activation='softmax'))

    # Compile with Adam and learning rate scheduler
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    model.compile(optimizer=optimizer,
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    return model