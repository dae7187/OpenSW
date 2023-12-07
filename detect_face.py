import cv2

def calculate_eye_distance(eyes, pixel_to_cm_ratio=0.0264583333):
    # pixel_to_cm_ratio: 픽셀과 센티미터 간의 변환 비율
    (ex1, ey1, ew1, eh1), (ex2, ey2, ew2, eh2) = eyes
    eye1_center = (ex1 + ew1 // 2, ey1 + eh1 // 2)
    eye2_center = (ex2 + ew2 // 2, ey2 + eh2 // 2)
    eye_distance_pixel = abs(eye2_center[0] - eye1_center[0])
    eye_distance_cm = eye_distance_pixel * pixel_to_cm_ratio
    return eye_distance_cm

def assess_beautiful_eyes(eye_distance_cm, threshold=3.5):
    if eye_distance_cm <= threshold:
        return "예쁜 눈을 가졌습니다!"
    else:
        return "눈 간의 거리가 평균보다 큽니다."

def detect_face_eyes_nose(image_path):
    # 이미지를 읽어옴
    image = cv2.imread(image_path)
    
    # 이미지를 그레이스케일로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 얼굴 감지기를 초기화
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # 얼굴 감지
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    
    # 눈 감지기를 초기화
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    
    # 얼굴 내에서 눈 감지
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        
        # 눈이 두 개 감지된 경우
        if len(eyes) == 2:
            eye_distance_cm = calculate_eye_distance(eyes)
            
            # 감지된 얼굴에 눈 사각형을 그림
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.rectangle(roi_gray, (eyes[0][0], eyes[0][1]), (eyes[0][0]+eyes[0][2], eyes[0][1]+eyes[0][3]), (0, 255, 0), 2)
            cv2.rectangle(roi_gray, (eyes[1][0], eyes[1][1]), (eyes[1][0]+eyes[1][2], eyes[1][1]+eyes[1][3]), (0, 255, 0), 2)
            
            # 눈과 눈 사이의 거리를 출력
            print(f"눈과 눈 사이의 거리: {eye_distance_cm:.2f} 센티미터")
            
            # 눈 간의 거리에 대한 평가 출력
            print(assess_beautiful_eyes(eye_distance_cm))
    
    # 결과 이미지를 화면에 표시
    cv2.imshow('Detected Face and Eyes', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 이미지 파일 경로를 지정하여 얼굴과 눈 감지 수행
image_path = 'path/to/your/image.jpg'  # 실제 이미지 파일 경로로 변경해야 합니다.
detect_face_eyes_nose(image_path)
