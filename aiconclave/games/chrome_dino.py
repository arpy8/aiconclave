import cv2
import pygame
import webbrowser
import pyautogui as pg

from aiconclave.trackers.PoseModule import PoseDetector
from aiconclave.constants import CD_UP_THRESHOLD, CD_GAME_URL


def put_text(img, text, position):
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

def play_sound():
    pygame.mixer.init()
    pygame.mixer.music.load('assets/chrome_dino/jump.mp3')
    pygame.mixer.music.play()

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

    webbrowser.open(CD_GAME_URL, new=2)

    jump_triggered = False

    while True:
        try:
            _, raw_img = cap.read()

            img = pose_detector.findPose(raw_img)
            lmList, _ = pose_detector.findPosition(img, draw=True, bboxWithHands=True)
        
            if len(lmList) >= 16:
                
                nose_coords = lmList[0][:2]
                
                specific_point = (350, 350)
                distance_from_nose, _, _ = pose_detector.findDistance(nose_coords, specific_point, img=img, color=(0, 0, 255), scale=5)

                if distance_from_nose > CD_UP_THRESHOLD and not jump_triggered:
                    pg.keyDown('up')
                    play_sound()
                    jump_triggered = True

                if not distance_from_nose > CD_UP_THRESHOLD and jump_triggered:
                    pg.keyUp('up')
                    jump_triggered = False
            
                put_text(img, f"Distance: {round(distance_from_nose, 2)}", (350, 80))
                put_text(img, f"Thresh: {CD_UP_THRESHOLD}", (350, 40))
                
                # if distance_from_nose < DOWN_THRESHOLD and not jump_triggered:
                #     pg.keyDown('down')
                #     play_sound()
                #     jump_triggered = True

                # if not distance_from_nose < DOWN_THRESHOLD and jump_triggered:
                #     pg.keyUp('down')
                #     jump_triggered = False
            
        except Exception as e:
            print(e)
            cv2.destroyAllWindows()
            cap.release()
            break

        cv2.namedWindow("Videocam Output", cv2.WINDOW_NORMAL)
        cv2.imshow("Videocam Output", raw_img)

        if cv2.waitKey(5) & 0xFF == 27:
            cv2.destroyAllWindows()
            cap.release()
            break

if __name__ == "__main__":
    main()