# import torch
# import cv2
# import numpy as np
#
# from ultralytics import YOLO
# class SceneGraphHandler:
#     def __init__(self, model_path='P:\DemoBackEnd\modelsNSVQA\last.pt', margin=20, overlap_thresh=0.3,
#                  image_height=720, near_thresh=0.1):
#         # Initialize YOLO model from provided path
#         self.model = YOLO(model_path)  # Load the YOLO model from the specified path
#
#         self.margin = margin  # Margin to adjust spatial relations
#         self.overlap_thresh = overlap_thresh  # Overlap threshold for under relation
#         self.image_height = image_height
#         self.near_thresh = near_thresh  # Threshold for proximity (near relation)
#
#     def get_center(self, x, y, w, h):
#         """Calculate the center of a bounding box."""
#         return x + w / 2, y + h / 2
#
#     def get_depth_score(self, bbox):
#         """Calculate a depth score based on the size and vertical position of the object."""
#         x, y, w, h = bbox
#         area = w * h
#         cx, cy = self.get_center(x, y, w, h)
#
#         α = 0.6
#         β = 0.4
#
#         size_depth = 1 / (area + 1e-6)  # Inverse of area (larger objects are farther away)
#         vertical_depth = cy / self.image_height  # Vertical position (top-to-bottom)
#
#         return α * size_depth + β * vertical_depth
#
#     def horizontal_overlap(self, b1, b2):
#         """Calculate the horizontal overlap between two bounding boxes."""
#         x1, y1, w1, h1 = b1
#         x2, y2, w2, h2 = b2
#
#         l1, r1 = x1, x1 + w1
#         l2, r2 = x2, x2 + w2
#
#         overlap = max(0, min(r1, r2) - max(l1, l2))
#         return overlap / max(w1, w2)
#
#     def vertical_overlap(self, b1, b2):
#         """Calculate the vertical overlap between two bounding boxes."""
#         x1, y1, w1, h1 = b1
#         x2, y2, w2, h2 = b2
#
#         t1, b1 = y1, y1 + h1
#         t2, b2 = y2, y2 + h2
#
#         overlap = max(0, min(b1, b2) - max(t1, t2))
#         return overlap / max(h1, h2)
#
#
#     def get_relation(self, obj1, obj2):
#         """Get the spatial relationship between two objects."""
#         x1, y1, w1, h1 = obj1["bbox"]
#         x2, y2, w2, h2 = obj2["bbox"]
#
#         cx1, cy1 = self.get_center(x1, y1, w1, h1)
#         cx2, cy2 = self.get_center(x2, y2, w2, h2)
#
#         bottom1 = y1 + h1
#         bottom2 = y2 + h2
#
#         depth1 = self.get_depth_score(obj1["bbox"])
#         depth2 = self.get_depth_score(obj2["bbox"])
#
#         # LEFT / RIGHT
#         if cx1 + self.margin < cx2:
#             return "left_of"
#         if cx1 - self.margin > cx2:
#             return "right_of"
#
#         # ABOVE / BELOW
#         if bottom1 + self.margin < y2:
#             return "above"
#         if y1 > bottom2 + self.margin:
#             return "below"
#
#         # UNDER (below + horizontal overlap)
#         if self.horizontal_overlap(obj1["bbox"], obj2["bbox"]) > self.overlap_thresh:
#             if y1 > bottom2:
#                 return "under"
#
#         # IN FRONT OF / BEHIND (depth estimation)
#         if depth1 + 0.05 < depth2:  # Increase/decrease this threshold to refine
#             return "in_front_of"
#         if depth1 - 0.05 > depth2:
#             return "behind"
#
#         # NEAR (proximity check)
#         if abs(cx1 - cx2) < self.near_thresh * self.image_height and abs(
#                 cy1 - cy2) < self.near_thresh * self.image_height:
#             return "near"
#
#         return "unknown"
#
#
#     def build_adjacency_matrix(self, objects):
#         """Build an adjacency matrix to store spatial relations between objects."""
#         n = len(objects)
#         matrix = [['' for _ in range(n + 1)] for _ in range(n + 1)]
#
#         labels = [f"{obj['label']}_{i}" for i, obj in enumerate(objects)]
#
#         # Header row/column
#         matrix[0][0] = ''
#         for i in range(n):
#             matrix[0][i + 1] = labels[i]
#             matrix[i + 1][0] = labels[i]
#
#         # Fill relations
#         for i in range(n):
#             for j in range(n):
#                 if i == j:
#                     continue
#
#                 relation = self.get_relation(objects[i], objects[j])
#                 matrix[i + 1][j + 1] = relation
#
#         return matrix
#
#
# # Function to load the image and detect objects using YOLOv5
# def detect_objects(self, image_path):
#     # Load the image using OpenCV
#     image = cv2.imread(image_path)
#
#     # Perform inference with YOLOv5
#     results = self.model.predict(image_path, show=False)  # Inference on the image
#     boxes = results[0].boxes  # Get the bounding boxes
#
#     detected = []
#     for i, box in enumerate(boxes):
#         cls_id = int(box.cls[0].item())  # Get the class ID
#         label = results[0].names[cls_id]  # Get the class name from the model
#         x_center, y_center, w, h = box.xywh[0].tolist()  # Get bounding box (x_center, y_center, width, height)
#
#         # Convert to xmin, ymin, width, height format
#         x_min = int(x_center - w / 2)
#         y_min = int(y_center - h / 2)
#
#         detected.append({
#             'label': label,
#             'bbox': [x_min, y_min, int(w), int(h)]  # Save the bounding box coordinates
#         })
#
#     return detected
#
#
#
# # Example usage
# if __name__ == "__main__":
#     # Path to the image
#     image_path=r"../static/ImageAnsweringDemoPics/manwithball.jpg"
#     # image_path = r"P:\DemoBackEnd - Copy\static\ImageAnsweringDemoPics\manwithball.jpg"  # Replace with the path to your image
#
#     # Initialize SceneGraphHandler with YOLO model path
#     model_path = "../modelsNSVQA/last.pt"  # Replace with your YOLO model path
#     scene_handler = SceneGraphHandler(model_path=model_path, margin=20, overlap_thresh=0.3, image_height=720,
#                                       near_thresh=0.1)
#
#     # Detect objects in the image using YOLOv5
#     objects = detect_objects(scene_handler, image_path)  # Pass the handler to the function
#
#     # Print relations between objects
#     for i, obj1 in enumerate(objects):
#         for j, obj2 in enumerate(objects):
#             if i != j:
#                 relation = scene_handler.get_relation(obj1, obj2)
#                 print(f"Relation between {obj1['label']} and {obj2['label']}: {relation}")
#
#     # Build adjacency matrix
#     adjacency_matrix = scene_handler.build_adjacency_matrix(objects)
#     print("\nAdjacency Matrix:")
#     for row in adjacency_matrix:
#         print(row)
#

import math
try:
    from ultralytics import YOLO

    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("Warning: 'ultralytics' module not found. Object detection will not work, but logic is accessible.")


class SceneGraphHandler:
    def __init__(self, model_path=None, image_height=720, image_width=1280, near_thresh=140, overlap_thresh=0.1):
        if model_path and YOLO_AVAILABLE:
            self.model = YOLO(model_path)
        else:
            self.model = None

        self.image_height = image_height
        self.image_width = image_width
        self.near_thresh = near_thresh
        self.overlap_thresh = overlap_thresh

    def get_bbox_center(self, bbox):
        x, y, w, h = bbox
        return x + w / 2, y + h / 2

    def get_depth_score_feature(self, bbox):
        """
        Simple depth heuristic: Lower Y-bottom = Closer to camera.
        Returns the y-coordinate of the bottom edge.
        Higher value = Closer (since Y increases downwards).
        """
        x, y, w, h = bbox
        return y + h

    def compute_iou(self, boxA, boxB):
        Ax1, Ay1, Aw, Ah = boxA
        Ax2, Ay2 = Ax1 + Aw, Ay1 + Ah
        Bx1, By1, Bw, Bh = boxB
        Bx2, By2 = Bx1 + Bw, By1 + Bh

        xA = max(Ax1, Bx1)
        yA = max(Ay1, By1)
        xB = min(Ax2, Bx2)
        yB = min(Ay2, By2)

        interWidth = max(0, xB - xA)
        interHeight = max(0, yB - yA)
        interArea = interWidth * interHeight

        areaA = Aw * Ah
        areaB = Bw * Bh

        iou = interArea / float(areaA + areaB - interArea + 1e-6)
        return iou

    def get_euclidean_distance(self, bbox1, bbox2):
        cx1, cy1 = self.get_bbox_center(bbox1)
        cx2, cy2 = self.get_bbox_center(bbox2)
        return math.sqrt((cx1 - cx2) ** 2 + (cy1 - cy2) ** 2)

    def get_relation(self, obj1, obj2):
        box1 = obj1['bbox']
        box2 = obj2['bbox']

        iou = self.compute_iou(box1, box2)
        dist = self.get_euclidean_distance(box1, box2)

        cx1, cy1 = self.get_bbox_center(box1)
        cx2, cy2 = self.get_bbox_center(box2)

        # Dimensions
        w1, h1 = box1[2], box1[3]
        w2, h2 = box2[2], box2[3]

        # Top/Bottom edges
        top1, bottom1 = box1[1], box1[1] + h1
        top2, bottom2 = box2[1], box2[1] + h2

        # Directional Deltas
        dx = cx2 - cx1  # Positive if obj2 is Right
        dy = cy2 - cy1  # Positive if obj2 is Down (Below)

        # ---------------------------------------------------------
        # 1. CHECK "ON" (Vertical Support)
        # ---------------------------------------------------------
        # Obj1 (Top) ON Obj2 (Bottom)
        # Conditions:
        # - Physically above: cy1 < cy2
        # - Good horizontal alignment
        # - Vertical proximity: bottom of 1 is near top of 2
        # REFINEMENT: Allow some overlap (perspective often places cup slightly 'inside' table box)

        x_overlap = min(box1[0] + w1, box2[0] + w2) - max(box1[0], box2[0])
        horizontal_overlap_ratio = x_overlap / float(min(w1, w2) + 1e-6)

        # Check if obj1 is smaller (support logic)
        is_smaller = (w1 * h1) < (w2 * h2) * 0.8

        if horizontal_overlap_ratio > 0.3 and cy1 < cy2:
            # Vertical Check:
            # Bottom1 should be close to Top2 OR inside the top region of Box2
            gap = top2 - bottom1
            # "On" usually means bottom1 is >= top2 (gap <= 0) but not too deep
            # Allow bottom1 to sink into obj2 up to 30% of obj2's height (perspective)
            # Allow bottom1 to float above obj2 up to 10% of obj2's height
            if -h2 * 0.4 < gap < h2 * 0.1:  # or bottom1 is roughly at top2
                return "on"
            # Support case: sitting strictly inside the bounding box but at the top
            if bottom1 > top2 and bottom1 < top2 + (h2 * 0.5):
                # Stronger check: is it smaller?
                if is_smaller:
                    return "on"

        # ---------------------------------------------------------
        # 2. CHECK "IN FRONT OF" / "BEHIND" (Partial Occlusion)
        # ---------------------------------------------------------
        # If overlapping significantly
        if iou > self.overlap_thresh:
            y_bottom1 = self.get_depth_score_feature(box1)
            y_bottom2 = self.get_depth_score_feature(box2)

            # Whichever bottom is lower (higher Y) is clearly in front
            diff = y_bottom1 - y_bottom2

            # Threshold: must be significantly lower (e.g., 5% of img height or simple pixel relative)
            # Normalizing by object height helps robustness
            avg_h = (h1 + h2) / 2

            if diff > avg_h * 0.1:
                return "behind"
            elif diff < -avg_h * 0.1:
                return "in_front_of"

        # ---------------------------------------------------------
        # 3. CHECK "NEAR"
        # ---------------------------------------------------------
        # Distance-based, if not overlapping much
        if dist < self.near_thresh:
            return "near"

        # ---------------------------------------------------------
        # 4. DIRECTIONAL (Fallback)
        # ---------------------------------------------------------
        # If mainly horizontal difference
        if abs(dx) > abs(dy):
            return "left_of" if dx > 0 else "right_of"
        else:
            return "above" if dy > 0 else "below"

    def build_adjacency_matrix(self, objects):
        """
        Builds a matrix where M[i][j] is the relation from object i to object j.
        """
        n = len(objects)
        labels = [obj['label'] for obj in objects]

        matrix = [[None] * (n + 1) for _ in range(n + 1)]
        matrix[0][0] = ""
        for i in range(n):
            matrix[0][i + 1] = labels[i]
            matrix[i + 1][0] = labels[i]

        for i in range(n):
            for j in range(n):
                if i == j:
                    matrix[i + 1][j + 1] = "self"
                    continue

                rel = self.get_relation(objects[i], objects[j])
                matrix[i + 1][j + 1] = rel

        return matrix

    def detect_objects(self, image_path):
        if not self.model:
            print("Model not loaded.")
            return []

        results = self.model.predict(image_path, show=False)
        boxes = results[0].boxes

        detected = []
        for box in boxes:
            cls_id = int(box.cls[0].item())
            label = results[0].names[cls_id]

            x_c, y_c, w, h = box.xywh[0].tolist()
            x = int(x_c - w / 2)
            y = int(y_c - h / 2)

            detected.append({
                "label": label,
                "bbox": [x, y, int(w), int(h)],
                "confidence": float(box.conf[0].item())
            })

        return detected

# ===================== Test =====================
if __name__ == "__main__":
    from config import YOLO_MODEL_PATH, IMAGE_ANSWERING_DEMO_DIR
    
    model_path = str(YOLO_MODEL_PATH)
    image_path = str(IMAGE_ANSWERING_DEMO_DIR / "bilal.jpg")

    handler = SceneGraphHandler(
        model_path=model_path,
        image_height=720,
        image_width=1280
    )

    objects = handler.detect_objects(image_path)

    print("\nDetected Objects:")
    for obj in objects:
        print(obj)

    print("\nRelations:")
    for i, obj1 in enumerate(objects):
        for j, obj2 in enumerate(objects):
            if i != j:
                rel = handler.get_relation(obj1, obj2)
                print(f"{obj1['label']} -> {obj2['label']} : {rel}")

    print("\nAdjacency Matrix:")
    matrix = handler.build_adjacency_matrix(objects)
    for row in matrix:
        print(row)
