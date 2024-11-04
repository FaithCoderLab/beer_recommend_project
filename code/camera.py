import cv2

def camera_on():
    # 웹캠키기
    cap = cv2.VideoCapture(0)

    print("Press 'Space' to take a photo, 'q' to quit.")

    while True:
        # 화면 업데이트
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        #사용설명 보여주기
        display_frame = frame.copy()
        text = "space: take photo, q: exit"
        font = cv2.FONT_HERSHEY_SIMPLEX
        position = (50, 50)  # 왼쪽 아래의 (x, y) 좌표
        font_scale = 1  # 폰트 사이즈
        color = (0, 255, 0)  # RGB 색상 지정
        thickness = 2  # 폰트 두께

        # 텍스트 보여주기
        cv2.putText(display_frame, text, position, font, font_scale, color, thickness)

        # 이미지 + 텍스트 보여주기
        cv2.imshow("Webcam", display_frame)

        # 키입력 기다리기
        key = cv2.waitKey(1) & 0xFF

        if key == ord(' '):  # 스페이스로 캡쳐하기
            cv2.imwrite("images/captured_photo.jpg", frame)
            print("Photo saved as 'captured_photo.jpg'")
            break
        elif key == ord('q'):  # Press 'q' to quit
            break

    # 비디오 중지 및 창닫기
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    camera_on()