import time

from PoseEstimationModule import poseDetector
import cv2
import pydirectinput

# Initialize the pose detector
detector = poseDetector()

def move_and_click(x, y):
    pydirectinput.moveTo(x, y)
    pydirectinput.click()

def control_game(image):
    height, width, _ = image.shape
    lmList = detector.findPosition(image,draw= False)

    if (len(lmList) != 0):
        xcord_right_11 = lmList[11][1]
        xcord_left_12 = lmList[12][1]

        ycord_right_11 = lmList[11][2]
        ycord_right_12 = lmList[12][2]

        ycord_right_9 = lmList[9][2]


        if xcord_left_12 > width // 2:
            pydirectinput.keyDown('left')
            pydirectinput.keyUp('right')
            print('left')
        elif xcord_right_11 < width // 2:
            pydirectinput.keyDown('right')
            pydirectinput.keyUp('left')
            print('right')
        else:
            pydirectinput.keyUp('left')
            pydirectinput.keyUp('right')


        if ycord_right_11 <= int(height // 2.5) or ycord_right_12 <= int(height // 2.5):
            # for more than one jump
            pydirectinput.keyDown('x')
            time.sleep(1)
            pydirectinput.keyUp('x')
            print('double jump')
        elif ycord_right_11 <= height // 2 or ycord_right_12 <= height // 2:
            pydirectinput.press('x')
            print('up')

        if ycord_right_9 >= height // 2:
            pydirectinput.keyDown('down')
            print('down')
        else:
            pydirectinput.keyUp('down')





def main():
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()

        lmList = detector.findPosition(img,draw=False)
        if len(lmList) != 0:
            cv2.circle(img, (lmList[11][1], lmList[11][2]), 5, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (lmList[12][1], lmList[12][2]), 5, (255, 0, 0), cv2.FILLED)

        height, width, _ = img.shape
        line_position = int(width / 2)
        cv2.line(img, (line_position, 0), (line_position, height), (0, 0, 0), thickness=2)

        cv2.line(img, (0, height//2), (width,height//2), (0, 0, 0), thickness=2)
        cv2.line(img, (0, int(height // 2.5)), (width, int(height // 2.5)), (0, 0, 0), thickness=2)

        control_game(img)

        img = cv2.flip(img, 1)

        # Display the webcam feed
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
