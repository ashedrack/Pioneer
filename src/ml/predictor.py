import tensorflow as tf
import numpy as np
from typing import List, Dict, Any
import logging

class ResourcePredictor:
    def __init__(self):
        self.model = None
        self.logger = logging.getLogger(__name__)
        
    def build_model(self, input_shape: tuple) -> None:
        """Build and compile the LSTM model for resource usage prediction."""
        self.model = tf.keras.Sequential([
            tf.keras.layers.LSTM(64, input_shape=input_shape, return_sequences=True),
            tf.keras.layers.LSTM(32),
            tf.keras.layers.Dense(24),  # Predict next 24 hours
            tf.keras.layers.Activation('sigmoid')
        ])
        
        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 50) -> Dict[str, Any]:
        """Train the model on historical resource usage data."""
        if self.model is None:
            self.build_model(input_shape=(X.shape[1], X.shape[2]))
            
        history = self.model.fit(
            X, y,
            epochs=epochs,
            validation_split=0.2,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(
                    monitor='val_loss',
                    patience=5,
                    restore_best_weights=True
                )
            ]
        )
        return history.history
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict resource usage for the next 24 hours."""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        predictions = self.model.predict(X)
        return predictions
    
    def evaluate_prediction(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """Evaluate prediction accuracy."""
        mse = np.mean((y_true - y_pred) ** 2)
        mae = np.mean(np.abs(y_true - y_pred))
        
        return {
            "mse": float(mse),
            "mae": float(mae),
            "rmse": float(np.sqrt(mse))
        }
