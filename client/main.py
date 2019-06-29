import cv2

stream = cv2.VideoCapture('http://192.168.1.127:8000/stream.mjpg')
width_height = (960, 540)

def start():
    while True:
        grabbed, frame = stream.read()
        if grabbed:
            resized = cv2.resize(frame, width_height)
            cv2.imshow("frame", resized)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.waitKey(0)
    cv2.destroyAllWindows()


start()
