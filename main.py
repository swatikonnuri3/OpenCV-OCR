import cv2
from time import sleep
import requests
import io
import json
import os
import random
from difflib import SequenceMatcher

def calculate_accuracy(detected_text, ground_truth):
    """Calculate OCR accuracy by comparing detected text to ground truth."""
    matcher = SequenceMatcher(None, detected_text, ground_truth)
    accuracy = matcher.ratio() * 100
    return accuracy

key = cv2.waitKey(1)
webcam = cv2.VideoCapture(0)
sleep(2)

print("For Recognize Image PRESS 'S'\n"
      "For QUIT PRESS 'Q\n"
      "After run time if 'images.jpg' is still visible, please re-run the program.\n")

while True:
    try:
        check, frame = webcam.read()
        print(check)  # prints true as long as the webcam is running
        print(frame)  # prints matrix values of each frame
        cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)
        if key == ord('s'):
            cv2.imwrite(filename='images.jpg', img=frame)
            r = random.randint(1, 20000000)
            img_file = 'images' + str(r) + '.jpg'
            cv2.imwrite(filename='data/' + img_file, img=frame)
            webcam.release()
            print("Processing image...")
            img_ = cv2.imread('images.jpg', cv2.IMREAD_ANYCOLOR)
            print("Image saved!")
            cv2.destroyAllWindows()
            break

        elif key == ord('q'):
            webcam.release()
            cv2.destroyAllWindows()
            break

    except KeyboardInterrupt:
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break

sleep(2)
resim = "images.jpg"
img = cv2.imread(resim)
print("Picture is Detected")

api = img

# OCR
url_api = "https://api.ocr.space/parse/image"
_, compressedimage = cv2.imencode(".jpg", api, [1, 90])
file_bytes = io.BytesIO(compressedimage)

result = requests.post(url_api,
                       files={resim: file_bytes},
                       data={"apikey": "helloworld",
                             "language": "eng"})

result = result.content.decode()
print(result)
result = json.loads(result)

parsed_results = result.get("ParsedResults")[0]
text_detected = parsed_results.get("ParsedText", "").strip()
print("Detected Text:")
print(text_detected)

# Define the ground truth text for accuracy evaluation
ground_truth_text = "Your expected text in the image here"

# Calculate accuracy
accuracy = calculate_accuracy(text_detected, ground_truth_text)
print(f"OCR Accuracy: {accuracy:.2f}%")

# Save detected text to a file
print("Text is writing to file...")
with open("text_detected.txt", "a+") as f:
    f.write(text_detected)
f.close()
print("Operation is successful")

# Display the image
cv2.imshow("roi", api)
cv2.imshow("Img", img)
cv2.waitKey(0)
os.remove(resim)
