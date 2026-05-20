import cv2
import theme
import time
import numpy as np

def get_focus_color(score):

    if score >= 80:
        return (0, 255, 120)

    elif score >= 50:
        return (0, 220, 255)

    else:
        return (0, 80, 255)

def get_focus_state(score):

    if score >= 85:
        return "Deep Focus"

    elif score >= 65:
        return "Focused"

    elif score >= 40:
        return "Drifting"

    else:
        return "Distracted"  
    
def get_fatigue_state(score):

    if score < 25:
        return "Fresh"

    elif score < 50:
        return "Normal"

    elif score < 75:
        return "Tired"

    return "Fatigued"
def get_pulse_radius(base=15, amplitude=6, speed=3):

    t = time.time()

    pulse = int(
        base + amplitude * abs(np.sin(t * speed))
    )

    return pulse   


def draw_top_bar(frame):
    h, w, _ = frame.shape

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (0, 0),
        (w, 80),
        theme.PANEL,
        -1
    )

    cv2.addWeighted(
        overlay,
        0.7,
        frame,
        0.3,
        0,
        frame
    )


def draw_title(canvas):
    cv2.putText(
        canvas,
        "AI Focus Tracker",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        theme.TEXT,
        2
    )
    
    
    
PANEL_WIDTH = 300


def draw_side_panel(frame):
    h, w, _ = frame.shape

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (0, 0),
        (PANEL_WIDTH, h),
        theme.PANEL,
        -1
    )

    cv2.addWeighted(
        overlay,
        0.85,
        frame,
        0.08,
        0,
        frame
    )
    
def draw_rounded_rect(img, top_left, bottom_right, color, radius=20):

    x1, y1 = top_left
    x2, y2 = bottom_right

    # Center rectangles
    cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y2), color, -1)
    cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, -1)

    # Corners
    cv2.circle(img, (x1 + radius, y1 + radius), radius, color, -1)
    cv2.circle(img, (x2 - radius, y1 + radius), radius, color, -1)
    cv2.circle(img, (x1 + radius, y2 - radius), radius, color, -1)
    cv2.circle(img, (x2 - radius, y2 - radius), radius, color, -1) 
    

    
    
    
def draw_card(frame, title, value, y,color):
    x =15
    width = PANEL_WIDTH - 30
    height = 90

    # # Card background
    # cv2.rectangle(
    #     frame,
    #     (x, y),
    #     (x + width, y + height),
    #     (45, 45, 45),
    #     -1
    # )
    
    draw_rounded_rect(
    frame,
    (x, y),
    (x + width, y + height),
    (45, 45, 45),
    radius=18
)
    #  # Small accent line
    cv2.rectangle(
        frame,
        (x, y+10),
        (x + 5, y + height-10),
        color,
        -1
    )
    
    
    # Title
    cv2.putText(
        frame,
        title,
        (x + 18, y + 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        theme.MUTED,
        2
    )

    # Value
    cv2.putText(
        frame,
        str(value),
        (x + 18, y + 68),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        theme.TEXT,
        3
    )
    
    
def draw_graph(frame, data, x, y, width, height):

    # Background
    draw_rounded_rect(
        frame,
        (x, y),
        (x + width, y + height),
        (35, 35, 40),
        radius=15
    )

    # Title
    cv2.putText(
        frame,
        "Focus Trend",
        (x + 15, y + 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        theme.TEXT,
        1
    )

    if len(data) < 2:
        return

    max_value = 100

    graph_x = x + 20
    graph_y = y + 50

    graph_width = width - 40
    graph_height = height - 70

    points = []

    for i, value in enumerate(data):

        px = int(graph_x + (i / len(data)) * graph_width)

        py = int(
            graph_y + graph_height -
            (value / max_value) * graph_height
        )

        points.append((px, py))

    for i in range(1, len(points)):
        cv2.line(
            frame,
            points[i - 1],
            points[i],
            get_focus_color(data[i]),
            2
        )
        

def draw_focus_ring(frame, score, center, radius):
    focus_color = get_focus_color(score)
    x, y = center
    ring_thickness = get_pulse_radius(
    base=10,
    amplitude=3,
    speed=2
)

    # Background circle
    cv2.circle(
        frame,
        center,
        radius,
        (40, 40, 45),
        12
    )

    # Progress angle
    angle = int(360 * (score / 100))

    # Progress arc
    cv2.ellipse(
        frame,
        center,
        (radius, radius),
        -90,
        0,
        angle,
        focus_color,
        ring_thickness
    )

    # Inner circle
    cv2.circle(
        frame,
        center,
        radius - 18,
        (20, 20, 25),
        -1
    )

    # Score text
    cv2.putText(
        frame,
        f"{score}%",
        (x - 45, y + 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        theme.TEXT,
        2
    )

    # Label
    cv2.putText(
        frame,
        "FOCUS",
        (x - 35, y + 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        theme.MUTED,
        1
    )
    
def draw_attention_heatmap(
    frame,
    gaze_points,
    offset_x,
    offset_y
):

    heat = frame.copy()

    for point in gaze_points:

        cv2.circle(
            heat,
            (
                point[0] + offset_x,
                point[1] + offset_y
            ),
            25,
            (0, 80, 255),
            -1
        )

    cv2.addWeighted(
        heat,
        0.08,
        frame,
        0.85,
        0,
        frame
    )
    
def draw_session_stats(frame, avg_focus, distractions, minutes, seconds):

    x = 20
    y = 720

    draw_rounded_rect(
        frame,
        (x, y),
        (245, 790),
        (35, 35, 40),
        radius=15
    )

    cv2.putText(
        frame,
        "Session Analytics",
        (x + 15, y + 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        theme.TEXT,
        2
    )

    cv2.putText(
        frame,
        f"Avg Focus : {avg_focus}%",
        (x + 15, y + 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        theme.MUTED,
        2
    )

    cv2.putText(
        frame,
        f"Distractions : {distractions}",
        (x + 15, y + 85),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        theme.MUTED,
        2
    )

    cv2.putText(
        frame,
        f"Session : {minutes:02}:{seconds:02}",
        (x + 15, y + 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        theme.MUTED,
        2
    )