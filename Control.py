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
    lmList = detector.findPosition(image)

    if (len(lmList) != 0):
        xcord_right_11 = lmList[11][1]
        xcord_left_12 = lmList[12][1]

        ycord_right_11 = lmList[11][2]
        ycord_right_19 = lmList[19][2]
        ycord_right_12 = lmList[12][2]
        ycord_right_20 = lmList[20][2]


        if xcord_left_12 > width // 2:
            pydirectinput.keyDown('left')
        elif xcord_right_11 < width // 2 :
            pydirectinput.keyDown('right')
        else:
            pydirectinput.keyUp('left')
            pydirectinput.keyUp('right')

        if ycord_right_12 >= ycord_right_20:
            pydirectinput.press('up')

        if ycord_right_11 >= ycord_right_19:
            move_and_click(1250, 420)



def main():
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()

        img = detector.findPose(img)
        control_game(img)

        # Display the webcam feed
        # cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
