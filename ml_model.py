
import numpy as np
class SimpleMLModel:
    def predict(self, features):
        return np.tanh(np.mean(features))
ml_model = SimpleMLModel()
