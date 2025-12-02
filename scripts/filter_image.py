import os
import cv2

input_dir = "data/raw"      # Previously filtered images
output_dir = "data/processed"   # Folder for cropped, close-up faces
os.makedirs(output_dir, exist_ok=True)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
# - This initializes an object detector in OpenCV using the Haar Cascade algorithm.
# - A cascade classifier is a machine learning–based approach where the algorithm is trained with lots of positive (faces) and negative (non‑faces) images.
# - Once loaded, you can use it to detect faces in images or video frames.
#  cv2.data.haarcascades
# - This is a built‑in OpenCV path that points to the directory containing pre‑trained Haar Cascade XML files.
# - These XML files store the trained data for detecting specific objects (faces, eyes, smiles, etc.).
#  "haarcascade_frontalface_default.xml"
# - This is one of OpenCV’s pre‑trained models specifically for detecting frontal human faces (faces looking straight at the camera).
# - It’s bundled with OpenCV, so you don’t need to train your own model.

target_count = 1000
selected = 0

def variance_of_laplacian(image): # for figuring out blurry images 
    return cv2.Laplacian(image, cv2.CV_64F).var() #- The Laplacian is a second‑order derivative filter that highlights regions of rapid intensity change (edges).
                                                  #- cv2.CV_64F specifies the output data type (64‑bit float), which avoids overflow and preserves precision.


print("Starting enhanced filtering: close-up, sharp faces...")

for fname in os.listdir(input_dir):
    if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue

    img_path = os.path.join(input_dir, fname)
    img = cv2.imread(img_path)

    if img is None:
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) ## need to change coloured image in gray as better understanding of image pixels
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
# - detectMultiScale scans the image at multiple scales (sizes) to detect objects (faces here).
# - It returns a list of bounding boxes (x, y, w, h) for each detected face.

    if len(faces) != 1:  # Only accept images with exactly 1 face
        continue

    x, y, w, h = faces[0] #- (x, y) = top‑left corner of the face.- w, h = width and height of the detected face region.

    face_area = w * h # Face area
    img_area = img.shape[0] * img.shape[1] # total image area

    # Check if face covers at least 30% of image area
    if (face_area / img_area) < 0.3: # to confirm that the image have only face closeup
        continue

    # Check image sharpness - variance of Laplacian threshold (higher is sharper)
    sharpness = variance_of_laplacian(gray)
    if sharpness < 100:  # Adjust threshold according to dataset
        continue

    # Crop face region with a small margin
    margin = 20 #- Adds a 20‑pixel margin around the face to avoid tight cropping.
    # - Ensures the crop stays within image boundaries (max and min prevent overflow)
    x1 = max(x - margin, 0)
    y1 = max(y - margin, 0)
    x2 = min(x + w + margin, img.shape[1])
    y2 = min(y + h + margin, img.shape[0])
    face_img = img[y1:y2, x1:x2]

    # Resize cropped face to 224x224 for consistency
    face_img = cv2.resize(face_img, (224, 224))

    # Save cropped face
    out_name = f"cropped_{selected + 1:04d}.jpg"
    cv2.imwrite(os.path.join(output_dir, out_name), face_img)
    selected += 1

    if selected % 100 == 0:
        print(f"Selected {selected} images for final dataset...")

    if selected >= target_count:
        break

print(f"\n✓ Complete! {selected} close-up, sharp face images saved to {output_dir}")
