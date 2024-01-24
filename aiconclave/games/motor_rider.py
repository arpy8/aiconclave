import cv2
import pyautogui as pg
from aiconclave.trackers.PoseModule import PoseDetector
from aiconclave.constants import MR_LEFT_THRESHOLD, MR_RIGHT_THRESHOLD, MR_DOWN_THRESHOLD


def put_text(img, text, position):
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

def main():
    global count, hand_near_face, up_key_pressed

    cap = cv2.VideoCapture(0)

    pose_detector = PoseDetector(staticMode=False,
                                modelComplexity=1,
                                smoothLandmarks=True,
                                enableSegmentation=False,
                                smoothSegmentation=True,
                                detectionCon=0.5,
                                trackCon=0.5)

    left_key_pressed = False
    right_key_pressed = False
    down_key_pressed = False

    while True:
        try:
            _, raw_img = cap.read()

            img = pose_detector.findPose(raw_img)
            lmList, _ = pose_detector.findPosition(img, draw=True, bboxWithHands=True)

            if len(lmList) >= 16:
                
                right_elbow_coords = lmList[11][:2]
                right_wrist_coords = lmList[15][:2]

                left_elbow_coords = lmList[12][:2]
                left_wrist_coords = lmList[16][:2]
                
                left_distance, _, _ = pose_detector.findDistance(left_elbow_coords, left_wrist_coords, img=img, color=(0, 0, 255), scale=5)
                right_distance, _, _ = pose_detector.findDistance(right_elbow_coords, right_wrist_coords, img=img, color=(0, 0, 255), scale=5)                

                put_text(img, f"(L, R) : {round(left_distance, 2), round(right_distance, 2)}", (img.shape[1]-450, 80))
                put_text(img, f"Thresh (L, R) : {MR_LEFT_THRESHOLD, MR_RIGHT_THRESHOLD}", (img.shape[1]-450,130))

                if left_distance < MR_LEFT_THRESHOLD and not left_key_pressed:
                    pg.keyDown('left')
                    left_key_pressed = True

                elif left_distance >= MR_LEFT_THRESHOLD and left_key_pressed:
                    pg.keyUp('left')
                    left_key_pressed = False

                if right_distance < MR_RIGHT_THRESHOLD and not right_key_pressed:
                    pg.keyDown('right')
                    right_key_pressed = True

                elif right_distance >= MR_RIGHT_THRESHOLD and right_key_pressed:
                    pg.keyUp('right')
                    right_key_pressed = False

                if left_distance < MR_DOWN_THRESHOLD and right_distance < MR_DOWN_THRESHOLD and not down_key_pressed:
                    pg.keyDown('down')
                    down_key_pressed = True

                elif left_distance >= MR_DOWN_THRESHOLD and right_distance >= MR_DOWN_THRESHOLD and down_key_pressed:
                    pg.keyUp('down')
                    down_key_pressed = False

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