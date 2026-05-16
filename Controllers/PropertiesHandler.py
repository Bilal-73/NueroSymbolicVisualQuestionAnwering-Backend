# def to_python(o):
#     if isinstance(o, np.generic):
#         return o.item()
#     if isinstance(o, np.ndarray):
#         return o.tolist()
#     if isinstance(o, dict):
#         return {k: to_python(v) for k, v in o.items()}
#     if isinstance(o, list):
#         return [to_python(i) for i in o]
#     return o
#
# from mtcnn import MTCNN
#
# detector = MTCNN()
#
# import cv2
# from collections import Counter
# from matplotlib.colors import CSS4_COLORS
# from Services.emotion_services import detect_emotion
# from mtcnn import MTCNN
# import numpy as np
#
# class PropertyHandler:
#     def __init__(self):
#         self.class_names = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
#         # Keep Haar as fallback
#         self.face_cascade = cv2.CascadeClassifier(
#             cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
#         )
#         # Initialize MTCNN detector
#         self.mtcnn = MTCNN()
#     # ================================================================
#     # FACE DETECTION USING HAAR (fallback)
#     # ================================================================
#     def detect_face_haar(self, image, pad=10):
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         faces = self.face_cascade.detectMultiScale(
#             gray,
#             scaleFactor=1.2,
#             minNeighbors=5,
#             minSize=(60, 60)
#         )
#         if len(faces) == 0:
#             return None
#         x, y, w, h = faces[0]
#         pad = max(10, int(0.1 * min(w, h)))
#         y1, y2 = max(0, y - pad), min(image.shape[0], y + h + pad)
#         x1, x2 = max(0, x - pad), min(image.shape[1], x + w + pad)
#         return image[y1:y2, x1:x2]
#     # ================================================================
#     # FACE DETECTION USING MTCNN
#     # ================================================================
#     def detect_face_mtcnn(self, crop):
#         result = self.mtcnn.detect_faces(crop)
#         if len(result) == 0:
#             return None
#         x, y, w, h = result[0]['box']
#         # Ensure coordinates are within image bounds
#         x1, y1 = max(0, x), max(0, y)
#         x2, y2 = min(crop.shape[1], x + w), min(crop.shape[0], y + h)
#         return crop[y1:y2, x1:x2]
#     # ================================================================
#     # MAIN METHOD
#     # ================================================================
#     def assign_properties(self, image, detections):
#         print("Assigning properties to detections...")
#         for det in detections:
#             x, y, w, h = det['bbox']
#             # Crop object with padding
#             pad = 5
#             y1, y2 = max(0, y - pad), min(image.shape[0], y + h + pad)
#             x1, x2 = max(0, x - pad), min(image.shape[1], x + w + pad)
#             crop = image[y1:y2, x1:x2]
#             # COLOR
#             det['color'] = self.detect_dominant_color_name(crop)
#             # SHAPE
#             det['shape'] = self.get_shape(w, h)
#             # EMOTION (ONLY FOR PERSON)
#             if det.get('label', '').lower() == "person":
#                 face = self.detect_face_mtcnn(crop)
#                 if face is None or face.shape[0] < 48:  # height too small
#                     face = crop[:int(0.3 * crop.shape[0]), :]  # take top 30% as fallback
#
#                 if face is not None:
#                     face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
#                     emo_data = detect_emotion(face_rgb)
#                 else:
#                     emo_data = {"emotion": "unknown", "confidence": 0.0, "emotions": {}}
#                 det['emotion'] = emo_data["emotion"]
#             else:
#                 det['emotion'] = "not_applicable"
#
#         return detections
#
#     # ================================================================
#     # COLOR DETECTION
#     # ================================================================
#     def detect_dominant_color_name(self, crop):
#         try:
#             crop = cv2.resize(crop, (50, 50))
#             pixels = crop.reshape(-1, 3)
#             pixels = [tuple(int(c) for c in p) for p in pixels]
#             dominant_rgb = Counter(pixels).most_common(1)[0][0]
#             return self.closest_color(dominant_rgb)
#         except:
#             return "unknown"
#
#     def closest_color(self, rgb):
#         min_dist = float("inf")
#         closest = "unknown"
#         for name, hex_value in CSS4_COLORS.items():
#             r_c, g_c, b_c = tuple(int(hex_value.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
#             dist = sum((comp1 - comp2) ** 2 for comp1, comp2 in zip(rgb, (r_c, g_c, b_c)))
#             if dist < min_dist:
#                 min_dist = dist
#                 closest = name
#         return closest
#
#     # ================================================================
#     # SHAPE PROPERTY
#     # ================================================================
#     def get_shape(self, width, height):
#         ratio = float(width) / float(height) if height != 0 else 0
#         if 0.9 < ratio < 1.1:
#             return "square"
#         elif ratio > 1.5:
#             return "wide"
#         elif ratio < 0.7:
#             return "tall"
#         else:
#             return "rectangle"


import cv2
import numpy as np
import math
from collections import Counter

try:
    from mtcnn import MTCNN
except ImportError:
    MTCNN = None
    print("Warning: MTCNN not installed. Face features will be limited.")

# Try importing emotion service if available in user's project structure
try:
    from Services.emotion_services import detect_emotion
except ImportError:
    def detect_emotion(img):
        return {"emotion": "unknown", "confidence": 0.0}


class PropertyHandler:
    def __init__(self):
        self.colors_db = {
            # Grayscale
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "grey": (128, 128, 128),
            "light_grey": (211, 211, 211),
            "dark_grey": (169, 169, 169),
            "charcoal": (54, 69, 79),
            # Reds
            "red": (255, 0, 0),
            "dark_red": (139, 0, 0),
            "maroon": (128, 0, 0),
            "crimson": (220, 20, 60),
            "tomato": (255, 99, 71),
            "coral": (255, 127, 80),
            "pink": (255, 192, 203),
            "hot_pink": (255, 105, 180),
            # Oranges / Browns
            "orange": (255, 165, 0),
            "dark_orange": (255, 140, 0),
            "brown": (165, 42, 42),
            "saddle_brown": (139, 69, 19),
            "chocolate": (210, 105, 30),
            "tan": (210, 180, 140),
            "beige": (245, 245, 220),
            "gold": (255, 215, 0),
            # Yellows
            "yellow": (255, 255, 0),
            "light_yellow": (255, 255, 224),
            "khaki": (240, 230, 140),
            # Greens
            "green": (0, 128, 0),
            "lime": (0, 255, 0),
            "dark_green": (0, 100, 0),
            "olive": (128, 128, 0),
            "forest_green": (34, 139, 34),
            "teal": (0, 128, 128),
            "turquoise": (64, 224, 208),
            # Blues
            "blue": (0, 0, 255),
            "navy": (0, 0, 128),
            "royal_blue": (65, 105, 225),
            "sky_blue": (135, 206, 235),
            "cyan": (0, 255, 255),
            "light_blue": (173, 216, 230),
            # Purples
            "purple": (128, 0, 128),
            "violet": (238, 130, 238),
            "indigo": (75, 0, 130),
            "magenta": (255, 0, 255),
            "lavender": (230, 230, 250),
        }

        # Initialize face detector if available
        if MTCNN:
            self.mtcnn = MTCNN()
        else:
            self.mtcnn = None
            # Fallback Haar
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    def assign_properties(self, image, detections):
        """
        Main entry point. Modifies detections list in-place.
        """
        print("Assigning refined properties...")

        for det in detections:
            bbox = det.get('bbox', [0, 0, 0, 0])
            x, y, w, h = bbox

            # Safe Crop with padding
            pad = 5
            y1, y2 = max(0, y - pad), min(image.shape[0], y + h + pad)
            x1, x2 = max(0, x - pad), min(image.shape[1], x + w + pad)

            # Ensure valid crop
            if x2 <= x1 or y2 <= y1:
                det['color'] = 'unknown'
                det['shape'] = 'unknown'
                det['emotion'] = 'not_applicable'
                continue

            crop = image[y1:y2, x1:x2]

            # 1. Refined Color (K-Means)
            det['color'] = self.get_dominant_color_kmeans(crop)

            # 2. Refined Shape (Contours)
            det['shape'] = self.get_advanced_shape(crop, w, h)

            # 3. Emotion (Person Only)
            if det.get('label', '').lower() == "person":
                det['emotion'] = self.get_emotion(crop)
            else:
                det['emotion'] = None

        return detections

    # ================= COLORS =================
    def get_dominant_color_kmeans(self, image, k=3):
        """
        Uses K-Means clustering to find the true dominant color of the object,
        ignoring background noise better than simple frequency.
        """
        try:
            # Resize for speed
            img_small = cv2.resize(image, (64, 64))

            # Skip if image is basically empty/black
            if np.mean(img_small) < 5:
                return "black"

            # Convert to RGB (OpenCV is BGR)
            img_rgb = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)
            pixel_data = img_rgb.reshape((-1, 3))
            pixel_data = np.float32(pixel_data)

            # Define criteria = ( type, max_iter = 10, epsilon = 1.0 )
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

            # K-Means
            _, label, centers = cv2.kmeans(pixel_data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

            # Find the most frequent cluster center
            # label.flatten() gives the index of the centroid for each pixel
            counts = Counter(label.flatten())

            # Get the center with most pixels
            # Sometimes the background (if uniform, e.g. white/black) might be dominant.
            # Strategy: if center is very close to pure white/black and k>1, maybe take 2nd?
            # For now, stick to simple dominant.
            dominant_idx = counts.most_common(1)[0][0]
            dominant_color = centers[dominant_idx]  # Float32 array [R, G, B]

            return self.closest_color_name(dominant_color)

        except Exception as e:
            # Fallback
            return "unknown"

    def closest_color_name(self, rgb_tuple):
        """
        Find closest color in self.colors_db using Euclidean distance.
        """
        min_dist = float("inf")
        closest_name = "unknown"

        r, g, b = rgb_tuple

        for name, db_rgb in self.colors_db.items():
            dr = r - db_rgb[0]
            dg = g - db_rgb[1]
            db = b - db_rgb[2]
            dist = math.sqrt(dr * dr + dg * dg + db * db)

            if dist < min_dist:
                min_dist = dist
                closest_name = name

        return closest_name

    # ================= SHAPES =================
    def get_advanced_shape(self, crop, bbox_w, bbox_h):
        """
        Detects shape beyond bbox ratio using Contours.
        """
        res = "undefined"

        try:
            # 1. First Check: Box Ratio (Simple High Level)
            ratio = float(bbox_w) / float(bbox_h) if bbox_h != 0 else 0

            # Convert to Grayscale & Blur
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # Canny Edge Detection
            # Determine threshold automatically using Otsu's or median
            v = np.median(blurred)
            lower = int(max(0, (1.0 - 0.33) * v))
            upper = int(min(255, (1.0 + 0.33) * v))
            edges = cv2.Canny(blurred, lower, upper)

            # Find Contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if not contours:
                # Fallback to ratio
                return self.get_shape_from_ratio(ratio)

            # Largest contour is likely the object
            c = max(contours, key=cv2.contourArea)

            # Approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)
            num_vertices = len(approx)

            # Circularity check
            # Circularity = 4 * pi * Area / (Perimeter^2)
            # 1.0 is perfect circle. Square is ~0.785. Triangle ~0.6.
            area = cv2.contourArea(c)
            if area < 50:  # Too small noise
                return self.get_shape_from_ratio(ratio)

            circularity = (4 * math.pi * area) / (peri * peri) if peri > 0 else 0

            # Logic Tree
            if circularity > 0.8:
                return "circular"  # or "round"
            elif 3 <= num_vertices <= 3:
                return "triangular"
            elif 4 <= num_vertices <= 4:
                # Check aspect ratio of rect
                x, y, w, h = cv2.boundingRect(c)
                ar = w / float(h)
                if 0.9 <= ar <= 1.1:
                    return "square"
                else:
                    return "rectangular"
            elif num_vertices > 6:
                if circularity > 0.7:
                    return "oval" if ratio > 1.5 or ratio < 0.6 else "round"
                else:
                    return "complex_polygon"
            else:
                # If approximate polygon didn't catch 3 or 4 specifically,
                # fall back to ratio
                return self.get_shape_from_ratio(ratio)

        except Exception:
            # Fallback
            return self.get_shape_from_ratio(ratio)

    def get_shape_from_ratio(self, ratio):
        if 0.9 < ratio < 1.1:
            return "square_like"
        elif ratio > 2.0:
            return "elongated_horizontal"  # maybe "wide"
        elif ratio < 0.5:
            return "elongated_vertical"  # maybe "tall"
        else:
            return "rectangular"

    # ================= EMOTION =================
    def get_emotion(self, crop):
        try:
            # Detect face
            face_img = None

            if self.mtcnn:
                faces = self.mtcnn.detect_faces(crop)
                if faces:
                    x, y, w, h = faces[0]['box']
                    # padding
                    x, y = max(0, x), max(0, y)
                    x2, y2 = min(crop.shape[1], x + w), min(crop.shape[0], y + h)
                    face_img = crop[y:y2, x:x2]

            # Fallback Haar if MTCNN failed or empty
            elif hasattr(self, 'face_cascade'):
                gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                if len(faces) > 0:
                    x, y, w, h = faces[0]
                    face_img = crop[y:y + h, x:x + w]

            # Fallback: Top part of person crop (head area)
            if face_img is None or face_img.size == 0:
                h, w = crop.shape[:2]
                face_img = crop[0:int(h * 0.3), :]  # Top 30%

            if face_img is not None and face_img.size > 0:
                face_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
                res = detect_emotion(face_rgb)
                return res.get("emotion", "neutral")

            return "unknown"
        except:
            return "error"




# ===================== Test =====================
# if __name__ == "__main__":
#
#     model_path = r"P:\DemoBackEnd - Copy\modelsNSVQA\last.pt"
#     image_path = r"P:\DemoBackEnd - Copy\static\ImageAnsweringDemoPics\danish.jpg"
#
#     # -------------------------------
#     # Detect objects (YOLO)
#     # -------------------------------
#     scene_handler = SceneGraphHandler(
#         model_path=model_path,
#         image_height=720,
#         image_width=1280
#     )
#
#     objects = scene_handler.detect_objects(image_path)
#
#     print("\nDetected Objects (YOLO Only):")
#     for obj in objects:
#         print(obj)
#
#     # -------------------------------
#     # Load image
#     # -------------------------------
#     image = cv2.imread(image_path)
#     if image is None:
#         print("❌ Failed to load image")
#         exit()
#
#     # -------------------------------
#     # Assign properties
#     # -------------------------------
#     prop_handler = PropertyHandler()
#     objects = prop_handler.assign_properties(image, objects)
#
#     # -------------------------------
#     # Print ONLY properties
#     # -------------------------------
#     print("\nDetected Objects (With Properties):")
#     for obj in objects:
#         print(
#             f"{obj['label']} | "
#             f"Color: {obj.get('color')} | "
#             f"Shape: {obj.get('shape')} | "
#             f"Emotion: {obj.get('emotion')}"
#         )
#
#     # -------------------------------
#     # Visualize detected properties
#     # -------------------------------
#     vis = image.copy()
#
#     for obj in objects:
#         x, y, w, h = obj["bbox"]
#
#         label = obj.get("label", "")
#         color = obj.get("color", "unknown")
#         shape = obj.get("shape", "unknown")
#         emotion = obj.get("emotion", "")
#
#         text = f"{label} | {color} | {shape}"
#         if emotion not in ["not_applicable", "unknown", None]:
#             text += f" | {emotion}"
#
#         # Bounding box
#         cv2.rectangle(vis, (x, y), (x + w, y + h), (0, 255, 0), 2)
#
#         # Text background for readability
#         (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
#         cv2.rectangle(vis, (x, y - th - 10), (x + tw + 5, y), (0, 255, 0), -1)
#
#         # Text
#         cv2.putText(
#             vis,
#             text,
#             (x + 2, y - 5),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.5,
#             (0, 0, 0),
#             2
#         )
#
#     cv2.imshow("Detected Objects + Properties", vis)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
