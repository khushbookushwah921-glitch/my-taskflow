import re


def parse_quick_add(description: str):
    original = description
    text = description.lower()

    # -----------------------------
    # PRIORITY
    # -----------------------------

    if "urgent" in text or "asap" in text:
        priority = "high"
    elif "whenever" in text or "low priority" in text:
        priority = "low"
    else:
        priority = "medium"

    # -----------------------------
    # DUE DATE
    # -----------------------------

    due_date_hint = None

    date_phrases = [
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
    ]

    # First check the required phrases in exact order
    for phrase in date_phrases:
        if phrase in text:
            due_date_hint = phrase
            break

    # Bare weekday is checked only if no previous phrase matched
    if due_date_hint is None:
        weekdays = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]

        for day in weekdays:
            if day in text:
                due_date_hint = day
                break

    # -----------------------------
    # TITLE
    # -----------------------------

    title = original

    # Remove ALL priority keywords
    priority_keywords = [
        "urgent",
        "asap",
        "whenever",
        "low priority",
    ]

    for keyword in priority_keywords:
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
        "due_date_hint": due_date_hint
    }