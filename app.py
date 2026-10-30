import cv2
import mediapipe as mp
import keyboard
import time


mp_hand = mp.solutions.hands.Hands(max_num_hands=1)

cap = cv2.VideoCapture(0)

finger_counter_open = 0
finger_counter_close = 0
countdown_state = ''
action_triggered = False

finger_tips_open = [8, 12]
finger_tips_close = [16, 20]

def volume_down():
    for _ in range(10):
        keyboard.press_and_release('volume down')
        time.sleep(0.05)

def volume_up():
    for _ in range(10):
        keyboard.press_and_release('volume up')
        time.sleep(0.05)

while True:
    finger_counter_open = 0
    finger_counter_close = 0
    success, frame = cap.read()
    if not success:
        break

    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = mp_hand.process(frameRGB)
    countdown_state = ''

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            landmark = hand.landmark

            for tip in finger_tips_open:
                if landmark[tip].y < landmark[tip-2].y:
                    finger_counter_open += 1

            for tip in finger_tips_close:
                if landmark[tip].y > landmark[tip-2].y:
                    finger_counter_close += 1

            if landmark[4].x < landmark[3].x:
                finger_counter_close += 1


            if finger_counter_open == 2 and finger_counter_close == 1:
                countdown_state = '3'
            elif finger_counter_open == 1 and finger_counter_close == 2:
                countdown_state = '2'
            elif finger_counter_open == 1 and finger_counter_close == 3:
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