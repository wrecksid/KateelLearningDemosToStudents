import argparse
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.metrics import mean_absolute_percentage_error
from keras import layers
import time
import datetime as dt


class ETL:
    """
    Extracts data for stock with ticker `ticker` from yf api,
    splits the data into train and test sets by date,
    reshapes the data into np.array of shape [#weeks, 5, 1],
    converts our problem into supervised learning problem.
    """
    def __init__(self, ticker, startdate, enddate, test_size=0.2, n_input=5, timestep=5) -> None:
        self.ticker = ticker
        self.startdate = startdate
        self.enddate = enddate
        self.test_size = test_size
        self.n_input = n_input
        self.df = self.extract_historic_data()
        self.timestep = timestep
        self.train, self.test = self.etl()
        self.X_train, self.y_train = self.to_supervised(self.train)
        self.X_test, self.y_test = self.to_supervised(self.test)

    def extract_historic_data(self) -> pd.Series:
        """
        gets historical data from yf api.
        """
        t = yf.Ticker(self.ticker)
        history = t.history(start=self.startdate, end=self.enddate, interval='1d')
        return history.Close

    def split_data(self) -> tuple:
        """
        Splits our pd.Series into train and test series with
        test series representing test_size * 100 % of data.
        """
        data = self.df
        if len(data) != 0:
            train_idx = round(len(data) * (1 - self.test_size))
            train = data[:train_idx]
            test = data[train_idx:]
            train = np.array(train)
            test = np.array(test)
            return train[:, np.newaxis], test[:, np.newaxis]
        else:
            raise Exception('Data set is empty, cannot split.')

    def window_and_reshape(self, data) -> np.array:
        """
        Reformats data into shape our model needs,
        namely, [# samples, timestep, # features]
        """
        NUM_FEATURES = 1
        samples = int(data.shape[0] / self.timestep)
        result = np.array(np.array_split(data, samples))
        return result.reshape((samples, self.timestep, NUM_FEATURES))

    def transform(self, train, test) -> tuple:
        train_remainder = train.shape[0] % self.timestep
        test_remainder = test.shape[0] % self.timestep

        if train_remainder != 0 and test_remainder != 0:
            train = train[train_remainder:]
            test = test[test_remainder:]
        elif train_remainder != 0:
            train = train[train_remainder:]
        elif test_remainder != 0:
            test = test[test_remainder:]
        return self.window_and_reshape(train), self.window_and_reshape(test)

    def etl(self) -> tuple:
        """
        Runs complete ETL
        """
        train, test = self.split_data()
        return self.transform(train, test)

    def to_supervised(self, train, n_out=5) -> tuple:
        """
        Converts time series problem to supervised learning problem.
        """
        data = train.reshape((train.shape[0] * train.shape[1], train.shape[2]))
        X, y = [], []
        in_start = 0
        for _ in range(len(data)):
            in_end = in_start + self.n_input
            out_end = in_end + n_out
            if out_end <= len(data):
                x_input = data[in_start:in_end, 0]
                x_input = x_input.reshape((len(x_input), 1))
                X.append(x_input)
                y.append(data[in_end:out_end, 0])
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
        data = data.reshape((data.shape[0] * data.shape[1], data.shape[2]))
        input_x = data[-self.n_input:, :]
        input_x = input_x.reshape((1, len(input_x), input_x.shape[1]))
        yhat = self.model.predict(input_x, verbose=0)[0]
        return yhat

    def get_predictions(self) -> np.array:
        history = [x for x in self.train]
        predictions = []
        for i in range(len(self.test)):
            yhat_sequence = self.forecast(history)
            predictions.append(yhat_sequence)
            history.append(self.test[i, :])
        return np.array(predictions)


class Evaluate:
    def __init__(self, actual, predictions) -> None:
        self.actual = actual
        self.predictions = predictions
        self.var_ratio = self.compare_var()
        self.mape = self.evaluate_model_with_mape()

    def compare_var(self):
        return abs(1 - (np.var(self.predictions) / np.var(self.actual)))

    def evaluate_model_with_mape(self):
        return mean_absolute_percentage_error(self.actual.flatten(), self.predictions.flatten())


def transformer_encoder(inputs, head_size, num_heads, ff_dim, dropout=0, epsilon=1e-6,
                        attention_axes=None, kernel_size=1):
    x = layers.LayerNormalization(epsilon=epsilon)(inputs)
    x = layers.MultiHeadAttention(key_dim=head_size, num_heads=num_heads, dropout=dropout,
                                  attention_axes=attention_axes)(x, x)
    x = layers.Dropout(dropout)(x)
    res = x + inputs

    x = layers.LayerNormalization(epsilon=epsilon)(res)
    x = layers.Conv1D(filters=ff_dim, kernel_size=kernel_size, activation="relu")(x)
    x = layers.Dropout(dropout)(x)
    x = layers.Conv1D(filters=inputs.shape[-1], kernel_size=kernel_size)(x)
    return x + res


def build_transformer(head_size, num_heads, ff_dim, num_trans_blocks,
                      mlp_units, dropout=0, mlp_dropout=0, attention_axes=None,
                      epsilon=1e-6, kernel_size=1):
    n_timesteps, n_features, n_outputs = 5, 1, 5
    inputs = tf.keras.Input(shape=(n_timesteps, n_features))
    x = inputs
    for _ in range(num_trans_blocks):
        x = transformer_encoder(x, head_size=head_size, num_heads=num_heads, ff_dim=ff_dim,
                                dropout=dropout, attention_axes=attention_axes,
                                kernel_size=kernel_size, epsilon=epsilon)

    x = layers.GlobalAveragePooling1D(data_format="channels_first")(x)
    for dim in mlp_units:
        x = layers.Dense(dim, activation="relu")(x)
        x = layers.Dropout(mlp_dropout)(x)

    outputs = layers.Dense(n_outputs)(x)
    return tf.keras.Model(inputs, outputs)


def fit_transformer(transformer: tf.keras.Model, data: ETL):
    transformer.compile(
        loss="mse",
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
        metrics=["mae", 'mape'])
    callbacks = [tf.keras.callbacks.EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)]
    start = time.time()
    hist = transformer.fit(data.X_train, data.y_train, batch_size=20, epochs=500, verbose=1, callbacks=callbacks)
    print('Training time:', time.time() - start)
    return hist


def main():
    parser = argparse.ArgumentParser(description="Transformer Stock Price Predictor")
    parser.add_argument('--ticker', type=str, default='AAPL', help="Stock ticker symbol (default: AAPL)")
    parser.add_argument('--startdate', type=str, default='2010-01-01', help="Start date YYYY-MM-DD (default: 2010-01-01)")
    parser.add_argument('--enddate', type=str, default='2025-02-15', help="End date YYYY-MM-DD (default: 2025-02-15)")
    args = parser.parse_args()

    # Parse dates to datetime objects
    startdate = dt.datetime.strptime(args.startdate, '%Y-%m-%d').date()
    enddate = dt.datetime.strptime(args.enddate, '%Y-%m-%d').date()

    data = ETL(args.ticker, startdate, enddate)

    transformer = build_transformer(head_size=64, num_heads=4, ff_dim=2, num_trans_blocks=4,
                                    mlp_units=[256], mlp_dropout=0.10, dropout=0.10, attention_axes=1)

    transformer.summary()

    hist = fit_transformer(transformer, data)

    start = time.time()
    transformer_preds = PredictAndForecast(transformer, data.train, data.test)
    print('Prediction time:', time.time() - start)

    evaluation = Evaluate(data.y_test, transformer_preds.predictions)
    print('Variance comparison ratio:', evaluation.var_ratio)
    print('MAPE:', evaluation.mape)

    plt.plot(hist.history['loss'])
    plt.title('Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.show()


if __name__ == "__main__":
    main()
