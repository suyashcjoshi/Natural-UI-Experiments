import cv2
import mediapipe
import speech_recognition as sr
import pyttsx3
import pyautogui
import webbrowser as web
import tkinter as tk

class NUI:
    # Class methods here
    def __init__(self):
        self.speech_recognizer = sr.Recognizer()
        self.hand_recognizer = mediapipe.solutions.hands.Hands()
        self.draw_options = mediapipe.solutions.drawing_utils
        self.screen_width, self.screen_height = pyautogui.size()
        self.x1 = self.x2 = self.y1 = self.y2 = 0
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=600, height=600, bg='white')
        self.canvas.create_line(0, 300, 600, 300, width=2)  # x-axis
        self.canvas.create_line(300, 0, 300, 600, width=2)  # y-axis
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.pack()

    def detect_gesture(self):
        camera = cv2.VideoCapture(0)
        while True:
            _, image = camera.read()
            image_height, image_width, _ = image.shape
            image = cv2.flip(image, 1)  # flip the mirrored image
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # convert to RGB format
            hands_output = self.hand_recognizer.process(rgb_image)
            all_hands = hands_output.multi_hand_landmarks
            if all_hands:
                for hand in all_hands:
                    self.draw_options.draw_landmarks(image, hand)
                    one_hand_landmarks = hand.landmark
                    for id, lm in enumerate(one_hand_landmarks):
                        x = int(lm.x * image_width)  # normalize the value
                        y = int(lm.y * image_height)  # normalize the value
                        if id == 4:  # detect if it's a thumb
                            mouse_x = int((self.screen_width / image_width) * x)
                            mouse_y = int((self.screen_height / image_height) * y)
                            cv2.circle(image, (x, y), 20, (0, 255, 255))
                            pyautogui.moveTo(mouse_x, mouse_y)
                            self.x1 = x
                            self.y1 = y
                        if id == 8:  # detect if it's an index finger
                            self.x2 = x
                            self.y2 = y
                            cv2.circle(image, (x, y), 20, (0, 255, 255))
                finger_vertical_distance = self.y1 - self.y2
                print(finger_vertical_distance)
                if finger_vertical_distance < 70:
                    pyautogui.click()
                    print("clicked!")

            cv2.imshow("Video capture", image)

            key = cv2.waitKey(100)
            if key == 27:  # pressing esc key will close the window
                break
        camera.release()
        cv2.destroyAllWindows()

    def control_gui(self, string):
        print(string)
        web.open('https://' + string, new = 2)

    def speak(self, command):
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()

    def get_mic_input(self):
        # List available microphones (optional)
        print("Available microphones:")
        print(sr.Microphone.list_microphone_names())
        try:
            with sr.Microphone() as source:
                print("Starting Speech Recognition...")
                self.speech_recognizer.adjust_for_ambient_noise(source, duration = 2.0)
                recorded_audio = self.speech_recognizer.listen(source)
                recognized_text = self.speech_recognizer.recognize_google(recorded_audio)
                recognized_text = recognized_text.lower()
                print(recognized_text)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service:", e)
        except Exception as ex:
            print("Error during recognition:", ex)

        return recognized_text
    
    def draw(self):
        x, y = event.x, event.y
        self.canvas.create_oval(x-3, y-3, x+3, y+3, fill='black')

    def main(self):
        recognized_text = self.get_mic_input()  # Get the recognized text first
        self.control_gui(recognized_text)  # Then use the recognized text in control_gui
        self.detect_gesture()  # Finally, run detect_gesture
        #self.draw(self)

if __name__ == '__main__':
    gesture_controller = NUI()
    gesture_controller.main()
