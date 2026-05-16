
import re

from nltk import word_tokenize

PRONOUN_MAP = {
    "he": "person",
    "she": "person",
    "him": "person",
    "her": "person",
    "they": "person",
    "them": "person"
}
import nltk

class TaskHandler:



    def __init__(self, objects, scene_graph, properties):
        self.objects = objects
        self.scene_graph = scene_graph
        self.properties = {o: p for o, p in zip(objects, properties)}

        self.MONITOR_REGEX = re.compile(
            r"^(let me know when|Monitor\s)(?P<obj1>[\w\s]+?)(?:s)?\s+(?P<action>emotion changes|smiles|happy|smile)\??$",
            re.IGNORECASE
        )
        self.TEMP_REGEX = re.compile(
            r"^let\s+me\s+know\s+(when|if)\s(?P<obj>[\w\s]+?)(?:s)?\s+(?P<action>leaves|leave|left|comes|come|enter|enters)\??$",
            re.IGNORECASE
        )

    def debug(self):
        import pprint
        pp = pprint.PrettyPrinter(indent=4)

        print("\n--- OBJECTS ---")
        pp.pprint(self.objects)

        print("\n--- SCENE GRAPH ---")
        pp.pprint(self.scene_graph)

        print("\n--- PROPERTIES ---")
        pp.pprint(self.properties)

    def resolve_object(self, name):
        exact = [o for o in self.objects if o.lower() == name.lower()]
        if exact:
            return exact[0]
        prefix = [o for o in self.objects if o.lower().startswith(name.lower())]
        return prefix[0] if len(prefix) == 1 else None

    def task_answer(self, obj_name, question,action):
        print("In task Answer")
        print(action)
        obj = self.resolve_object(obj_name)
        print(obj)
        tokens=word_tokenize(str(question))
        print(tokens)

        if action in {"come", "comes", "enter", "enters"}:
            return f"Yes the {obj} has entered" if obj_name else f"No, {obj} is not entered right now"
        if action in {"leave", "leaves", "left"}:
            return f"No, the {obj} is still inside the room." if obj_name else f"Yes, the {obj} has left the room."

    def task_answer_emotion(self, obj_name):
        print("In task Emotion Answer")
        obj = self.resolve_object(obj_name)
        print(obj)



        obj_emotion = self.properties.get(obj, {}).get("emotion")
        if obj_emotion in {None, "none", "not_applicable"}:
            return "Emotion is not applicable for this object."
        return f"Yes,Person is {obj_emotion}" if obj_emotion.lower() == obj_emotion.lower() else f"No, Person is not {obj_emotion}"



    def resolve_pronouns(self, text):
        return " ".join(PRONOUN_MAP.get(w, w) for w in text.lower().split())
    def answer_emotion(self, obj_name, emotion):
        obj = self.resolve_object(obj_name)
        if not obj:
            return f"Object {obj_name} not present"
        obj_emotion = self.properties.get(obj, {}).get("emotion")
        if obj_emotion in {None, "none", "not_applicable"}:
            return "Emotion is not applicable for this object."
        return f"Yes,Person is {emotion}" if obj_emotion.lower() == emotion.lower() else f"No, Person is not {emotion}"


    def ask(self, question):
        print("recieved : ", question)
        question = self.resolve_pronouns(question.strip().lower())

        # ---------------- Summary ----------------


        print(type(question))
        m = self.TEMP_REGEX.match(question)
        print(m)
        n = self.MONITOR_REGEX.match(question)
        print(n)

        if m!=None:
            return self.task_answer(m.group("obj"),question,m.group("action"))
        if n!=None:
            return self.task_answer_emotion(n.group("obj1"))
        # print("Not a temp question")
        # if n!=None:
        #     obj_name = (m.group("obj1") or m.group("obj2") or m.group("obj3") or m.group("obj4"))
        #     emotion = (m.group("emo1") or m.group("emo2") or m.group("emo3") or m.group("emo4"))
        #     return self.answer_emotion(obj_name, emotion)
        # print("Not a Monitor question")

        return None