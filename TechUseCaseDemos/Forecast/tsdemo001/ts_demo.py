"""
Time Series Forecasting Demo
============================

This demo demonstrates a simple time series forecasting workflow:
1. Generate synthetic time series data with trend, seasonality, and noise.
2. Visualize the data.
3. Prepare data for supervised learning (windowing).
4. Build and train a simple LSTM model.
5. Forecast and evaluate the model.
6. Plot actual vs predicted values.

Dependencies:
    numpy, pandas, matplotlib, tensorflow, scikit-learn
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)


def generate_synthetic_time_series(n_points=200):
    """
    Generate a synthetic time series with:
    - Linear trend
    - Yearly seasonality (sinusoidal)
    - Monthly seasonality (sinusoidal)
    - Random noise
    """
    time = np.arange(n_points)
    
    # Trend component
    trend = 0.05 * time
    
    # Yearly seasonality (period = 50 points)
    yearly_season = 2 * np.sin(2 * np.pi * time / 50)
    
    # Monthly seasonality (period = 10 points)
    monthly_season = 1 * np.sin(2 * np.pi * time / 10)
    
    # Noise
    noise = 0.5 * np.random.randn(n_points)
    
    # Combine components
    values = trend + yearly_season + monthly_season + noise
    
    # Create a date range (starting from 2020-01-01)
    dates = pd.date_range(start='2020-01-01', periods=n_points, freq='D')
    
    df = pd.DataFrame({'date': dates, 'value': values})
    df.set_index('date', inplace=True)
    
    return df


def create_windowed_dataset(series, window_size=10, batch_size=32, shuffle_buffer=1000):
    """
    Convert a time series into a windowed dataset for supervised learning.
    """
    dataset = tf.data.Dataset.from_tensor_slices(series.values)
    dataset = dataset.window(window_size + 1, shift=1, drop_remainder=True)
    dataset = dataset.flat_map(lambda window: window.batch(window_size + 1))
    dataset = dataset.map(lambda window: (window[:-1], window[-1]))
    if shuffle_buffer > 0:
        dataset = dataset.shuffle(shuffle_buffer)
    dataset = dataset.batch(batch_size).prefetch(1)
    return dataset


def build_model(window_size):
    """
    Build a simple LSTM model for time series forecasting.
    """
    model = keras.Sequential([
        layers.LSTM(64, activation='relu', input_shape=(window_size, 1)),
        layers.Dense(32, activation='relu'),
        layers.Dense(1)
    ])
    model.compile(loss='mse', optimizer=keras.optimizers.Adam(learning_rate=0.001),
                  metrics=['mae'])
    return model


def plot_forecast(train, test, forecast, window_size, title='Time Series Forecast'):
    """
    Plot the training data, test data, and forecast.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(train.index, train.values, label='Training Data', color='blue')
    plt.plot(test.index, test.values, label='Actual Test Data', color='green')
    # Forecast starts after window_size points due to windowing
    forecast_index = test.index[window_size:]
    plt.plot(forecast_index, forecast, label='Forecast', color='red', linestyle='--')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def main():
    print("Generating synthetic time series data...")
    df = generate_synthetic_time_series(n_points=300)
    
    # Split into train and test (80% train, 20% test)
    split_idx = int(len(df) * 0.8)
    train = df.iloc[:split_idx]
    test = df.iloc[split_idx:]
    
    print(f"Training data shape: {train.shape}")
    print(f"Test data shape: {test.shape}")
    
    # Plot the full series
    plt.figure(figsize=(12, 4))
    plt.plot(df.index, df.values, color='black')
    plt.title('Synthetic Time Series Data')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('synthetic_timeseries.png')
    plt.close()
    print("Saved synthetic time series plot to 'synthetic_timeseries.png'")
    
    # Parameters
    window_size = 20
    batch_size = 32
    
    # Create windowed datasets
    train_dataset = create_windowed_dataset(train['value'], window_size, batch_size)
    test_dataset = create_windowed_dataset(test['value'], window_size, batch_size, shuffle_buffer=0)  # No shuffle for test
    
    # Build and train model
    print("\nBuilding and training LSTM model...")
    model = build_model(window_size)
    model.summary()
    
    history = model.fit(
        train_dataset,
        epochs=20,
        validation_data=test_dataset,
        verbose=1
    )
    
    # Plot training history
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss (MSE)')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['mae'], label='Training MAE')
    plt.plot(history.history['val_mae'], label='Validation MAE')
    plt.title('Model MAE')
    plt.xlabel('Epoch')
    plt.ylabel('MAE')
    plt.legend()
    plt.tight_layout()
    plt.savefig('training_history.png')
    plt.close()
    print("Saved training history plot to 'training_history.png'")
    
    # Make predictions on test set
    print("\nMaking predictions on test set...")
    forecast = model.predict(test_dataset).flatten()
    
    # Calculate metrics
    mae = mean_absolute_error(test['value'].values[window_size:], forecast)
    mse = mean_squared_error(test['value'].values[window_size:], forecast)
    rmse = np.sqrt(mse)
    
    print(f"\nForecast Evaluation:")
    print(f"MAE: {mae:.4f}")
    print(f"MSE: {mse:.4f}")
    print(f"RMSE: {rmse:.4f}")
    
    # Plot forecast
    plot_forecast(train, test, forecast, window_size, title='LSTM Time Series Forecast')
    plt.savefig('forecast_plot.png')
    plt.close()
    print("Saved forecast plot to 'forecast_plot.png'")
    
    # Save the model
    model.save('ts_forecast_model.h5')
    print("Saved model to 'ts_forecast_model.h5'")
    
    print("\nDemo completed successfully!")


if __name__ == "__main__":
    main()