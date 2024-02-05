import cv2
import numpy as np
import pyautogui
import imutils
import webbrowser


def open_website():
    webbrowser.open('https://www.onemotion.com/chord-player/')
    
def Press(key):
    pyautogui.press(key)

def draw_circle(frame, center, radius, label, color):
    cv2.circle(frame, center, radius, color, -1)
    cv2.putText(frame, label, (center[0] - 30, center[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

def main():
    open_website()
    
    cap = cv2.VideoCapture(0)

    while True:
        try:
            _, frame = cap.read()
            frame = cv2.flip(frame,1)
            frame = imutils.resize(frame,height=700, width=900)

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            lowred = np.array([131,90,106])
            highred = np.array([255,255,255])

            lowblue = np.array([40,150,116])
            highblue = np.array([255,255,255])

            red_mask = cv2.inRange(hsv, lowred, highred)
            blue_mask = cv2.inRange(hsv, lowblue, highblue)

            # Drum UI
            draw_circle(frame, (100, 100), 50, 'RIDE', (255, 0, 0))
            draw_circle(frame, (320, 100), 50, 'RIDE BELL', (0, 0, 255))
            draw_circle(frame, (550, 100), 50, 'HITHAT close', (255, 0, 0))
            draw_circle(frame, (780, 100), 50, 'CRASH', (0, 0, 255))

            draw_circle(frame, (100, 320), 50, 'SNARE', (255, 0, 0))
            draw_circle(frame, (100, 540), 50, 'SNARE RIM', (0, 0, 255))

            draw_circle(frame, (820, 320), 50, 'HIT HAT', (255, 0, 0))
            draw_circle(frame, (820, 540), 50, 'HIT HAT OPEN', (0, 0, 255))

            draw_circle(frame, (100, 660), 50, 'TOM HI', (255, 0, 0))
            draw_circle(frame, (320, 660), 50, 'TOM MID', (0, 0, 255))
            draw_circle(frame, (550, 660), 50, 'TOM LOW', (255, 0, 0))
            draw_circle(frame, (780, 660), 50, 'KICK', (0, 0, 255))

            # Red Object Detection
            contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
            for cnt in contours:
                x,y,w,h = cv2.boundingRect(cnt)
                if 0 < x < 200 and 0 < y < 150:
                    Press('7') # RIDE
                elif 210 < x < 430 and 0 < y < 150:
                    Press('8') # RIDE BELL
                elif 440 < x < 650 and 0 < y < 150:
                    Press('6') # HIT HAT CLOSE
                elif 660 < x < 900 and 0 < y < 150:
                    Press('9') # CRASH
                elif 0 < x < 50 and 160 < y < 370:
                    Press('2') # SNARE
                elif 0 < x < 50 and 380 < y < 570:
                    Press('3') # SNARE RIM
                elif 850 < x < 900 and 160 < y < 370:
                    Press('4') # HIT HAT
                elif 850 < x < 900 and 380 < y < 570:
                    Press('5') # HIT HAT OPEN
                elif 0 < x < 200 and 580 < y < 700:
                    Press('q') # TOM HI
                elif 210 < x < 430 and 580 < y < 700:
                    Press('w') # TOM MID
                elif 440 < x < 650 and 580 < y < 700:
                    Press('e') # TOM LOW
                elif 660 < x < 900 and 580 < y < 700:
                    Press('1') # KICK
                break

            # Blue Object Detection
            contours, _ = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
            for cnt in contours:
                x,y,w,h = cv2.boundingRect(cnt)
                if 0 < x < 200 and 0 < y < 150:
                    Press('7') # RIDE
                elif 210 < x < 430 and 0 < y < 150:
                    Press('8') # RIDE BELL
                elif 440 < x < 650 and 0 < y < 150:
                    Press('6') # HIT HAT CLOSE
                elif 660 < x < 900 and 0 < y < 150:
                    Press('9') # CRASH
                elif 0 < x < 50 and 160 < y < 370:
                    Press('2') # SNARE
                elif 0 < x < 50 and 380 < y < 570:
                    Press('3') # SNARE RIM
                elif 850 < x < 900 and 160 < y < 370:
                    Press('4') # HIT HAT
                elif 850 < x < 900 and 380 < y < 570:
                    Press('5') # HIT HAT OPEN
                elif 0 < x < 200 and 580 < y < 700:
                    Press('q') # TOM HI
                elif 210 < x < 430 and 580 < y < 700:
                    Press('w') # TOM MID
                elif 440 < x < 650 and 580 < y < 700:
                    Press('e') # TOM LOW
                elif 660 < x < 900 and 580 < y < 700:
                    Press('1') # KICK
                break
            
        except Exception as e:
            print(e)
            cv2.destroyAllWindows()
            cap.release()
            break
        
        # cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
        cv2.imshow("frame", frame)
        
        if cv2.waitKey(5) & 0xFF == 27:
            cv2.destroyAllWindows()
            cap.release()
            break

    cap.release()
    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    main()