import cv2
import time
import webbrowser
import pyautogui as pg

from aiconclave.trackers.PoseModule import PoseDetector
from aiconclave.trackers.HandTrackingModule import HandDetector
from aiconclave.constants import RR_LEFT_THRESHOLD, RR_RIGHT_THRESHOLD, RR_X_THRESHOLD, RR_GAME_URL, RR_WRIST_THRESHOLD

pg.FAILSAFE = False

def open_game_tab():
    webbrowser.open(RR_GAME_URL, new=2)

def put_text(img, text, position):
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

def main():
    open_game_tab()
    
    time.sleep(3)
    
    pg.keyDown('x')
    pg.keyDown('up')
    
    global count, hand_near_face, up_key_pressed

    cap = cv2.VideoCapture(0)

    hand_detector = HandDetector(detectionCon=0.7, maxHands=1)
    pose_detector = PoseDetector(staticMode=False,
                                modelComplexity=1,
                                smoothLandmarks=True,
                                enableSegmentation=False,
                                smoothSegmentation=True,
                                detectionCon=0.5,
                                trackCon=0.5)

    left_key_pressed = False
    right_key_pressed = False
    x_key_pressed = False
    c_key_pressed = False

    while True:
        try:
            _, raw_img = cap.read()

            hands, _ = hand_detector.findHands(raw_img)
            img = pose_detector.findPose(raw_img)
            lmList, _ = pose_detector.findPosition(img, draw=True, bboxWithHands=True)

            # put_text(img, f"Left Key: {'Pressed' if left_key_pressed else 'Released'}", (img.shape[1]-300, 90))
            # put_text(img, f"Right Key: {'Pressed' if right_key_pressed else 'Released'}", (img.shape[1]-300, 130))

            if len(lmList) >= 16 and hands:
                fingers = hand_detector.fingersUp(hands[0])
                
                right_elbow_coords = lmList[11][:2]
                right_wrist_coords = lmList[15][:2]

                left_elbow_coords = lmList[12][:2]
                left_wrist_coords = lmList[16][:2]
                
                left_distance, _, _ = pose_detector.findDistance(left_elbow_coords, left_wrist_coords, img=img, color=(0, 0, 255), scale=5)
                right_distance, _, _ = pose_detector.findDistance(right_elbow_coords, right_wrist_coords, img=img, color=(0, 0, 255), scale=5)                
                
                put_text(img, f"Distance (L,R): {left_distance, right_distance}\nThresh (L,R): {RR_LEFT_THRESHOLD, RR_RIGHT_THRESHOLD}", 
                         (img.shape[1]-350, 90))
                
                # if left_distance < RR_X_THRESHOLD and right_distance < RR_X_THRESHOLD and not x_key_pressed:
                if left_distance < RR_X_THRESHOLD and right_distance < RR_X_THRESHOLD:
                    pg.keyDown('x')
                    # x_key_pressed = True

                # elif left_distance >= RR_X_THRESHOLD and right_distance >= RR_X_THRESHOLD and x_key_pressed:
                #     pg.keyUp('x')
                #     x_key_pressed = False
                    
                if left_distance < RR_LEFT_THRESHOLD and not left_key_pressed:
                    pg.keyDown('left')
                    left_key_pressed = True
                    
                    if sum(fingers)>4 and not c_key_pressed:
                        pg.keyDown('c')
                        c_key_pressed = True
                        
                    elif not sum(fingers)>4 and c_key_pressed:
                        pg.keyUp('c')
                        c_key_pressed = False

                elif left_distance >= RR_LEFT_THRESHOLD and left_key_pressed:
                    pg.keyUp('left')
                    left_key_pressed = False

                if right_distance < RR_RIGHT_THRESHOLD and not right_key_pressed:
                    pg.keyDown('right')
                    right_key_pressed = True
                    
                    if sum(fingers)>4 and not c_key_pressed:
                        pg.keyDown('c')
                        c_key_pressed = True
                        
                    elif not sum(fingers)>4 and c_key_pressed:
                        pg.keyUp('c')
                        c_key_pressed = False

                elif right_distance >= RR_RIGHT_THRESHOLD and right_key_pressed:
                    pg.keyUp('right')
                    right_key_pressed = False

                
        except Exception as e:
            print(e)
            cv2.destroyAllWindows()
            cap.release()
            break
                
        cv2.namedWindow("Videocam Output", cv2.WINDOW_NORMAL)
        cv2.imshow("Videocam Output", img)
        
        if cv2.waitKey(5) & 0xFF == 27:
            cv2.destroyAllWindows()
            cap.release()
            break


if __name__ == "__main__":
    main()