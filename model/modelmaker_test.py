"""
https://www.tensorflow.org/lite/models/modify/model_maker/speech_recognition
model_maker speech_recognition 예제 파일로 만든 model test.
테스트할 모델의 경로와 테스트할 wav파일을 하위 data폴더 안에 넣은 후 테스트하면 됩니다.
"""

import numpy as np
from scipy.io import wavfile
import tensorflow as tf
import matplotlib.pyplot as plt
from tflite_support import metadata
import librosa
import json
from IPython.display import Audio


def get_labels(model):
  """Returns a list of labels, extracted from the model metadata."""
  displayer = metadata.MetadataDisplayer.with_model_file(model)
  labels_file = displayer.get_packed_associated_file_list()[0]
  labels = displayer.get_associated_file_buffer(labels_file).decode()
  return [line for line in labels.split('\n')]

def get_input_sample_rate(model):
  """Returns the model's expected sample rate, from the model metadata."""
  displayer = metadata.MetadataDisplayer.with_model_file(model)
  metadata_json = json.loads(displayer.get_metadata_json())
  input_tensor_metadata = metadata_json['subgraph_metadata'][0][
          'input_tensor_metadata'][0]
  input_content_props = input_tensor_metadata['content']['content_properties']
  return input_content_props['sample_rate']



# Get a WAV file for inference and list of labels from the model
tflite_file = 'lookout.tflite'
labels = get_labels(tflite_file)
random_audio = 'data/불이야.wav'

# Ensure the audio sample fits the model input
interpreter = tf.lite.Interpreter(tflite_file)
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_size = input_details[0]['shape'][1]
sample_rate = get_input_sample_rate(tflite_file)
audio_data, _ = librosa.load(random_audio, sr=sample_rate)



if len(audio_data) < input_size:
  audio_data.resize(input_size)
audio_data = np.expand_dims(audio_data[:input_size], axis=0)

print(len(audio_data))
print(audio_data.shape)
plt.title(random_audio)
plt.plot(audio_data[0])
plt.show()

# Run inference
interpreter.allocate_tensors()
interpreter.set_tensor(input_details[0]['index'], audio_data)
interpreter.invoke()
output_data = interpreter.get_tensor(output_details[0]['index'])

# Display prediction and ground truth
top_index = np.argmax(output_data[0])
label = labels[top_index]
score = output_data[0][top_index]

plt.bar(labels, output_data[0])
plt.title('prediction results')
plt.show()
print('---prediction---')
print(f'Class: {label}\nScore: {score}')