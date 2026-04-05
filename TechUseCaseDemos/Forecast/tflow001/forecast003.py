import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import yfinance as yf
import datetime as dt
from sklearn.metrics import mean_absolute_percentage_error
import time

class ETL:
    def __init__(self, ticker, test_size=0.2, period='10y', n_input=5, timestep=5) -> None:
        self.ticker = ticker
        self.period = period
        self.test_size = test_size
        self.n_input = n_input
        self.timestep = timestep
        self.df = self.extract_historic_data()
        self.train, self.test = self.etl()
        self.X_train, self.y_train = self.to_supervised(self.train)
        self.X_test, self.y_test = self.to_supervised(self.test)

    def extract_historic_data(self) -> pd.Series:
        enddate = dt.datetime.strptime('2025-02-15','%Y-%m-%d').date()
        startdate = enddate - dt.timedelta(days=365*15) # 15 years data
        t = yf.Ticker(self.ticker)
        history = t.history(start=startdate, end=enddate, interval='1d')
        if history.empty:
            raise ValueError("No data fetched from yfinance")
        return history.Close

    def split_data(self) -> tuple:
        data = np.array(self.df)
        if len(data) == 0:
            raise Exception('Data set is empty, cannot split.')
        train_idx = round(len(data) * (1 - self.test_size))
        train = data[:train_idx]
        test = data[train_idx:]
        return train[:, np.newaxis], test[:, np.newaxis]

    def window_and_reshape(self, data) -> np.array:
        NUM_FEATURES = 1
        samples = int(data.shape[0] / self.timestep)
        if samples == 0:
            raise ValueError("Not enough data for at least one sample after windowing")
        result = np.array(np.array_split(data[:samples*self.timestep], samples))
        return result.reshape((samples, self.timestep, NUM_FEATURES))

    def transform(self, train, test) -> tuple:
        train_remainder = train.shape[0] % self.timestep
        test_remainder = test.shape[0] % self.timestep
        if train_remainder != 0:
            train = train[train_remainder:]
        if test_remainder != 0:
            test = test[test_remainder:]
        return self.window_and_reshape(train), self.window_and_reshape(test)

    def etl(self) -> tuple:
        train, test = self.split_data()
        return self.transform(train, test)

    def to_supervised(self, data, n_out=5) -> tuple:
        flattened = data.reshape((data.shape[0]*data.shape[1], data.shape[2]))
        X, y = [], []
        in_start = 0
        while True:
            in_end = in_start + self.n_input
            out_end = in_end + n_out
            if out_end > len(flattened):
                break
            X.append(flattened[in_start:in_end, 0].reshape(-1,1))
            y.append(flattened[in_end:out_end, 0])
            in_start += 1
        return np.array(X), np.array(y)

class PredictAndForecast:
    def __init__(self, model, train, test, n_input=5) -> None:
        self.model = model
        self.train = train
        self.test = test
        self.n_input = n_input
        self.predictions = self.get_predictions()

    def forecast(self, history) -> np.array:
        data = np.array(history)
        data = data.reshape((data.shape[0]*data.shape[1], data.shape[2]))
        input_x = data[-self.n_input:, :]
        input_x = input_x.reshape((1, self.n_input, data.shape[1]))
        yhat = self.model.predict(input_x, verbose=0)
        return yhat[0]

    def get_predictions(self) -> np.array:
        history = list(self.train)
        predictions = []
        for i in range(len(self.test)):
            yhat_seq = self.forecast(history)
            predictions.append(yhat_seq)
            history.append(self.test[i, :])
        return np.array(predictions)

class Evaluate:
    def __init__(self, actual, predictions) -> None:
        if len(actual) == 0 or len(predictions) == 0:
            raise ValueError("Actual or Predicted arrays are empty")
        min_len = min(len(actual), len(predictions))
        if len(actual) != len(predictions):
            print(f"Warning: Length mismatch detected. Truncating to {min_len}.")
        self.actual = actual[:min_len]
        self.predictions = predictions[:min_len]

        self.var_ratio = self.compare_var()
        self.mape = self.evaluate_model_with_mape()

    def compare_var(self):
        var_actual = np.var(self.actual)
        if var_actual == 0:
            return float('nan')  # Cannot divide by zero variance
        return abs(1 - (np.var(self.predictions) / var_actual))

    def evaluate_model_with_mape(self):
        return mean_absolute_percentage_error(self.actual.flatten(), self.predictions.flatten())

def transformer_encoder(inputs, head_size, num_heads, ff_dim, dropout=0, epsilon=1e-6, attention_axes=None, kernel_size=1):
    x = layers.LayerNormalization(epsilon=epsilon)(inputs)
    x = layers.MultiHeadAttention(key_dim=head_size, num_heads=num_heads, dropout=dropout, attention_axes=attention_axes)(x, x)
    x = layers.Dropout(dropout)(x)
    res = x + inputs
    x = layers.LayerNormalization(epsilon=epsilon)(res)
    x = layers.Conv1D(filters=ff_dim, kernel_size=kernel_size, activation="relu")(x)
    x = layers.Dropout(dropout)(x)
    x = layers.Conv1D(filters=inputs.shape[-1], kernel_size=kernel_size)(x)
    return x + res

def build_transformer(head_size, num_heads, ff_dim, num_trans_blocks, mlp_units, dropout=0, mlp_dropout=0, attention_axes=None, epsilon=1e-6, kernel_size=1):
    n_timesteps, n_features, n_outputs = 5, 1, 5
    inputs = tf.keras.Input(shape=(n_timesteps, n_features))
    x = inputs
    for _ in range(num_trans_blocks):
        x = transformer_encoder(x, head_size, num_heads, ff_dim, dropout, epsilon, attention_axes, kernel_size)
    x = layers.GlobalAveragePooling1D(data_format="channels_first")(x)
    for dim in mlp_units:
        x = layers.Dense(dim, activation="relu")(x)
        x = layers.Dropout(mlp_dropout)(x)
    outputs = layers.Dense(n_outputs)(x)
    return tf.keras.Model(inputs, outputs)

def fit_transformer(transformer: tf.keras.Model, data: ETL):
    transformer.compile(loss="mse",
                        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
                        metrics=["mae", "mape"])
    callbacks = [tf.keras.callbacks.EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)]
    start = time.time()
    history = transformer.fit(data.X_train, data.y_train, batch_size=20, epochs=500, verbose=1, callbacks=callbacks)
    print(f"Training time: {time.time() - start:.2f}s")
    return history

def main():
    Ticker = 'MSFT'
    print("Starting ETL process...")
    data = ETL(Ticker)

    print("Building transformer model...")
    transformer = build_transformer(head_size=64, num_heads=4, ff_dim=2, num_trans_blocks=4,
                                    mlp_units=[256], mlp_dropout=0.10, dropout=0.10, attention_axes=1)

    transformer.summary()

    print("Training model...")
    fit_transformer(transformer, data)

    print("Generating predictions...")
    preds = PredictAndForecast(transformer, data.train, data.test)

    print("Evaluating performance...")
    evaluation = Evaluate(data.y_test, preds.predictions)
    print(f"Variance Ratio: {evaluation.var_ratio}")
    print(f"MAPE: {evaluation.mape}")

if __name__ == "__main__":
    main()
