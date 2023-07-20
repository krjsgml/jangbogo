import socket
from _thread import *
import time
#import RPi.GPIO as GPIO

HOST = '172.30.1.63'
PORT = 3333

print('connect server')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# GPIO 핀 번호 설정

## hc-sr04
#trig = 33
#echo = 37
#
## 리니어 모터
#Dir_Linear = 13
#SPD = 11
#BRK = 15
#
## 오른쪽 모터
#IN1 = 29
#IN2 = 31
#PWM1 = 35
#
## 왼쪽 모터
#IN3 = 40
#IN4 = 38
#PWM2 = 36
#
#GPIO.setwarnings(False)
## 리니어 모터
#GPIO.setmode(GPIO.BOARD)                    # 핀번호 설정을 BOARD 방식으로 지정
#GPIO.setup(Dir_Linear, GPIO.OUT)            # 방향 설정 핀을 출력 핀으로 설정
#GPIO.setup(SPD, GPIO.OUT)                   # 속도 제어 핀을 출력 핀으로 설정
#GPIO.setup(BRK, GPIO.OUT)                   # 브레이크 제어 핀을 출력 핀으로 설정
#
## hc-sr04
#GPIO.setup(trig, GPIO.OUT)
#GPIO.setup(echo, GPIO.IN)
#
##DC 모터
#GPIO.setup(IN1, GPIO.OUT)                   # IN1 핀을 출력 핀으로 설정
#GPIO.setup(IN2, GPIO.OUT)                   # IN2 핀을 출력 핀으로 설정
#GPIO.setup(PWM1, GPIO.OUT)                  # PWM1 핀을 출력 핀으로 설정
#
#GPIO.setup(IN3, GPIO.OUT)                   # IN3 핀을 출력 핀으로 설정
#GPIO.setup(IN4, GPIO.OUT)                   # IN4 핀을 출력 핀으로 설정
#GPIO.setup(PWM2, GPIO.OUT)                  # PWM2 핀을 출력 핀으로 설정
#
#pwm1 = GPIO.PWM(PWM1, 490)                  # PWM1 설정
#pwm2 = GPIO.PWM(PWM2, 490)                  # PWM2 설정
#pwm1.start(0)
#pwm2.start(0)
#
#GPIO.output(IN1, GPIO.HIGH)                 # IN1 핀 출력 설정
#GPIO.output(IN2, GPIO.LOW)                  # IN2 핀 출력 설정
#GPIO.output(IN3, GPIO.HIGH)                 # IN3 핀 출력 설정
#GPIO.output(IN4, GPIO.LOW)                  # IN4 핀 출력 설정
#
#def move_forward(speed1, speed2):
#    GPIO.output(IN1, GPIO.HIGH)             # IN1 핀 출력 설정
#    GPIO.output(IN2, GPIO.LOW)              # IN2 핀 출력 설정
#    GPIO.output(IN3, GPIO.HIGH)             # IN3 핀 출력 설정
#    GPIO.output(IN4, GPIO.LOW)              # IN4 핀 출력 설정
#    
#    pwm1.ChangeDutyCycle(speed1)
#    pwm2.ChangeDutyCycle(speed2)
#    
#def move_backward(speed1, speed2):
#    GPIO.output(IN1, GPIO.LOW)              # IN1 핀 출력 설정
#    GPIO.output(IN2, GPIO.HIGH)             # IN2 핀 출력 설정
#    GPIO.output(IN3, GPIO.LOW)              # IN3 핀 출력 설정
#    GPIO.output(IN4, GPIO.HIGH)             # IN4 핀 출력 설정
#    
#    pwm1.ChangeDutyCycle(speed1)
#    pwm2.ChangeDutyCycle(speed2)
#    
#def stop():
#    GPIO.output(IN1, GPIO.LOW)              # IN1 핀 출력 설정
#    GPIO.output(IN2, GPIO.LOW)              # IN2 핀 출력 설정
#    GPIO.output(IN3, GPIO.LOW)              # IN3 핀 출력 설정
#    GPIO.output(IN4, GPIO.LOW)              # IN4 핀 출력 설정
#    pwm1.ChangeDutyCycle(0)
#    pwm2.ChangeDutyCycle(0)
#    
#def linear_forward(speed):
#    GPIO.output(Dir_Linear, GPIO.HIGH)      # 전진 방향 설정
#    GPIO.output(BRK, GPIO.LOW)              # 브레이크 해제
#    pwm = GPIO.PWM(SPD, 100)                # PWM 설정
#    pwm.start(speed)                        # 속도 설정
#    time.sleep(8)                           # 2초 동안 구동
#    pwm.stop()                              # PWM 정지
#    GPIO.output(BRK, GPIO.HIGH)             # 브레이크 설정
#    
## HC-SR04 초음파 센서 : 센서값 읽기
#def calculate_distance():
#    GPIO.output(trig, GPIO.LOW)
#    time.sleep(0.1)
#    GPIO.output(trig, GPIO.HIGH)
#    time.sleep(0.00001)
#    GPIO.output(trig, GPIO.LOW)
#
#    while GPIO.input(echo) == 0:
#        pulse_start = time.time()
#
#    while GPIO.input(echo) == 1:
#        pulse_end = time.time()
#
#    pulse_duration = pulse_end - pulse_start
#    distance = pulse_duration * 17000
#    distance = round(distance, 2)
#
#    return distance
#
while True:
    data = client_socket.recv(1024)
    try:
        sig = data.decode()
    except:
        continue

    if sig == '1':
        print('linear down ------ ')
        motor_mode = 1
        
        #GPIO.output(Dir_Linear, GPIO.HIGH)      # 전진 방향 설정
        #GPIO.output(BRK, GPIO.LOW)              # 브레이크 해제
        #pwm = GPIO.PWM(SPD, 100)                # PWM 설정
        #pwm.start(100)                          # 속도 설정
        #time.sleep(8)                           # 2초 동안 구동
        #pwm.stop()                              # PWM 정지
        #GPIO.output(BRK, GPIO.HIGH)             # 브레이크 설정

    if sig == '2':
        print('linear down ------ ')
        motor_mode = 2

        #GPIO.output(Dir_Linear, GPIO.HIGH)      # 전진 방향 설정
        #GPIO.output(BRK, GPIO.LOW)              # 브레이크 해제
        #pwm = GPIO.PWM(SPD, 100)                # PWM 설정
        #pwm.start(100)                          # 속도 설정
        #time.sleep(8)                           # 2초 동안 구동
        #pwm.stop()                              # PWM 정지
        #GPIO.output(BRK, GPIO.HIGH)             # 브레이크 설정

    elif sig == '0':
        motor_mode = 0
        print('linear up ------ ')
        #pwm1.ChangeDutyCycle(0)
        #pwm2.ChangeDutyCycle(0)

        #GPIO.output(Dir_Linear, GPIO.LOW)       # 후진 방향 설정
        #GPIO.output(BRK, GPIO.LOW)              # 브레이크 해제
        #pwm = GPIO.PWM(SPD, 100)                # PWM 설정
        #pwm.start(100)                          # 속도 설정
        #time.sleep(8)                           # 2초 동안 구동
        #pwm.stop()                              # PWM 정지
        #GPIO.output(BRK, GPIO.HIGH)             # 브레이크 설정

    if motor_mode == 1:
        if sig == 'f':
            print('right')
            #pwm1.ChangeDutyCycle(30*100/255)
            #pwm2.ChangeDutyCycle(15*100/255)

        elif sig == 'd':
            print("forward")
            #pwm1.ChangeDutyCycle(30*100/255)
            #pwm2.ChangeDutyCycle(30*100/255)
        
        elif sig == 's':
            print("left")
            #pwm1.ChangeDutyCycle(15*100/255)
            #pwm2.ChangeDutyCycle(30*100/255)
            
        elif sig == 'q':
            print('stop')
            #pwm1.ChangeDutyCycle(0)
            #pwm2.ChangeDutyCycle(0)

    if motor_mode == 2:
        # move lacation 'a'
        if sig == 'a': 
            print('move lacation a')
            #move_forward(20, 20)
            #time.sleep(12)
            #move_forward(15, 20)
            #time.sleep(1)
            #stop()
        
        if sig == 'b': 
            print('move lacation b')
            # move lacation 'b'
            #move_forward(15, 20)
            #time.sleep(3)
            #move_forward(20, 20)
            #time.sleep(2)
            #stop()

        if sig == 'c': 
            print('move lacation c')
            # move lacation 'c'
            #move_forward(20, 18)
            #time.sleep(12)
            #move_forward(20, 15)
            #time.sleep(1)
            #stop()

        if sig == 'd': 
            print('move lacation d')
            # move lacation 'd'
            #move_forward(20, 15)
            #time.sleep(3)
            #move_forward(20, 20)
            #time.sleep(2)
            #stop()#

    elif motor_mode == 0:
        continue

GPIO.cleanup() # GPIO 초기화