import re


PRIORITY_KEYWORDS = [
    "urgent",
    "asap",
    "whenever",
    "low priority",
]

DATE_PHRASES = [
    "today",
    "tomorrow",
    "next week",
    "next monday",
    "next tuesday",
    "next wednesday",
    "next thursday",
    "next friday",
    "next saturday",
    "next sunday",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]


def parse_quick_add(description: str):
    original = description
    working = description.lower()

    # -------------------------
    # PRIORITY
    # -------------------------

    if "urgent" in working or "asap" in working:
        priority = "high"
    elif "whenever" in working or "low priority" in working:
        priority = "low"
    else:
        priority = "medium"

    # -------------------------
    # DATE
    # -------------------------

    due_date_hint = None

    for phrase in DATE_PHRASES:
        if phrase in working:
            due_date_hint = phrase
            break

    # -------------------------
    # TITLE
    # -------------------------

    title = original

    # Remove ALL priority keywords
    for keyword in PRIORITY_KEYWORDS:
        title = re.sub(
            re.escape(keyword),
            "",
            title,
            flags=re.IGNORECASE
        )

    # Remove every occurrence of matched date phrase
    if due_date_hint:
        title = re.sub(
            re.escape(due_date_hint),
            "",
            title,
            flags=re.IGNORECASE
        )

    title = title.strip()

    if not title:
        title = "Untitled task"

    return {
        "title": title,
        "priority": priority,
        "due_date_hint": due_date_hint,
    }