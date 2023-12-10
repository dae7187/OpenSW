import cv2

def mouse_callback(event, x, y, flags, param):
    global point1, point2, point3, point4, selecting, face_width_px, eye_distance_px

    if event == cv2.EVENT_LBUTTONDOWN:
        if selecting == 0:
            point1 = (x, y)
            selecting = 1
        elif selecting == 1:
            point2 = (x, y)
            selecting = 2
            # 얼굴의 너비 측정 및 출력 (단위: 픽셀)
            face_width_px = calculate_distance(point1, point2)
            print(f"얼굴의 너비를 측정했습니다. 값: {face_width_px} 픽셀")
        elif selecting == 2:
            point3 = (x, y)
            selecting = 3
        elif selecting == 3:
            point4 = (x, y)
            selecting = 0
            # 눈 사이의 거리 측정 및 출력 (단위: 픽셀)
            eye_distance_px = calculate_distance(point3, point4)
            print(f"눈과 눈 사이의 거리를 측정했습니다. 값: {eye_distance_px} 픽셀")
            # 얼굴과 눈 간의 비율 계산 및 출력
            print(f"얼굴과 눈 간의 비율: {face_width_px / eye_distance_px:.2f}")

def calculate_distance(point1, point2):
    return ((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)**0.5

def manual_measurements(image_path):
    global point1, point2, point3, point4, selecting, face_width_px, eye_distance_px

    point1, point2, point3, point4 = (-1, -1), (-1, -1), (-1, -1), (-1, -1)
    selecting = 0
    face_width_px, eye_distance_px = 0, 0

    image = cv2.imread(image_path)

    cv2.imshow('Measurements', image)
    cv2.setMouseCallback('Measurements', mouse_callback)

    while True:
        display_image = image.copy()

        if selecting == 1:
            cv2.rectangle(display_image, point1, (point2[0], point2[1]), (0, 255, 0), 2)
        elif selecting == 3:
            cv2.rectangle(display_image, point3, (point4[0], point4[1]), (0, 255, 0), 2)

        cv2.imshow('Measurements', display_image)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

    cv2.destroyAllWindows()

# 이미지 파일 경로를 지정하여 수동으로 측정
image_path = 'OIP.jpg'  # 실제 이미지 파일 경로로 변경해야 합니다.
manual_measurements(image_path)
