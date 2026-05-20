import cv2
import theme


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
    
    
    
PANEL_WIDTH = 260


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
        0.15,
        0,
        frame
    )
    
    
    
def draw_card(frame, title, value, y):
    x =15
    width = PANEL_WIDTH - 30
    height = 70

    # Card background
    cv2.rectangle(
        frame,
        (x, y),
        (x + width, y + height),
        (45, 45, 45),
        -1
    )
     # Small accent line
    cv2.rectangle(
        frame,
        (x, y),
        (x + 5, y + height),
        theme.PRIMARY,
        -1
    )
    
    # Title
    cv2.putText(
        frame,
        title,
        (x + 15, y + 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        theme.MUTED,
        1
    )

    # Value
    cv2.putText(
        frame,
        str(value),
        (x + 15, y + 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        theme.TEXT,
        2
    )