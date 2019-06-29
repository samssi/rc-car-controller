import cv2

stream = cv2.VideoCapture('http://192.168.1.127:8000/stream.mjpg')


def start():
    while True:
        grabbed, frame = stream.read()
        if grabbed:
            cv2.imshow("frame", frame)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.waitKey(0)
    cv2.destroyAllWindows()


start()
