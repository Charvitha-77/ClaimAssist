import json
import numpy as np
import joblib
from azureml.core.model import Model

def init():
    global model
    model_path = Model.get_model_path("lightgbm_model")
    model = joblib.load(model_path)

def run(data):
    try:
        data = json.loads(data)
        prediction = model.predict(np.array(data['data']))
        return json.dumps({"result": prediction.tolist()})
    except Exception as e:
        return json.dumps({"error": str(e)})
