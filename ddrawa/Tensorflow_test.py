# TensorFlow and tf.keras
import tensorflow as tf
import numpy as np
import cv2
from camera import gstreamer_pipeline
from motor import Robot
# Load TFLite model and allocate tensors.
#interpreter = tf.lite.Interpreter(model_path="./saved_model/my_model.quant.tflite")
interpreter = tf.lite.Interpreter(model_path="./new_new_tastcase_001_E100.tflite")
interpreter.allocate_tensors()
# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
# Test model on random input data.
input_shape = input_details[0]['shape']
robot = Robot()

cap_down = cv2.VideoCapture(gstreamer_pipeline(sensor_id = 0, flip_method = 0), cv2.CAP_GSTREAMER)
#input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
# input_data = np.array(np.random.randint(0,1000, size=input_shape), dtype=np.float32)
while True:
    # left_val = 0.45
    # right_val = 0.45
    left_val = 0.4
    right_val = 0.4
    ret, frame = cap_down.read()
    if ret:
        try:
            #input_data = np.array([[1]], dtype=np.float32)
            # print("input : %s" % input_data)
            input_data = frame.copy()
            input_data = input_data.astype(np.float32)
            input_data = cv2.resize(input_data, (224,224))
            input_data = np.expand_dims(input_data, axis=0)
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()
            # The function `get_tensor()` returns a copy of the tensor data.
            # Use `tensor()` in order to get a pointer to the tensor.
            output_data = interpreter.get_tensor(output_details[0]['index'])

            res = np.argmax(output_data)
            print('res', res)
            if res == 0:
                robot.motors2(left_val, right_val)
            elif res == 1:
                robot.motors2(left_val*0.4, right_val*0.8)
                # time.sleep(0.05)
            elif res == 2:
                robot.motors2(left_val*0.8, right_val*0.4)
                # time.sleep(0.05)
            frame = cv2.flip(frame,0)
            frame = cv2.flip(frame,1)

            # cv2.imshow('frame',frame)
            if cv2.waitKey(1) == 27:
                break
        except KeyboardInterrupt as ke:
            break
        except Exception as e:
            print(e)
            break

cap_down.release()
robot.stop()
robot.init()
# cv2.destroyAllWindows()
print("프로그램 종료")
