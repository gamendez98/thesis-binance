from tensorflow.keras import layers, models

from modified_anatoley_loss import AnatoleyLoss


# Define a simple model
def create_model():
    model = models.Sequential([
        layers.Dense(64, activation='relu', input_shape=(10,)),
        layers.Dense(1, activation='sigmoid')
    ])
    return model


# Create a simple dataset
import numpy as np

# Random dataset for example
X_train = np.random.randn(100, 10)  # 100 samples, 10 features
y_train = np.random.randn(100, 1)  # 100 labels

# Instantiate the model
model = create_model()

# Compile the model with the custom loss
custom_loss = AnatoleyLoss()
model.compile(optimizer='adam', loss=custom_loss)

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32)


def evaluate_model_return(x_test, y_test, threashhold = 0.5):
    y_pred = model.predict(x_test)