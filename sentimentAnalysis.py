import pickle
import os
import numpy as np

class CustomModelPrediction(object):

  def __init__(self, model, processor):
    self._model = model
    self._processor = processor
  
  def predict(self, instances, **kwargs):
    preprocessed_data = self._processor.transform_text(instances)
    predictions = self._model.predict(preprocessed_data)
    return predictions.tolist()

  @classmethod
  def from_path(cls, model_dir):
    import tensorflow.keras as keras
    model = keras.models.load_model(
      os.path.join(model_dir,'keras_saved_model_en_1800.h5'))
    with open(os.path.join(model_dir, 'processor_state_en_1800.pkl'), 'rb') as f:
      processor = pickle.load(f)

    return cls(model, processor)

def analyseEnglish(test_requests):
    classifier = CustomModelPrediction.from_path('.')
    results = classifier.predict(test_requests)
    labels=['Negative','Neutral']
    for i in range(len(results)):
        for idx,val in enumerate(results[i]):
            if val > 0.7:
                return str(labels[idx]),  str(val)

def analyseHindi(test_requests):
    classifier = CustomModelPrediction.from_path('.', 'keras_saved_model.h5', 'processor_state.pkl')
    results = classifier.predict(test_requests)
    labels=['Negative','Neutral']
    for i in range(len(results)):
        for idx,val in enumerate(results[i]):
            if val > 0.7:
                return str(labels[idx]),  str(val)

# analyseEnglish(['Hello this is an app'])