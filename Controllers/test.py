from Controllers.scene_questions import *

ALL_TESTS = {

    # =========================
    # SUMMARY
    # =========================
    QuestionType.SUMMARY: [
        "What is in front of me?",
        "Tell me how many objects are present?",
        "Can you tell me what objects are here?"
    ],

    # =========================
    # OBJECT EXISTENCE (basic)
    # =========================
    QuestionType.OBJECT_EXISTENCE: [
        "Is there a chair?",
        "Is there a person?",
        "Is there a bottle?"
    ],

    # =========================
    # OBJECT EXISTENCE (natural)
    # =========================
    QuestionType.OBJECT_EXISTENCE_ALT: [
        "Do you see a chair?",
        "Is any bottle present?",
        "Can you find a person?",
        "Do you see person?",
        "Is any chair?"
    ],

    # =========================
    # COUNTING (explicit)
    # =========================
    QuestionType.COUNT_SPECIFIC: [
        "How many chairs are there?",
        "How many bottles present?",
        "How many people are there?",
        "How many objects are there in the scene?"
    ],

    # =========================
    # COUNTING (implicit / short)
    # =========================
    QuestionType.COUNT_IMPLICIT: [
        "Count the chairs",
        "Count chairs",
        "Number of bottles?",
        "Number of people"
    ],

    # =========================
    # COUNTING (container)
    # =========================
    QuestionType.COUNT_CONTAINER: [
        "How many apples are in the basket?",
        "How many books are on the table?",
        "How many cups are there in tray?",
        "How many bottles are there in the box?"
    ],

    # =========================
    # MOVEMENT
    # =========================
    QuestionType.MOVEMENT: [
        "Tell me if person enters the room",
        "Tell me if person leaves",
        "Tell me if chair left",
        "Tell me if bottle comes",
        "Tell me if person enters"
    ],

    # =========================
    # RELATION (existence & count)
    # =========================
    QuestionType.RELATION_EXISTENCE: [
        "Is there anything left of table?",
        "Is there anything near person?",
        "Is there anything above chair?",
        "How many objects right of bottle?",
        "How many objects below table?"
    ],

    # =========================
    # PROPERTY
    # =========================
    QuestionType.PROPERTY: [
        "What is the color of chair?",
        "Tell me shape of bottle?",
        "Tell me emotion of person?",
        "What is the bbox of chair?"
    ],

    # =========================
    # POSITION
    # =========================
    QuestionType.POSITION: [
        "Is the person in the center?",
        "Is the chair in the top left?",
        "What objects are in the top left?",
        "What objects are in the bottom right?"
    ],

    # =========================
    # MONITOR / EVENT
    # =========================
    QuestionType.MONITOR: [
        "Notify me when a person enters",
        "Notify me when chair leaves",
        "Alert me if bottle comes",
        "Alert me if person goes"
    ],

    # =========================
    # UNKNOWN (should fail)
    # =========================
    QuestionType.UNKNOWN: [
        "Where is the chair?",
        "Describe the scene",
        "Is the chair red and near the table?",
        "What is happening?",
        "Explain what you see"
    ]
}


def detect_intent(q: str):
    ql = q.lower().strip()

    if ql in SUMMARY_QUESTIONS:
        return QuestionType.SUMMARY

    if OBJECT_EXISTENCE_REGEX.match(ql):
        return QuestionType.OBJECT_EXISTENCE

    if OBJECT_EXISTENCE_ALT_REGEX.match(ql):
        return QuestionType.OBJECT_EXISTENCE_ALT

    if COUNT_CONTAINER_REGEX.match(ql):
        return QuestionType.COUNT_CONTAINER

    if COUNT_SPECIFIC_REGEX.match(ql):
        return QuestionType.COUNT_SPECIFIC

    if COUNT_IMPLICIT_REGEX.match(ql):
        return QuestionType.COUNT_IMPLICIT

    if MOVEMENT_REGEX.match(ql):
        return QuestionType.MOVEMENT

    if RELATION_REGEX.match(ql):
        return QuestionType.RELATION_EXISTENCE

    if POSITION_REGEX.match(ql):
        return QuestionType.POSITION

    if MONITOR_REGEX.match(ql):
        return QuestionType.MONITOR

    if PROPERTY_REGEX.match(ql):
        return QuestionType.PROPERTY

    return QuestionType.UNKNOWN


if __name__ == "__main__":
    print("\n========== SCENE QUESTION TEST REPORT ==========\n")

    total = 0
    passed = 0

    for expected_type, questions in ALL_TESTS.items():
        print(f"\n--- Testing {expected_type.value.upper()} ---")
        for q in questions:
            total += 1
            detected = detect_intent(q)
            ok = detected == expected_type
            passed += int(ok)

            status = "✅ PASS" if ok else "❌ FAIL"
            print(f"{status:<7} | {q:<50} → {detected.value}")

    print("\n==============================================")
    print(f"TOTAL: {total} | PASSED: {passed} | FAILED: {total - passed}")
    print("==============================================\n")
