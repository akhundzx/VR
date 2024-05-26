import cv2
import mediapipe
import pyautogui

cam = cv2.VideoCapture(0)
width,height = pyautogui.size()
hands = mediapipe.solutions.hands.Hands(static_image_mode = False,
                                max_num_hands = 1,
                                min_tracking_confidence = 0.5,
                                min_detection_confidence = 0.5)

cx4,cy4,cx8,cy8,cx20,cy20 = 0,0,0,0,0,0
mpDraw = mediapipe.solutions.drawing_utils
while True:
    ret, img = cam.read()
    img = cv2.flip(img,1)
    result = hands.process(img)
    print(result)
    if result.multi_hand_landmarks:
        for id,lm in enumerate(result.multi_hand_landmarks[0].landmark):
            h,w,_ = img.shape
            cx,cy = int(lm.x*w),int(lm.y*h)
            cv2.circle(img,(cx,cy),5,(255,0,255))
            
            if id == 4:
                cx4,cy4 = cx,cy
                cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED)
            if id == 20:
                cx20,cy20 = cx,cy
                cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED)
            if id == 8:
                cx8,cy8 = cx,cy
                cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED)
                pyautogui.moveTo(cx*width/w,cy*height/h)
            if 0<abs(cx4-cx8)<50 and 0<abs(cy8-cy4)<50:
                pyautogui.click(clicks=1)
                cx4,cy4,cx8,cy8 = 0,0,0,0
            if 0<abs(cx4-cx20)<50 and 0<abs(cy20-cy4)<50:
                pyautogui.click(button = 'right',clicks=1)
                cx20,cy20,cx8,cy8 = 0,0,0,0

        mpDraw.draw_landmarks(img,result.multi_hand_landmarks[0],mediapipe.solutions.hands.HAND_CONNECTIONS)
    but = cv2.waitKey(30) & 0xFF
    if but == 27:
        break 
    cv2.imshow('From Camera',img)
    cv2.waitKey(1)
    
