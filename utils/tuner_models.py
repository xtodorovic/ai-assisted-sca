from tensorflow.keras import layers, models # type: ignore
import tensorflow as tf

TRACE_LENGTH = 47 # Length of the traces
# Number of classes for the output layer
NUM_CLASSES = 16 # 16 for PRESENT, 256 for AES SBox

def build_simple_cnn(hp):
    """
    Builds a simple CNN model based on the architecture described in the thesis document.
    Parameters:
    - input_shape: tuple, the shape of the input data (time_steps, features).
    - num_classes: int, the number of output classes.
    - hyperparameters: dict, contains model hyperparameters (e.g., filters, kernel sizes, etc.).
    Returns:
    - model: A compiled TensorFlow Keras model.
    """
    # Define the input shape
    # input_shape = (T, 1)  # Assuming T is the length of the input sequence
    
    input_shape = (TRACE_LENGTH, 1)

    model = models.Sequential()
    model.add(layers.Input(shape=input_shape))

    # Convolutional Layers
    model.add(layers.Conv1D(
        filters=hp.Int('filters', min_value=8, max_value=64, step=8),
        kernel_size=5,
        activation='relu'
    ))
    model.add(layers.MaxPooling1D(pool_size=2))

    model.add(layers.GlobalAveragePooling1D())

    # Dense Layers
    model.add(layers.Dense(
        hp.Int('dense_units', min_value=32, max_value=128, step=32),
        activation='relu'
    ))
    model.add(layers.Dense(16, activation='softmax'))  # Output: 256 SBox classes

    model.compile(
        optimizer=tf.keras.optimizers.Adam(hp.Choice('learning_rate', [1e-2, 1e-3, 1e-4])),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model


def residual_separable_block(x, filters, kernel_size, block_name):
    """
    Residual block with depthwise separable convolution.
    Args:
        x: Input tensor.
        filters: Number of filters for the convolution.
        kernel_size: Size of the convolution kernel.
        block_name: Name prefix for the layers in this block.
    Returns:
        x: Output tensor after applying the residual block.
    """
    # Residual connection

    shortcut = x

    # Depthwise Separable Conv
    x = layers.SeparableConv1D(filters=filters, kernel_size=kernel_size,
                                padding='same', name=f"{block_name}_sepconv")(x)
    x = layers.BatchNormalization(name=f"{block_name}_bn1")(x)
    x = layers.ReLU(name=f"{block_name}_relu1")(x)

    # Pointwise Conv for residual connection match
    if shortcut.shape[-1] != filters:
        shortcut = layers.Conv1D(filters, kernel_size=1, padding='same',
                                 name=f"{block_name}_shortcut_conv")(shortcut)
        shortcut = layers.BatchNormalization(name=f"{block_name}_shortcut_bn")(shortcut)

    x = layers.Add(name=f"{block_name}_add")([x, shortcut])
    x = layers.ReLU(name=f"{block_name}_relu_out")(x)
    return x


def build_advanced_cnn(hp):
    """
    Builds an advanced CNN model based on the architecture described in the thesis document.
    Parameters:
    - input_shape: tuple, the shape of the input data (time_steps, features).
    - num_classes: int, the number of output classes.
    - hyperparameters: dict, contains model hyperparameters (e.g., filters, kernel sizes, etc.).
    Returns:
    - model: A compiled TensorFlow Keras model.
    """
    # Define the input shape
    # input_shape = (T, 1)  # Assuming T is the length of the input sequence
    input_shape = (TRACE_LENGTH, 1)

    dropout_rate = hp.Float("dropout_rate", min_value=0.1, max_value=0.5, step=0.1)

    inputs = layers.Input(shape=input_shape, name="input")

    x = residual_separable_block(
        inputs,
        filters=hp.Int("filters_block1", 16, 64, step=16),
        kernel_size=hp.Choice("kernel_block1", [3, 5]),
        block_name="block1")
    x = layers.MaxPooling1D(pool_size=2, name="pool1")(x)

    x = residual_separable_block(
        x,
        filters=hp.Int("filters_block2", 32, 128, step=32),
        kernel_size=hp.Choice("kernel_block2", [3, 5]),
        block_name="block2")
    x = layers.MaxPooling1D(pool_size=2, name="pool2")(x)

    x = residual_separable_block(
        x,
        filters=hp.Int("filters_block3", 64, 256, step=64),
        kernel_size=hp.Choice("kernel_block3", [3, 5]),
        block_name="block3")

    x = layers.GlobalAveragePooling1D(name="gap")(x)
    x = layers.Dense(hp.Int("dense_units", 64, 256, step=64), activation='relu', name="dense1")(x)
    x = layers.Dropout(dropout_rate, name="dropout")(x)

    outputs = layers.Dense(NUM_CLASSES, activation='softmax', name="output")(x)

    model = models.Model(inputs=inputs, outputs=outputs, name="advanced_sca_cnn")

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            hp.Choice("learning_rate", [1e-2, 1e-3, 1e-4])
        ),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    return model