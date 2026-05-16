import re

# Example regex: count how many objects
COUNT_SPECIFIC_REGEX = re.compile(
    r"^how\s+many\s+(?P<obj>[\w\s]+?)(?:s)?\s+are\s+(there|present)\??$",
    re.IGNORECASE
)

# Example question
question = "How many chairs are there?"

# Test regex
match = COUNT_SPECIFIC_REGEX.match(question)

if match:
    print("Matched!")
    print("Captured object:", match.group("obj"))
else:
    print("No match.")
