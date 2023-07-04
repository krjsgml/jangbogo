import socket
from _thread import *
import time
import RPi.GPIO as GPIO

HOST
PORT

print('connect server')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# GPIO 핀 번호 설정

# 리니어 모터
Dir_Linear = 13
SPD = 11
BRK = 15

# 오른쪽 모터
IN1 = 29
IN2 = 31
PWM1 = 35

# 왼쪽 모터
IN3 = 40
IN4 = 38
PWM2 = 36

GPIO.setwarnings(False)
# 리니어 모터
GPIO.setmode(GPIO.BOARD)          # 핀번호 설정을 BOARD 방식으로 지정
GPIO.setup(Dir_Linear, GPIO.OUT)      # 방향 설정 핀을 출력 핀으로 설정
GPIO.setup(SPD, GPIO.OUT)          # 속도 제어 핀을 출력 핀으로 설정
GPIO.setup(BRK, GPIO.OUT)          # 브레이크 제어 핀을 출력 핀으로 설정

#DC 모터
GPIO.setup(IN1, GPIO.OUT)          # IN1 핀을 출력 핀으로 설정
GPIO.setup(IN2, GPIO.OUT)          # IN2 핀을 출력 핀으로 설정
GPIO.setup(PWM1, GPIO.OUT)       # PWM1 핀을 출력 핀으로 설정

GPIO.setup(IN3, GPIO.OUT)          # IN3 핀을 출력 핀으로 설정
GPIO.setup(IN4, GPIO.OUT)          # IN4 핀을 출력 핀으로 설정
GPIO.setup(PWM2, GPIO.OUT)       # PWM2 핀을 출력 핀으로 설정

pwm1 = GPIO.PWM(PWM1, 10) # PWM1 설정
pwm2 = GPIO.PWM(PWM2, 10) # PWM2 설정
pwm1.start(0)
pwm2.start(0)

GPIO.output(IN1, GPIO.HIGH) # IN1 핀 출력 설정
GPIO.output(IN2, GPIO.LOW) # IN2 핀 출력 설정
GPIO.output(IN3, GPIO.HIGH) # IN3 핀 출력 설정
GPIO.output(IN4, GPIO.LOW) # IN4 핀 출력 설정

while True:
    data = client_socket.recv(1024)
    try:
        sig = data.decode()
    except:
        continue

    if sig == '1':
        print('linear down ------ ')
        tracking_motor = 1
        
        GPIO.output(Dir_Linear, GPIO.HIGH) # 전진 방향 설정
        GPIO.output(BRK, GPIO.LOW) # 브레이크 해제
        pwm = GPIO.PWM(SPD, 100) # PWM 설정
        pwm.start(100) # 속도 설정
        time.sleep(8) # 2초 동안 구동
        pwm.stop() # PWM 정지
        GPIO.output(BRK, GPIO.HIGH) # 브레이크 설정

    elif sig == '0':
        tracking_motor = 0
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)
        print('linear up ------ ')

        GPIO.output(Dir_Linear, GPIO.LOW) # 후진 방향 설정
        GPIO.output(BRK, GPIO.LOW) # 브레이크 해제
        pwm = GPIO.PWM(SPD, 100) # PWM 설정
        pwm.start(100) # 속도 설정
        time.sleep(8) # 2초 동안 구동
        pwm.stop() # PWM 정지
        GPIO.output(BRK, GPIO.HIGH) # 브레이크 설정

    if tracking_motor == 1:
        if sig == 'w':
            print("left top")
            pwm1.ChangeDutyCycle(15*100/255)
            pwm2.ChangeDutyCycle(30*100/255)

        elif sig == 'e':
            print("center top")
            pwm1.ChangeDutyCycle(30*100/255)
            pwm2.ChangeDutyCycle(30*100/255)
        
        elif sig == 'r':
            print("right top")
            pwm1.ChangeDutyCycle(30*100/255)
            pwm2.ChangeDutyCycle(15*100/255)
        
        elif sig == 's':
            print("left middle")
            pwm1.ChangeDutyCycle(10*100/255)
            pwm2.ChangeDutyCycle(25*100/255)

        elif sig == 'd':
            print("center middle")
            pwm1.ChangeDutyCycle(20*100/255)
            pwm2.ChangeDutyCycle(20*100/255)

        elif sig == 'f':
            print("right middle")
            pwm1.ChangeDutyCycle(25*100/255)
            pwm2.ChangeDutyCycle(10*100/255)

        elif sig == 'x':
            print("left bottom")
            pwm1.ChangeDutyCycle(30*100/255)
            pwm2.ChangeDutyCycle(50*100/255)

        elif sig == 'c':
            print("center bottom")
            pwm1.ChangeDutyCycle(50*100/255)
            pwm2.ChangeDutyCycle(50*100/255)

        elif sig == 'v':
            print("right bottom")
            pwm1.ChangeDutyCycle(50*100/255)
            pwm2.ChangeDutyCycle(30*100/255)

        elif sig == 'q':
            print('stop')
            pwm1.ChangeDutyCycle(0)
            pwm2.ChangeDutyCycle(0)
    
    elif tracking_motor == 0:
        continue
    
GPIO.cleanup() # GPIO 초기화
