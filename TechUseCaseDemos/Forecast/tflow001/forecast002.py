import numpy as np
from sklearn.metrics import mean_absolute_percentage_error

class ETL:
    # ... (keep your existing ETL class code, no change)
    # You may add input validation if desired, but your ETL class is fine as is.

class PredictAndForecast:
    def __init__(self, model, train, test, n_input=5) -> None:
        self.model = model
        self.train = train
        self.test = test
        self.n_input = n_input
        try:
            self.predictions = self.get_predictions()
        except Exception as e:
            raise RuntimeError(f"Failed to generate predictions: {e}")

    def forecast(self, history) -> np.array:
        try:
            data = np.array(history)
            data = data.reshape((data.shape[0]*data.shape[1], data.shape[2]))
            input_x = data[-self.n_input:, :]
            input_x = input_x.reshape((1, len(input_x), input_x.shape[1]))
            yhat = self.model.predict(input_x, verbose=0)
            yhat = yhat[0]
            return yhat
        except Exception as e:
            raise RuntimeError(f"Forecast error: {e}")

    def get_predictions(self) -> np.array:
        history = [x for x in self.train]
        predictions = []
        try:
            for i in range(len(self.test)):
                yhat_sequence = self.forecast(history)
                predictions.append(yhat_sequence)
                history.append(self.test[i, :])
            return np.array(predictions)
        except Exception as e:
            raise RuntimeError(f"Error during walk-forward prediction: {e}")

class Evaluate:
    def __init__(self, actual: np.array, predictions: np.array) -> None:
        if actual is None or predictions is None:
            raise ValueError("Actual or predictions cannot be None.")
        if len(actual) == 0 or len(predictions) == 0:
            raise ValueError("Actual and predictions must not be empty.")

        min_len = min(len(actual), len(predictions))
        if len(actual) != len(predictions):
            print(f"Warning: Length mismatch between actual ({len(actual)}) and predictions ({len(predictions)}). Truncating to {min_len}.")

        self.actual = actual[:min_len]
        self.predictions = predictions[:min_len]

        self.var_ratio = self.compare_var()
        self.mape = self.evaluate_model_with_mape()

    def compare_var(self) -> float:
        try:
            var_pred = np.var(self.predictions)
            var_actual = np.var(self.actual)
            if var_actual == 0:
                print("Warning: Variance of actual data is zero, variance ratio set to NaN.")
                return np.nan
            return abs(1 - (var_pred / var_actual))
        except Exception as e:
            print(f"Error computing variance ratio: {e}")
            return np.nan

    def evaluate_model_with_mape(self) -> float:
        try:
            return mean_absolute_percentage_error(self.actual.flatten(), self.predictions.flatten())
        except Exception as e:
            raise RuntimeError(f"Error computing MAPE: {e}")

def main():
    try:
        Ticker = 'MSFT'
        
        # Load and prepare data
        data = ETL(Ticker)
        
        # Build and train your transformer model (assuming build_transformer and fit_transformer are defined)
        transformer = build_transfromer(head_size=64, num_heads=4, ff_dim=2, num_trans_blocks=4,
                                       mlp_units=[256], mlp_dropout=0.10, dropout=0.10, attention_axes=1)
        fit_transformer(transformer)
        
        # Generate predictions
        transformer_preds = PredictAndForecast(transformer, data.train, data.test)
        
        # Evaluate with safe handling of length mismatch
        evaluation = Evaluate(data.y_test, transformer_preds.predictions)
        
        print(f"Variance Ratio: {evaluation.var_ratio}")
        print(f"MAPE: {evaluation.mape}")
        
    except Exception as e:
        print(f"An error occurred in main execution: {e}")

# Ensure execution is only triggered in main run context
if __name__ == "__main__":
    main()
