import os
import json
import re
import joblib
import numpy as np
from config import RELATION_CLASSIFIER_PATH, VECTORIZER_PATH, KG_DIR

# Try importing pyttsx3
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False


class MLKGBasedQA:
    def __init__(
        self,
        kg_folder,
        model_path=None,
        vectorizer_path=None,
        confidence_threshold=0.8
    ):
        if model_path is None:
            model_path = str(RELATION_CLASSIFIER_PATH)
        if vectorizer_path is None:
            vectorizer_path = str(VECTORIZER_PATH)
            
        self.kg_folder = kg_folder
        self.confidence_threshold = confidence_threshold

        # Load KG
        self.kg = self.load_kg()
        self.objects = list(self.kg.keys()) or ["dummy_object"]

        # Load ML models
        self.clf = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)

        # Answer templates
        self.templates = {
            "used for": "{object} is used for {value}.",
            "has part": "{object} consists of {value}.",
            "part of": "{object} is part of {value}.",
            "material used": "{object} is made from {value}.",
            "subclass of": "{object} belongs to {value}.",
            "lifespan": "{object} typically lasts {value}.",
            "weight": "{object} weighs around {value}.",
            "height": "{object} has a height of {value}.",
            "color": "{object} is available in {value}.",
            "manufacturer": "{object} is manufactured by {value}."
        }

    # -------------------------
    # TEXT TO SPEECH
    # -------------------------
    def speak(self, text):
        if not TTS_AVAILABLE:
            return
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 160)
            engine.setProperty("volume", 1.0)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except:
            pass

    # -------------------------
    # LOAD KNOWLEDGE GRAPH
    # -------------------------
    def load_kg(self):
        kg = {}
        if not os.path.exists(self.kg_folder):
            print(f"KG folder not found: {self.kg_folder}")
            return kg

        for file in os.listdir(self.kg_folder):
            if file.endswith(".json"):
                with open(os.path.join(self.kg_folder, file), "r", encoding="utf-8") as f:
                    data = json.load(f)

                obj = data["object"].lower()
                kg[obj] = {}

                for _, relation, value in data["triplets"]:
                    kg[obj].setdefault(relation.lower(), []).append(value)

        return kg

    # -------------------------
    # RELATION DETECTION (ML)
    # -------------------------
    def detect_relation(self, question):
        vec = self.vectorizer.transform([question])
        probs = self.clf.predict_proba(vec)[0]

        best_idx = np.argmax(probs)
        confidence = probs[best_idx]
        relation = self.clf.classes_[best_idx]

        if confidence < self.confidence_threshold:
            return None

        return relation

    # -------------------------
    # OBJECT DETECTION
    # -------------------------
    def detect_object(self, question):
        q = question.lower()
        matches = []

        for obj in self.objects:
            pattern = r"\b" + re.escape(obj) + r"\b"
            if re.search(pattern, q):
                matches.append(obj)

        if matches:
            return max(matches, key=len)  # longest match

        return None

    # -------------------------
    # ANSWER
    # -------------------------
    def answer(self, question):
        # 1️⃣ Relation
        relation = self.detect_relation(question)
        if not relation:
            return None  # IMPORTANT for hybrid fallback

        # 2️⃣ Object
        obj = self.detect_object(question)
        if not obj:
            return None

        # 3️⃣ KG lookup
        if relation not in self.kg[obj]:
            return None

        value = ", ".join(self.kg[obj][relation])
        template = self.templates.get(relation)

        return template.format(
            object=obj.capitalize(),
            value=value
        )


# =========================
# INTERACTIVE TEST
# =========================
if __name__ == "__main__":
    qa = MLKGBasedQA(str(KG_DIR))

    print("\n=== CLASS-BASED ML QA ===")
    print("Type 'exit' to quit\n")

    while True:
        q = input("Q: ")
        if q.lower() == "exit":
            break

        ans = qa.answer(q)
        if not ans:
            ans = "Sorry, I could not understand your question."

        print("A:", ans)
        qa.speak(ans)
