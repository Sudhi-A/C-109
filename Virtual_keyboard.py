import cv2
import mediapipe as mp
from pynput.keyboard import Key,Controller

Keyboard = Controller()

cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawings_utils

hands = mp_hands(min_detection_confidence = 0.8, min_tracking_confidence = 0.5)

tipIds = [4, 8, 12, 16, 20]

state = None

#Define a function to count fingers

def countFinger(image, hand_landmarks, handNo = 0):
    
    global state
    
    if hand_landmarks:
        #Get all landmarks of the First Hand VISIBLE
         
        landmarks = hand_landmarks[handNo].landmark

        # Count Fingers
        Fingers = []
        
        for lm_index in tipIds:
            #Get Finger Tip and Bottom y Position Values
            
            
            Finger_tip_y = landmarks[lm_index].y
            Finger_bottom_y = landmarks[lm_index - 2].y

            #Check if any Finger is OPEN or Closed
            if lm_index != 4:
                if Finger_tip_y  < Finger_bottom_y:
                    Fingers.append(1)
                    #print("Finger with id", lm_index,is Open)

                if Finger_tip_y > Finger_bottom_y:
                    Fingers.append(0)
                    #print("Finger with id", lm_index,is Closed)        


        total_fingers = Fingers.count(1)


        # PLAY or PAUSE a Video
        if total_fingers == 4:
            state = "Play"
            
        if total_fingers == 0 and state == "Play":
            state = "Pause"
            Keyboard.press(Key.space)

        #Move Video Forward & BackWards
        Finger_tip_x = (landmarks[8].x)*width

        if total_fingers == 1:
            if Finger_tip_x < width-400:
                print("Play backward")
                Keyboard.press(Key.left)
            if Finger_tip_x > width-50:
                print("Play Forward")
                Keyboard.press(Key.right)

#Define a function to

    def drawHandLandMarks(image, hand_landmarks):

        #Draw connections between landmark points
        if hand_landmarks:
            
            for land_marks in hand_landmarks:
               
                mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)
    
    while True:
        success, image = cap.read()
        
        image = cv2.flip(image, 1)

        #Detect the Hands Landmarks
        results = hands.process(image)

        #Get landmark position from the processed result

        hand_landmarks = results.multi_hand_landmarks

        #Draw LandMarks

        
        drawHandLandMarks(image, hand_landmarks)

        #GetnHand Fingers Position
        
        countFinger(image, hand_landmarks)
        cv2.imshow("Media Controller", image)        
        



    
    