"""
speech-to-text with tensorflow lite model
use pyaudio to record your voice and generate streaming data to 44100Hz input data
"""


import pyaudio
import numpy as np
from six.moves import queue
import tensorflow as tf
import os, sys, pickle
from datetime import datetime

from firebase_db import FirebaseDB

filename = 'device_id.pickle'

# Load DEVICE_ID
if os.path.isfile(filename):
    # 파일에서 디바이스 uuid 로드
    with open(filename, 'rb') as f:
        DEVICE_ID = str(pickle.load(f))
else:
    sys.exit("error: Execute ./connect_device.py and regist your device first")

DEVICE_STATUS = True

RATE = 44100
CHUNK = int(RATE / 10)  # 100ms
WORD_THRESHOLD = 0.7  # prediction 값을 참이라고 판별하는 score threshold

class Model():
    """Init a model and set interpreter"""
    def __init__(self, model_path):
        self.labels = ['background', '불이야', '조심해', '도둑이야']
        self.interpreter = tf.lite.Interpreter(model_path)
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        self.input_size = self.input_details[0]['shape'][1]
        self.sample_rate = 44100

        self.interpreter.allocate_tensors()


    def set_input(self, audio):
        self.interpreter.set_tensor(self.input_details[0]['index'], audio)
        self.interpreter.invoke()
        return self.interpreter.get_tensor(self.output_details[0]['index'])



class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paFloat32,
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


def prediction(audio_gen):
    fb = FirebaseDB()
    model = Model(model_path='model/lookout.tflite')
    input_size = model.input_size
    window = []
    prev = ""
    for x in audio_gen:
        window.append(x)
        wav = np.fromstring(b''.join(window), dtype=np.float32)

        if len(wav) < input_size:
            wav.resize(input_size)
        wav = np.expand_dims(wav[-input_size:], axis=0)

        print('shape:',wav.shape)

        output_data = model.set_input(wav)
        print(output_data[0])

        top_index = np.argmax(output_data[0])
        label = model.labels[top_index]
        score = output_data[0][top_index]
        if score < WORD_THRESHOLD:  # WORD_THRESHOLD 값을 못넘겼을 경우 continue
            continue
        print('---prediction---')
        print(f'Class: {label}\nScore: {score}')

        if prev != 'background' and prev == label:  # 잘못 인식되는 case를 줄이기 위해 prediction 값이 연속으로 같을 경우에만 firebase에 업로드
            nowdate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            fb.update({
                str(DEVICE_ID):{
                "device_status":DEVICE_STATUS,
                "content":{
                    "message":['불이야', '조심해', '도둑이야'][top_index-1],
                    "datetime":nowdate
            }}})
            
        prev = label



def main():
    
    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        prediction(audio_generator)
        print(list(audio_generator))


if __name__ == '__main__':
    main()
    print("end main")