import mediapipe as mp
import pyautogui
import cv2

def hand_gesture():
    cap = cv2.VideoCapture(1)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(static_image_mode=False,
                          max_num_hands=1,
                          min_detection_confidence=0.5,
                          min_tracking_confidence=0.5)
    mpDraw = mp.solutions.drawing_utils
    pTime = 0
    cTime = 0
    # 视频窗口
    show = 1
    # 顶点
    dot = [120, 120, 550, 400]
    # 鼠标左键状态 0弹起，1按下
    mouse_left = 0
    # 双指捏合点击间距
    tero = 40
    # 鼠标右键状态
    mouse_right = 0
    # 鼠标左键双击状态
    mouse_double_click = 0
    # 坐标列表
    x0 = y0 = x1 = y1 = x2 = y2 = x3 = y3 = x4 = y4 = 0
    while True:
        success, img = cap.read()
        if success == True:
            new_video = cv2.flip(img, 180)
        if show == 1:# draw line
            cv2.line(new_video, (dot[0], dot[1]), (dot[2], dot[1]), (0, 255, 0), 2)
            cv2.line(new_video, (dot[0], dot[1]), (dot[0], dot[3]), (0, 255, 0), 2)
            cv2.line(new_video, (dot[0], dot[3]), (dot[2], dot[3]), (0, 255, 0), 2)
            cv2.line(new_video, (dot[2], dot[1]), (dot[2], dot[3]), (0, 255, 0), 2)
        imgRGB = cv2.cvtColor(new_video, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    # print(id,lm)
                    h, w, c = new_video.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)

                    if id == 0:
                        if cx > dot[0] and cx < dot[2] and cy > dot[1] and cy < dot[3]:
                            x0 = ((cx - dot[0]) / (dot[2] - dot[0])) * 1920
                            y0 = ((cy - dot[1]) / (dot[3] - dot[1])) * 1080
                            pyautogui.moveTo(x0, y0, duration=0.02) 
                    if id == 4:
                        x1 = ((cx - dot[0]) / (dot[2] - dot[0])) * 1920
                        y1 = ((cy - dot[1]) / (dot[3] - dot[1])) * 1080

                    if id == 8:
                        x2 = ((cx - dot[0]) / (dot[2] - dot[0])) * 1920
                        y2 = ((cy - dot[1]) / (dot[3] - dot[1])) * 1080

                    if id == 20:
                        x3 = ((cx - dot[0]) / (dot[2] - dot[0])) * 1920
                        y3 = ((cy - dot[1]) / (dot[3] - dot[1])) * 1080

                    if id == 12:
                        x4 = ((cx - dot[0]) / (dot[2] - dot[0])) * 1920
                        y4 = ((cy - dot[1]) / (dot[3] - dot[1])) * 1080
                    #! control
                    if abs(x1 - x2) <= tero and abs(y1 - y2) <= tero and mouse_left == 0:
                        pyautogui.mouseDown()
                        mouse_left = 1

                    if abs(x1 - x2) > tero and abs(y1 - y2) > tero and mouse_left == 1:
                        pyautogui.mouseUp()
                        mouse_left = 0

                    if abs(x1 - x3) <= tero and abs(y1 - y3) <= tero and mouse_right == 0:
                        pyautogui.rightClick()
                        mouse_right = 1

                    if abs(x1 - x3) > tero and abs(y1 - y3) > tero and mouse_right == 1:
                        mouse_right = 0

                    if abs(x1 - x4) <= tero and abs(y1 - y4) <= tero and mouse_double_click == 0:
                        pyautogui.doubleClick()
                        mouse_double_click = 1

                    if abs(x1 - x4) > tero and abs(y1 - y4) > tero and mouse_double_click == 1:
                        mouse_double_click = 0

                    if show == 1:
                        mpDraw.draw_landmarks(new_video, handLms, mpHands.HAND_CONNECTIONS)

        if show == 1:
            cv2.imshow("Test", new_video)
        cv2.waitKey(1)
        boardkey = cv2.waitKey(10) & 0xFF
        if boardkey == 27:
            break