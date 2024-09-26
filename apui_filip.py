import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    fingerCount = 0
    fingers = 0

    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            

            y0 = hand_landmarks.landmark[0].y
            is_normal = all(point.y <= y0 for point in hand_landmarks.landmark[1:])
            is_upsideDown = all(point.y >= y0 for point in hand_landmarks.landmark[1:])
            is_left = all(point.x >= y0 for point in hand_landmarks.landmark[1:])
            is_right = all(point.x <= y0 for point in hand_landmarks.landmark[1:])
                
            if(is_normal):
                if(handedness.classification[0].label == "Right"):
                    if(hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x):
                            fingerCount += 1
                if(handedness.classification[0].label == "Left"):
                    if(hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x):
                            fingerCount += 1

                for x in range(0, 4):
                    if(hand_landmarks.landmark[8 + (4*x)].y < hand_landmarks.landmark[7 + (4*x)].y):
                        fingerCount += 1
                print("normal")
                    
            elif(is_upsideDown):
                if(handedness.classification[0].label == "Right"):
                    if(hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x):
                            fingerCount += 1
                if(handedness.classification[0].label == "Left"):
                    if(hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x):
                            fingerCount += 1

                for x in range(0, 4):
                    if(hand_landmarks.landmark[8 + (4*x)].y > hand_landmarks.landmark[7 + (4*x)].y):
                        fingerCount += 1
                print("upsidedown")

            elif(is_left):
                if(handedness.classification[0].label == "Right"):
                    if(hand_landmarks.landmark[4].y < hand_landmarks.landmark[3].y):
                            fingerCount += 1

                if(handedness.classification[0].label == "Left"):
                    if(hand_landmarks.landmark[4].y > hand_landmarks.landmark[3].y):
                            fingerCount += 1

                for x in range(0, 4):
                    if(hand_landmarks.landmark[8 + (4*x)].x > hand_landmarks.landmark[7 + (4*x)].x):
                        fingerCount += 1
                print("left")

            elif(is_right):
                if(handedness.classification[0].label == "Right"):
                    if(hand_landmarks.landmark[4].y > hand_landmarks.landmark[3].y):
                            fingerCount += 1

                if(handedness.classification[0].label == "Left"):
                    if(hand_landmarks.landmark[4].y < hand_landmarks.landmark[3].y):
                            fingerCount += 1

                for x in range(0, 4):
                    if(hand_landmarks.landmark[8 + (4*x)].x < hand_landmarks.landmark[7 + (4*x)].x):
                        fingerCount += 1
                print("right")

            for i in range(0,5):
                x0, y0 = hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y
                x_prev, y_prev = hand_landmarks.landmark[4 + (4*i)].x, hand_landmarks.landmark[4 + (4*i)].y
                x_curr, y_curr = hand_landmarks.landmark[3 + (4*i)].x, hand_landmarks.landmark[3 + (4*i)].y

                if (x_prev < x_curr < x0 or x0 < x_curr < x_prev) and (y_prev < y_curr < y0 or y0 < y_curr < y_prev):
                    fingers += 1
                
    cv2.putText(frame, f"Pocet prstu:", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, f"Podle pozice: {fingerCount}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, f"Podle mezi body: {fingers}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
    cv2.imshow('Hand Tracking', frame)

    # Ukončit program stisknutím klávesy 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
