import pyaudio
import numpy as np

import tensorflow as tf
import librosa
from tflite_support import metadata
import json
import os


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
  input_tensor_metadata = metadata_json['subgraph_metadata'][0]['input_tensor_metadata'][0]
  input_content_props = input_tensor_metadata['content']['content_properties']
  return input_content_props['sample_rate']


SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)

p = pyaudio.PyAudio()

stream = p.open(
    format=pyaudio.paFloat32,
    channels=1,
    rate=SAMPLE_RATE,
    input=True,
    frames_per_buffer=CHUNK_SIZE
)


# Get a WAV file for inference and list of labels from the model
tflite_file = 'model/browserfft-speech.tflite'
labels = get_labels(tflite_file)
random_audio = 'model/data/55.wav'

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

print(audio_data.shape)

# Run inference
interpreter.allocate_tensors()
interpreter.set_tensor(input_details[0]['index'], audio_data)
interpreter.invoke()
output_data = interpreter.get_tensor(output_details[0]['index'])

# Display prediction and ground truth
top_index = np.argmax(output_data[0])
label = labels[top_index]
score = output_data[0][top_index]
print('---prediction---')
print(f'Class: {label}\nScore: {score}')


buffer = np.array([], dtype=np.float32)

while True:
    data = np.fromstring(stream.read(input_size//10),dtype=np.float32)
    print(type(data[0]))
    if len(buffer) >= input_size:
        # if len(buffer) < input_size:
        #     buffer.resize(input_size)
        buffer = np.expand_dims(buffer[:input_size], axis=0)
        print(buffer.shape)
        interpreter.allocate_tensors()
        interpreter.set_tensor(input_details[0]['index'], buffer)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])

        # Display prediction and ground truth
        top_index = np.argmax(output_data[0])
        label = labels[top_index]
        score = output_data[0][top_index]
        print('---prediction---')
        print(f'Class: {label}\nScore: {score}')

        buffer = np.delete(buffer, range(0,input_size//10))
    buffer = np.append(buffer, data)

    

    print(len(buffer))





stream.stop_stream()
stream.close()
p.terminate()