import pyaudio
import numpy as np
from scipy.io import wavfile
import tensorflow as tf
import matplotlib.pyplot as plt

SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms


p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paFloat32,channels=1,rate=SAMPLE_RATE,input=True,
              frames_per_buffer=CHUNK_SIZE)

i = 0
buffer = np.array([])
while True:
    data = np.fromstring(stream.read(CHUNK_SIZE),dtype=np.float32)
    print(type(data))
    print(len(data))
    if buffer.size 
    buffer = np.append(buffer, data)
    print(len(buffer))
    # print(data)
    # print(type(data))
    # print(len(data))
    i += 1
    # print(int(np.average(np.abs(data))))

print(len(buffer))

interpreter = tf.lite.Interpreter(model_path="conv.tflite")
interpreter.allocate_tensors()
input_data = np.array(buffer[:16000]/32767.0, dtype=np.float32).reshape((16000, 1))
interpreter.set_tensor(interpreter.get_input_details()[0]['index'], input_data)
interpreter.set_tensor(interpreter.get_input_details()[1]['index'], np.int32(SAMPLE_RATE)) 
output = interpreter.tensor(interpreter.get_output_details()[0]["index"])
interpreter.invoke()
output = interpreter.get_tensor(interpreter.get_output_details()[0]['index'])
plt.bar(['silence', 'unknown', 'buliya'], output[0])
plt.title(f'Predictions for buliya')
plt.show()
for i in output[0]:
  print(i, end=' ')


stream.stop_stream()
stream.close()
p.terminate()
