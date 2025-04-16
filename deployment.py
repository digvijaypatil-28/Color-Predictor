import cv2
import pandas as pd

df=pd.read_csv(r'D:\Coding\Machine Learning\Color Predictor\colors.csv')

# Global variables
clicked = False
r = g = b = xpos = ypos = 0

# KNN function to get the nearest color name
def get_color_name(R, G, B, df):
    min_dist = float('inf')
    color_name = ""
    for i in range(len(df)):
        d = ((R - df.loc[i, "R"])**2 +
             (G - df.loc[i, "G"])**2 +
             (B - df.loc[i, "B"])**2) ** 0.5
        if d < min_dist:
            min_dist = d
            color_name = df.loc[i, "color_name"]
    return color_name

# Mouse callback function
def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

# Load image
img_path = r"D:\Coding\Machine Learning\Color Predictor\Static\color_detection_window_opencv.png.webp"  # Replace with your image file
img = cv2.imread(img_path)
cv2.namedWindow('Color Detection')
cv2.setMouseCallback('Color Detection', draw_function)

while True:
    cv2.imshow("Color Detection", img)
    if clicked:
        # Draw rectangle
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Get color name
        text = get_color_name(r, g, b, df)

        # Display text
        cv2.putText(img, text, (30, 50), 2, 0.8, (255, 255, 255), 2)
        if r + g + b >= 600:
            cv2.putText(img, text, (30, 50), 2, 0.8, (0, 0, 0), 2)

        clicked = False

    # Exit on ESC key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()