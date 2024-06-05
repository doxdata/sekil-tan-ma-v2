import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

def detect_shapes(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
        area = cv2.contourArea(contour)
        corners = len(approx)

        if area > 100 and 3 <= corners <= 8:
            cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)
            x, y = approx.ravel()[0], approx.ravel()[1]
            cv2.putText(frame, get_shape_name(corners), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50, param1=50, param2=100, minRadius=20, maxRadius=100)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
            cv2.putText(frame, "Daire", (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    return frame

def get_shape_name(corners):
    shapes = {3: "Ucgen", 4: "Dortgen", 5: "Besgen", 6: "Altigen", 7: "Yedigen", 8: "Sekizgen"}
    return shapes.get(corners, "Daire")

def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = detect_shapes(frame)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.configure(image=imgtk)
    label.after(10, update_frame)

def release_camera():
    if cap.isOpened():
        cap.release()

def main():
    global cap, label
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # DirectShow backend kullanımı

    # Kamera çözünürlüğünü 640x480 olarak ayarla
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("Kamera açılamadı!")
        exit()

    root = tk.Tk()
    root.title("AKVA")
    root.protocol("WM_DELETE_WINDOW", release_camera)

    # Tkinter penceresinin boyutlarını 640x480 olarak ayarla
    root.geometry("640x480")

    label = tk.Label(root)
    label.pack()

    update_frame()

    root.mainloop()

    release_camera()

if __name__ == "__main__":
    main()
