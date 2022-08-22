import numpy as np
from scipy.io import wavfile
import tensorflow as tf
import matplotlib.pyplot as plt

interpreter = tf.lite.Interpreter(model_path="conv.tflite")
# print(interpreter.get_input_details())

# for tensor_detail in interpreter.get_tensor_details():
#     print(tensor_detail)

# print(interpreter.get_input_details())
# print(interpreter.get_output_details())

# 인터프리터에 텐서들을 배정한다. 이 작업을 통해서 데이터가 입력될 때 데이터가 계산되는 길이 정의된다.
interpreter.allocate_tensors()

# 인식하고자 하는 웨이브파일을 읽어온다.
samplerate, data = wavfile.read("C:\\Users\\eunji\\Downloads\\55.wav")

# 첫 번쨰 input을 입력한다. 그래프를 분석하면 (16000, 1)shape의 [0,1)의 np.float32임을 확인할 수 있다. 그것에 맞춰서 데이터를 수정하자
input_data = np.array(data[:16000]/32767.0, dtype=np.float32).reshape((16000, 1))
interpreter.set_tensor(interpreter.get_input_details()[0]['index'], input_data)
# 두 번째 input을 입력한다. 16it 웨이브 파일이므로 16000이어야 한다.
interpreter.set_tensor(interpreter.get_input_details()[1]['index'], np.int32(samplerate)) 
output = interpreter.tensor(interpreter.get_output_details()[0]["index"])

# 키워드 인식을 실제로 실행시킨다.
interpreter.invoke()

# 실행결과를 읽어온다.
output = interpreter.get_tensor(interpreter.get_output_details()[0]['index'])

plt.bar(['silence', 'unknown', 'buliya'], output[0])
plt.title(f'Predictions for buliya')
plt.show()
for i in output[0]:
  print(i, end=' ')