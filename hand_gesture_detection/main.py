import cv2
import mediapipe as mp
import streamlit as st
import threading

# Inicializar MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Variables globales
gesture_frame = None
gesture_text = ""
frame_lock = threading.Lock()

# Clasificación de gestos
def classify_gesture(hand_landmarks):
    tips = [
        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP],
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP],
    ]
    mcp = [
        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP],
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP],
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP],
        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP],
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP],
    ]
    fingers_up = sum([tips[i].y < mcp[i].y for i in range(5)])
    if fingers_up == 5:
        return "Palma abierta"
    elif fingers_up == 0:
        return "Puño cerrado"
    elif (tips[1].y < mcp[1].y and tips[0].y < mcp[0].y and fingers_up == 2):
        return "Pulgar e índice en L"
    elif (tips[1].y < mcp[1].y and fingers_up == 1):
        return "Índice levantado"
    else:
        return "Otro gesto"

# Hilo para procesar cámara
def process_camera():
    global gesture_frame, gesture_text
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5) as hands:
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            text_overlay = []
            if results.multi_hand_landmarks:
                for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    gesture = classify_gesture(hand_landmarks)
                    text_overlay.append(f"Mano {i+1}: {gesture}")

            with frame_lock:
                gesture_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                gesture_text = "\n".join(text_overlay)

# Streamlit App
st.title("Detección de Gestos de Mano")
st.text("Con enfoque en aprender e implementar en el segundo semestre 2023")
st.write("https://github.com/SebastianPinzonC/Operativos-2023")

# Iniciar hilo
threading.Thread(target=process_camera, daemon=True).start()

frame_placeholder = st.empty()
gesture_placeholder = st.empty()

# Actualizar frames en Streamlit
import time
while True:
    with frame_lock:
        if gesture_frame is not None:
            frame_placeholder.image(gesture_frame)
            gesture_placeholder.text(gesture_text)
    time.sleep(0.03)
