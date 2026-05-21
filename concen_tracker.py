import cv2
import mediapipe as mp
import numpy as np
import time
from collections import deque
import ui
import theme



mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

score_history = deque(maxlen=100)
distraction = 0
calibrated = False

baseline_nose_x = None
baseline_nose_y = None

baseline_gaze = None

stable_focus_score = 0

focus_confidence = 0
gaze_points = deque(maxlen=200)
fatigue_score = 0

blink_history = deque(maxlen=300)

fatigue_warning = False

def eye_aspect_ratio(landmarks, eye_points, image_w, image_h):
    p = []
    for idx in eye_points:
        lm = landmarks[idx]
        x, y = int(lm.x * image_w), int(lm.y * image_h)
        cv2.circle(frame, (x, y), 2, (0, 255, 0), -1) 
        p.append((x, y))

    A = np.linalg.norm(np.array(p[1]) - np.array(p[5]))
    B = np.linalg.norm(np.array(p[2]) - np.array(p[4]))
    C = np.linalg.norm(np.array(p[0]) - np.array(p[3]))
    ear = (A + B) / (2.0 * C)
    return ear

def is_blinking(ear, threshold=0.2):
    return ear < threshold

def get_head_pose_score(landmarks, image_w, image_h,baseline_x,baseline_y):
   
    nose = landmarks[1]

    dx = abs(nose.x - baseline_x)
    dy = abs(nose.y - baseline_y)

    distance = np.sqrt(dx**2 + dy**2)

    if distance < 0.08:
     return 1.0

    elif distance < 0.15:
     return 0.7
    elif distance < 0.22:
        return 0.4

    return 0.0

    

def get_gaze_score(
    landmarks,
    baseline_gaze
):

    left_iris = landmarks[468]
    right_iris = landmarks[473]

    avg_x = (
        left_iris.x + right_iris.x
    ) / 2.0

    deviation = abs(avg_x - baseline_gaze)

    if deviation < 0.05:
        return 1.0

    elif deviation < 0.1:
        return 0.7
    elif deviation < 0.15:
        return 0.4

    return 0.0

def compute_concentration_score(gaze, head_pose, blink):
    score = 0.4 * gaze + 0.4 * head_pose + 0.2 * (0 if blink else 1)
    return round(score * 100, 2)

def bar(score, frame):
    """Enhanced visual bar for concentration level"""
    bar_width = 200
    bar_height = 30
    bar_x = 30
    bar_y = 100
    
    cv2.rectangle(frame, (bar_x, bar_y), 
                 (bar_x + bar_width, bar_y + bar_height), 
                 (50, 50, 50), -1)
    
    fill_width = int(score * bar_width / 100)
    color = (0, 255, 0) if score > 40 else (0, 100, 255)
    cv2.rectangle(frame, (bar_x, bar_y), 
                 (bar_x + fill_width, bar_y + bar_height), 
                 color, -1)
 
    cv2.rectangle(frame, (bar_x, bar_y), 
                 (bar_x + bar_width, bar_y + bar_height), 
                 (200, 200, 200), 2)
    
    cv2.putText(frame, f"{score}%", 
               (bar_x + bar_width + 10, bar_y + bar_height//2 + 5),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)

cap = cv2.VideoCapture(0)
blink_counter = 0
session_start = time.time()
calibration_start = time.time()
focus_scores = []

distraction_count = 0
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

cv2.namedWindow("Concentration Tracker", cv2.WINDOW_NORMAL)

cv2.resizeWindow(
    "Concentration Tracker",
    WINDOW_WIDTH,
    WINDOW_HEIGHT
)
smooth_score = 0
blink = False
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (900, 600))
    frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=25)
    # canvas = np.zeros((800, 1300, 3), dtype=np.uint8)
    canvas = np.full((900, 1400, 3), (15, 15, 18), dtype=np.uint8)
    cv2.rectangle(
    canvas,
    (330, 70),
    (1250, 690),
    ui.get_focus_color(smooth_score),
    3
)
   
    if not ret:
        break
    
   

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_h, image_w, _ = frame.shape
    fps = cap.get(cv2.CAP_PROP_FPS)
    session_time = int(time.time() - session_start)

    minutes = session_time // 60
    seconds = session_time % 60

    avg_focus = int(np.mean(focus_scores)) if focus_scores else 0
    results = face_mesh.process(frame_rgb)
    

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
 
            mp_drawing.draw_landmarks(
                frame, 
                face_landmarks, 
                mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 200, 0), thickness=1, circle_radius=1),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 150, 255), thickness=1)
            )

            landmarks = face_landmarks.landmark
            if not calibrated:

                elapsed = time.time() - calibration_start

                cv2.putText(
                    canvas,
                    "Calibrating Vision System...",
                    (350, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 255),
                    2
                )
                remaining = 3 - int(elapsed)

                cv2.putText(
                    canvas,
                    f"Starting in {remaining}...",
                    (500, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (180, 180, 180),
                    2
                )

                if elapsed > 3:

                    nose = landmarks[1]

                    baseline_nose_x = nose.x
                    baseline_nose_y = nose.y

                    left_iris = landmarks[468]
                    right_iris = landmarks[473]

                    baseline_gaze = (
                        left_iris.x + right_iris.x
                    ) / 2.0

                    calibrated = True
                    print("Calibration Complete")
            left_ear = eye_aspect_ratio(landmarks, LEFT_EYE, image_w, image_h)
            right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE, image_w, image_h)
            avg_ear = (left_ear + right_ear) / 2

            blink = is_blinking(avg_ear)
            blink_history.append(1 if blink else 0)
            if calibrated:
                gaze_score = get_gaze_score(landmarks,baseline_gaze)
                left_iris = landmarks[468]
                right_iris = landmarks[473]

                gaze_x = int(
                    ((left_iris.x + right_iris.x) / 2.0) * 900
                )

                gaze_y = int(
                     ((left_iris.y + right_iris.y) / 2.0) * 700
                    )

                gaze_points.append((gaze_x, gaze_y))
                head_score = get_head_pose_score(landmarks, image_w, image_h,baseline_nose_x,baseline_nose_y)
                concentration = compute_concentration_score(gaze_score, head_score, blink)

                score_history.append(concentration)
                focus_scores.append(concentration)
                raw_score = int(np.mean(score_history))

                stable_focus_score = int(
    0.85 * stable_focus_score +
    0.15 * raw_score
)

                smooth_score = stable_focus_score
                if smooth_score >= 65:
                    focus_confidence = min(100, focus_confidence + 3)

                else:
                    focus_confidence = max(0, focus_confidence -2)
                recent_blinks = sum(blink_history)

                if smooth_score < 45:
                    fatigue_score += 0.4

                if recent_blinks > 35:
                    fatigue_score += 0.3

                if focus_confidence < 20:
                    fatigue_score += 0.2

                fatigue_score = min(100, fatigue_score)
                fatigue_score = max(0, fatigue_score - 0.05)

                fatigue_warning = fatigue_score > 60
                if smooth_score < 40 and focus_confidence < 5:
                    distraction_count += 1
                ui.draw_side_panel(canvas)
                ui.draw_title(canvas)

                ui.draw_card(
                canvas,
                "Focus Score",
                f"{smooth_score}%",
                110,
                  ui.get_focus_color(smooth_score)
            )

                ui.draw_card(
                canvas,
                "Status",
                ui.get_focus_state(smooth_score),
                220,
                ui.get_focus_color(smooth_score)
            )

                ui.draw_card(
                canvas,
                "Blink",
                "Yes" if blink else "No",
                330,
                (0, 140, 255) if blink else (0, 255, 120)
            )
                
                ui.draw_card(
                    canvas,
                    "Confidence",
                    f"{focus_confidence}%",
                    440,
                    ui.get_focus_color(smooth_score)
                )
                ui.draw_card(
                    canvas,
                     "Fatigue",
                    ui.get_fatigue_state(fatigue_score),
                    550,
                    (0, 255, 120) if fatigue_score < 50 else (0, 140, 255)
                )
                ui.draw_graph(
                canvas,
                list(score_history),
                340,
                720,
                500,
                 120
                )
                ui.draw_focus_ring(
                canvas,
                smooth_score,
                (1080, 790),
                60
            )
                
                # Bottom status indicator

                status_x = 1180
                status_y = 790

                cv2.putText(
                    canvas,
                    ui.get_focus_state(smooth_score).upper(),
                    (status_x, status_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    theme.TEXT,
                    2
                )

                pulse_radius = ui.get_pulse_radius()

                cv2.circle(
    canvas,
    (status_x + 170, status_y - 10),
    pulse_radius,
    status_color,
    -1
)
                ui.draw_session_stats(
                canvas,
                avg_focus,
                distraction_count,
                minutes,
                seconds
            )
                
                if fatigue_warning:

                    cv2.rectangle(
                    canvas,
        (340, 15),
        (1050, 50),
        (0, 80, 255),
        -1
    )

                    cv2.putText(
                        canvas,
                        "Fatigue Detected — Consider Taking a Break",
                            (380, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 255, 255),
                        2
    )
            
           
    
    
    cv2.putText(
    canvas,
    f"FPS: {fps:.1f}",
    (1120, 45),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 255),
    2
)
    
    
    status_color = (0, 255, 100) if smooth_score > 40 else (0, 100, 255)

    
    ui.draw_attention_heatmap(
    frame,
    gaze_points,
    0,
    0
)
    canvas[80:680, 340:1240] = frame

    cv2.imshow("Concentration Tracker", canvas)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()