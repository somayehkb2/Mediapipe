import cv2
import mediapipe as mp
import keyboard
import time

mp_hand = mp.solutions.hands.Hands(max_num_hands=1)
cap = cv2.VideoCapture(0)

countdown_state = ''
action_triggered = False


def volume_down():
    for _ in range(10):
        keyboard.press_and_release('volume down')
        time.sleep(0.05)


def volume_up():
    for _ in range(10):
        keyboard.press_and_release('volume up')
        time.sleep(0.05)


while True:
    success, frame = cap.read()
    if not success:
        break

    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = mp_hand.process(frameRGB)
    countdown_state = ''

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            landmark = hand.landmark

            
            index_open  = landmark[8].y  < landmark[6].y    # اشاره
            middle_open = landmark[12].y < landmark[10].y   # وسط
            ring_open   = landmark[16].y < landmark[14].y   # حلقه
            pinky_open  = landmark[20].y < landmark[18].y   # کوچک
            thumb_open  = landmark[4].x  < landmark[3].x    # شست

            
            if (middle_open and ring_open and pinky_open
                    and not index_open and not thumb_open):
                countdown_state = '3'

            
            elif (ring_open and pinky_open
                    and not middle_open and not index_open and not thumb_open):
                countdown_state = '2'

            
            elif (pinky_open
                    and not ring_open and not middle_open
                    and not index_open and not thumb_open):
                countdown_state = '1'

                if not action_triggered:
                    print("شمارش کامل شد! کم کردن صدا...")
                    volume_down()
                    time.sleep(1.0)
                    volume_up()
                    print("صدا دوباره زیاد شد.")
                    action_triggered = True

            else:
                action_triggered = False

    
    if countdown_state != '':
        cv2.putText(frame, countdown_state, (50, 150),
                    cv2.FONT_HERSHEY_COMPLEX, 4, (0, 255, 0), 4)

    cv2.imshow('WebCam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()