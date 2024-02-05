import cv2
import time
import random
import pkg_resources
import subprocess as sb
import pydirectinput as pg

from aiconclave.games.tekken_players import PaulPhoenix
from aiconclave.trackers.PoseModule import PoseDetector
from aiconclave.constants import TK_FRONT_POINT_COORDS, TK_REAR_POINT_COORDS, TK_THRESH, TK_RPUNCH_ANGLE_LTHRESH, TK_RPUNCH_ANGLE_UTHRESH, TK_LPUNCH_ANGLE_LTHRESH, TK_LPUNCH_ANGLE_UTHRESH, TK_RANDOM_UPPER, TK_RANDOM_LOWER

count = 0

key_pressed = False
run_key_pressed = False

keys = ["a", "s", "z", "x"]
color_keys = ["green", "red", "blue", "pink"]

def launch_game():
    teken_path = pkg_resources.resource_filename(__name__, '../assets/tekken/TekkenGame.exe')
    sb.Popen(teken_path)
    return None

def put_text(img, text, position):
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
    
def check_angle(pose_detector, point1, point2, point3, img, lower_thresh, upper_thresh):
    angle, _ = pose_detector.findAngle(point1, point2, point3, img=img)
    return lower_thresh <= angle <= upper_thresh, angle    

def main():
    launch_game()
    
    global count, run_key_pressed, key_pressed

    paul = PaulPhoenix()
    cap = cv2.VideoCapture(0)
    pose_detector = PoseDetector(staticMode=False,
                                modelComplexity=1,
                                smoothLandmarks=True,
                                enableSegmentation=False,
                                smoothSegmentation=True,
                                detectionCon=0.5,
                                trackCon=0.5)

    while True:
        try:
            _, raw_img = cap.read()
        
            img = pose_detector.findPose(raw_img)
            lmList, _ = pose_detector.findPosition(img, draw=True, bboxWithHands=True)
            if len(lmList) >= 16:
                
                right_elbow_coords = lmList[14][:2]
                right_shoulder_coords = lmList[12][:2]
                right_hip_coords = lmList[24][:2]

                nose_coords = lmList[0][:2]
                left_shoulder_coords = lmList[11][:2]
                left_elbow_coords = lmList[13][:2]

                DISTANCE_FROM_FRONT_POINT, _, _ = pose_detector.findDistance(nose_coords, TK_FRONT_POINT_COORDS, img=img, color=(0, 0, 255), scale=5)
                DISTANCE_FROM_REAR_POINT, _, _ = pose_detector.findDistance(nose_coords, TK_REAR_POINT_COORDS, img=img, color=(0, 0, 255), scale=5)

                if DISTANCE_FROM_FRONT_POINT < TK_THRESH and not run_key_pressed:
                    run_key_pressed = True
                    for _ in range(2):
                        pg.keyDown("right")
                        time.sleep(0.2)
                        pg.keyUp("right")
                if not DISTANCE_FROM_FRONT_POINT < TK_THRESH and run_key_pressed:
                    run_key_pressed = False
                    
                if DISTANCE_FROM_REAR_POINT < TK_THRESH and not run_key_pressed:
                    run_key_pressed = True
                    for _ in range(2):
                        pg.keyDown("left")
                        time.sleep(0.2)
                        pg.keyUp("left")
                if not DISTANCE_FROM_REAR_POINT < TK_THRESH and run_key_pressed:
                    run_key_pressed = False
                    
                is_r_punch, _ = check_angle(pose_detector, right_elbow_coords, right_shoulder_coords, right_hip_coords, 
                                        img, TK_RPUNCH_ANGLE_LTHRESH, TK_RPUNCH_ANGLE_UTHRESH)
                is_l_punch, _ = check_angle(pose_detector, nose_coords, left_shoulder_coords, left_elbow_coords,  
                                        img, TK_LPUNCH_ANGLE_LTHRESH, TK_LPUNCH_ANGLE_UTHRESH)

                is_punch = is_r_punch or is_l_punch
                
                if is_punch and not key_pressed:
                    count += 1
                    key_pressed = True
                    rand_num = random.randint(TK_RANDOM_LOWER, TK_RANDOM_UPPER)

                    if count%rand_num == 0:
                        random.choice([paul.perform_combo_hit(), paul.burning_fist()]) 
                    else:
                        rand_key1 = random.choice(color_keys)
                        rand_key2 = random.choice(color_keys)
                        paul.press_key(0.2, [rand_key1, rand_key2])
                    
                if not is_punch and key_pressed:
                    key_pressed = False
                
        except Exception as e:
            print(e)
            cv2.destroyAllWindows()
            cap.release()
            break
        
        cv2.circle(img, TK_FRONT_POINT_COORDS, TK_THRESH, (255, 0, 0), -1)
        cv2.circle(img, TK_REAR_POINT_COORDS, TK_THRESH, (255, 0, 0), -1)

        cv2.namedWindow("Videocam Output", cv2.WINDOW_NORMAL)
        cv2.imshow("Videocam Output", raw_img)
        
        if cv2.waitKey(5) & 0xFF == 27:
            cv2.destroyAllWindows()
            cap.release()
            break


if __name__ == "__main__":
    main()