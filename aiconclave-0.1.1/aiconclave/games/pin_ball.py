import cv2
import time
import webbrowser
import pyautogui as pg
import pydirectinput as pg2

from aiconclave.trackers.PoseModule import PoseDetector
from aiconclave.constants import PB_LEFT_THRESHOLD, PB_RIGHT_THRESHOLD, PB_GAME_URL


def open_game_tab():
    webbrowser.open(PB_GAME_URL, new=2)

def put_text(img, text, position):
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

def launch_ball():
    print("launching the ball")
    pg2.keyDown('down')
    time.sleep(1.25)
    pg2.keyUp('down')

def main():
    global count, hand_near_face, up_key_pressed

    pg2.keyDown('down')
    cap = cv2.VideoCapture(0)

    pose_detector = PoseDetector(staticMode=False,
                                modelComplexity=1,
                                smoothLandmarks=True,
                                enableSegmentation=False,
                                smoothSegmentation=True,
                                detectionCon=0.5,
                                trackCon=0.5)

    open_game_tab()

    left_key_pressed = False
    right_key_pressed = False

    while True:
        try:
            _, raw_img = cap.read()

            img = pose_detector.findPose(raw_img)
            lmList, _ = pose_detector.findPosition(img, draw=True, bboxWithHands=True)

            if len(lmList) >= 16:
                
                left_shoulder_coords = lmList[11][:2]
                left_elbow_coords = lmList[13][:2]
                left_wrist_coords = lmList[15][:2]
                
                right_shoulder_coords = lmList[12][:2]
                right_elbow_coords = lmList[14][:2]
                right_wrist_coords = lmList[16][:2]

                left_angle, _ = pose_detector.findAngle(left_shoulder_coords, left_elbow_coords, left_wrist_coords, img=img, color=(0, 0, 255), scale=5)
                right_angle, _ = pose_detector.findAngle(right_wrist_coords, right_elbow_coords, right_shoulder_coords, img=img, color=(0, 0, 255), scale=5)                

                put_text(img, f"Thresh (L=R): <{PB_LEFT_THRESHOLD}", (img.shape[1]-360, 50))
                put_text(img, f"Left Angle: {round(left_angle, 2)}", (img.shape[1]-360, 90))
                put_text(img, f"Right Angle: {round(right_angle, 2)}", (img.shape[1]-360, 130))
                
                if left_angle < PB_LEFT_THRESHOLD and right_angle < PB_RIGHT_THRESHOLD:
                    launch_ball()
                    
                if left_angle < PB_LEFT_THRESHOLD and not left_key_pressed:
                    pg.keyDown('left')
                    left_key_pressed = True

                elif left_angle >= PB_LEFT_THRESHOLD and left_key_pressed:
                    pg.keyUp('left')
                    left_key_pressed = False

                if right_angle < PB_RIGHT_THRESHOLD and not right_key_pressed:
                    pg.keyDown('right')
                    right_key_pressed = True

                elif right_angle >= PB_RIGHT_THRESHOLD and right_key_pressed:
                    pg.keyUp('right')
                    right_key_pressed = False

        except Exception as e:
            print(e)
            cv2.destroyAllWindows()
            cap.release()
            break

        cv2.namedWindow("Videocam Output", cv2.WINDOW_NORMAL)
        cv2.imshow("Videocam Output", raw_img)
        
        if cv2.waitKey(5) & 0xFF == 27:
            pg2.keyUp('down')
            cv2.destroyAllWindows()
            cap.release()
            break

if __name__ == "__main__":
    main()