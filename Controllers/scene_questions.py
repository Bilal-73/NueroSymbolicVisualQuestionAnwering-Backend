import re
from enum import Enum

# =========================
# Question Categories
# =========================
class QuestionType(Enum):
    SUMMARY = "summary"
    OBJECT_EXISTENCE = "object_existence"
    MOVEMENT = "movement"
    RELATION_EXISTENCE = "relation_existence"
    RELATION_COUNT = "relation_count"
    PROPERTY = "property"
    UNKNOWN = "unknown"


# =========================
# Supported Relations
# =========================
RELATIONS = ["left of", "right of", "below", "near", "on","in front of","behind"]
REL_PATTERN = "|".join(map(re.escape, RELATIONS))


# =========================
# Regex Expressions
# =========================

SUMMARY_QUESTIONS = {
    "what is in front of me?": QuestionType.SUMMARY,
    "tell me how many objects are present?": QuestionType.SUMMARY,
    "can you tell me what objects are here?": QuestionType.SUMMARY
}
# =========================
# Counting Regexes
# =========================

# "How many <obj> are there?" / "How many <obj> present?"
COUNT_SPECIFIC_REGEX = re.compile(
    r"""^how\s+many\s+(?P<obj>[\w\s]+?)(?:s)?
        \s+are\s+(there|present)
        (?:\s+in\s+the\s+scene)?
        \??$""",
    re.IGNORECASE | re.VERBOSE
)

# "How many <obj> are in/on the <container>?"
COUNT_CONTAINER_REGEX = re.compile(
    r"""^how\s+many\s+(?P<obj>[\w\s]+?)(?:s)?
        \s+are\s+(?P<prep>in|on|there\s+in)
        \s+(the\s+)?(?P<container>[\w\s]+)
        \??$""",
    re.IGNORECASE | re.VERBOSE
)

OBJECT_EXISTENCE_REGEX = re.compile(
    r"^is there a (?P<obj>\w+)\?$",
    re.IGNORECASE
)

MOVEMENT_REGEX = re.compile(
    rf"""^tell\s+me\s+if\s+(?P<obj>\w+)
        (?:\s+in\s+center)?
        \s+(?P<action>leave|leaves|left|come|comes|enter|enters)
        (?:\s+the\s+room)?
        \s*[\?\.\!]?$""",
    re.IGNORECASE | re.VERBOSE
)


RELATION_EXISTENCE_REGEX = re.compile(
    rf"""^is\s+(there\s+)?anything\s+
        (?P<relation>{REL_PATTERN})\s+
        (?P<object>[\w\s]+)\?$""",
    re.IGNORECASE | re.VERBOSE
)


RELATION_COUNT_REGEX = re.compile(
    rf"""^how\s+many\s+objects\s+
        (?P<relation>{REL_PATTERN})\s+
        (?P<object>[\w\s]+)\?$""",
    re.IGNORECASE | re.VERBOSE
)

PROPERTY_REGEX = re.compile(
    r"^(tell me|what is the)\s+(?P<prop>\w+)\s+of\s+(?P<obj>\w+)\?$",
    re.IGNORECASE
)

OBJECT_EXISTENCE_ALT_REGEX = re.compile(
    r"""^(do\s+you\s+see|is\s+any|can\s+you\s+find)
        \s+(a|any)?\s*(?P<obj>\w+)
        (\s+present)?\??$""",
    re.IGNORECASE | re.VERBOSE
)

EMOTIONS = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]

EMOTION_PATTERN = "|".join(EMOTIONS)

EMOTION_YN_REGEX = re.compile(
    rf"""^(
        is\s+(the\s+)?(?P<obj1>\w+)\s+(?P<emo1>{EMOTION_PATTERN}) |

        does\s+(the\s+)?(?P<obj2>\w+)\s+(look|seem)\s+(?P<emo2>{EMOTION_PATTERN}) |

        is\s+(the\s+)?(?P<obj3>\w+)\s+looking\s+(?P<emo3>{EMOTION_PATTERN}) |

        is\s+(the\s+)?(?P<obj4>\w+)\s+in\s+(a\s+)?(?P<emo4>{EMOTION_PATTERN})\s+mood
    )\??$""",
    re.IGNORECASE | re.VERBOSE
)


# =========================
# Human-Readable Catalog
# =========================
# QUESTION_CATALOG = {
#     QuestionType.SUMMARY: [
#         "What is in front of me?",
#         "Tell me how many objects are present?",
#         "Can you tell me what objects are here?"
#     ],
#     QuestionType.OBJECT_EXISTENCE: [
#         "Is there a <object>?"
#     ],
#     QuestionType.MOVEMENT: [
#         "Tell me if <object> enters the room",
#         "Tell me if <object> leaves the room"
#     ],
#     QuestionType.RELATION_EXISTENCE: [
#         "Is there anything <relation> <object>?"
#     ],
#     QuestionType.RELATION_COUNT: [
#         "How many objects <relation> <object>?"
#     ],
#     QuestionType.PROPERTY: [
#         "What is the <property> of <object>?",
#         "Tell me <property> of <object>?"
#     ]
# }



# import re
# from enum import Enum
#
# # =========================
# # Question Categories
# # =========================
# class QuestionType(Enum):
#     SUMMARY = "summary"
#     OBJECT_EXISTENCE = "object_existence"
#     OBJECT_EXISTENCE_ALT = "object_existence_alt"
#     MOVEMENT = "movement"
#     RELATION_EXISTENCE = "relation_existence"
#     RELATION_COUNT = "relation_count"
#     COUNT_SPECIFIC = "count_specific"
#     COUNT_CONTAINER = "count_container"
#     COUNT_IMPLICIT = "count_implicit"
#     PROPERTY = "property"
#     POSITION = "position"
#     MONITOR = "monitor"
#     UNKNOWN = "unknown"
#
#
# # =========================
# # Constants
# # =========================
# RELATIONS = ["left of", "right of", "above", "below", "near"]
# REL_PATTERN = "|".join(map(re.escape, RELATIONS))
#
# POSITIONS = ["center", "top left", "top right", "bottom left", "bottom right"]
# POS_PATTERN = "|".join(map(re.escape, POSITIONS))
#
#
# # =========================
# # Exact Summary Questions
# # =========================
# SUMMARY_QUESTIONS = {
#     "what is in front of me?": QuestionType.SUMMARY,
#     "tell me how many objects are present?": QuestionType.SUMMARY,
#     "can you tell me what objects are here?": QuestionType.SUMMARY
# }
#
#
# # =========================
# # Regex Expressions
# # =========================
#
# # --- Object existence (basic) ---
# OBJECT_EXISTENCE_REGEX = re.compile(
#     r"^is there a (?P<obj>\w+)\?$",
#     re.IGNORECASE
# )
#
# # --- Object existence (natural language) ---
# OBJECT_EXISTENCE_ALT_REGEX = re.compile(
#     r"""^(do\s+you\s+see|is\s+any|can\s+you\s+find)
#         \s+(a|any)?\s*(?P<obj>\w+)
#         (\s+present)?\??$""",
#     re.IGNORECASE | re.VERBOSE
# )
#
# # --- Movement ---
# MOVEMENT_REGEX = re.compile(
#     r"""^tell\s+me\s+if\s+(?P<obj>\w+)
#         (?:\s+in\s+center)?
#         \s+(?P<action>leave|leaves|left|come|comes|enter|enters)
#         (?:\s+the\s+room)?
#         \s*[\?\.\!]?$""",
#     re.IGNORECASE | re.VERBOSE
# )
#
# # --- Relations ---
# RELATION_REGEX = re.compile(
#     rf"""^(
#         is\s+(there\s+)?anything\s+(?P<rel1>{REL_PATTERN})\s+(?P<obj1>\w+)\? |
#         how\s+many\s+objects\s+(?P<rel2>{REL_PATTERN})\s+(?P<obj2>\w+)\?
#     )$""",
#     re.IGNORECASE | re.VERBOSE
# )
#
# # --- Properties ---
# PROPERTY_REGEX = re.compile(
#     r"^(tell me|what is the)\s+(?P<prop>\w+)\s+of\s+(?P<obj>\w+)\?$",
#     re.IGNORECASE
# )
#
# # --- Counting (explicit) ---
# COUNT_SPECIFIC_REGEX = re.compile(
#     r"""^how\s+many\s+(?P<obj>[\w\s]+?)(?:s)?
#         \s+are\s+(there|present)
#         (?:\s+in\s+the\s+scene)?
#         \??$""",
#     re.IGNORECASE | re.VERBOSE
# )
#
# # --- Counting (container-based) ---
# COUNT_CONTAINER_REGEX = re.compile(
#     r"""^how\s+many\s+(?P<obj>[\w\s]+?)(?:s)?
#         \s+are\s+(?P<prep>in|on|there\s+in)
#         \s+(the\s+)?(?P<container>[\w\s]+)
#         \??$""",
#     re.IGNORECASE | re.VERBOSE
# )
#
# # --- Counting (implicit / short) ---
# COUNT_IMPLICIT_REGEX = re.compile(
#     r"""^(count|number\s+of)\s+(the\s+)?(?P<obj>[\w\s]+)\??$""",
#     re.IGNORECASE | re.VERBOSE
# )
#
# # --- Position questions ---
# POSITION_REGEX = re.compile(
#     rf"""^(
#         is\s+the\s+(?P<obj1>\w+)\s+in\s+the\s+(?P<pos1>{POS_PATTERN}) |
#         what\s+objects\s+are\s+in\s+the\s+(?P<pos2>{POS_PATTERN})
#     )\??$""",
#     re.IGNORECASE | re.VERBOSE
# )
#
# # --- Monitoring / Event ---
# MONITOR_REGEX = re.compile(
#     r"""^(notify\s+me\s+when|alert\s+me\s+if)
#         \s+(a\s+)?(?P<obj>\w+)\s+
#         (?P<action>enters|leaves|comes|goes)
#     $""",
#     re.IGNORECASE | re.VERBOSE
# )
# EMOTIONS = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
#
# EMOTION_PATTERN = "|".join(EMOTIONS)
#
# EMOTION_YN_REGEX = re.compile(
#     rf"""^(
#         is\s+(the\s+)?(?P<obj1>\w+)\s+(?P<emo1>{EMOTION_PATTERN}) |
#
#         does\s+(the\s+)?(?P<obj2>\w+)\s+(look|seem)\s+(?P<emo2>{EMOTION_PATTERN}) |
#
#         is\s+(the\s+)?(?P<obj3>\w+)\s+looking\s+(?P<emo3>{EMOTION_PATTERN}) |
#
#         is\s+(the\s+)?(?P<obj4>\w+)\s+in\s+(a\s+)?(?P<emo4>{EMOTION_PATTERN})\s+mood
#     )\??$""",
#     re.IGNORECASE | re.VERBOSE
# )