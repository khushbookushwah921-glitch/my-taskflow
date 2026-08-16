from app.algorithms import (
    insertion_sort,
    binary_search,
    insertion_sort_count,
    binary_search_count,
    linear_search_count,
)


def check(case_name, result, expected):
    if result == expected:
        print(f"PASS: {case_name}")
    else:
        print(f"FAIL: {case_name} — expected {expected}, got {result}")


# 1. Empty list
records = []
insertion_sort(records, "title")
check("insertion_sort empty list", records, [])


# 2. Single element
records = [{"title": "Task A"}]
insertion_sort(records, "title")
check(
    "insertion_sort single element",
    records,
    [{"title": "Task A"}]
)


# 3. Binary search first
records = [
    {"title": "Alpha"},
    {"title": "Beta"},
    {"title": "Gamma"},
]
check(
    "binary_search first",
    binary_search(records, "Alpha", "title"),
    0
)


# 4. Binary search last
check(
    "binary_search last",
    binary_search(records, "Gamma", "title"),
    2
)


# 5. Binary search middle
check(
    "binary_search middle",
    binary_search(records, "Beta", "title"),
    1
)


# 6. Binary search not found
check(
    "binary_search not found",
    binary_search(records, "Delta", "title"),
    -1
)


# 7. Insertion sort count
records = [
    {"title": "Charlie"},
    {"title": "Alpha"},
    {"title": "Beta"},
]

count = insertion_sort_count(records, "title")

expected_sorted = [
    {"title": "Alpha"},
    {"title": "Beta"},
    {"title": "Charlie"},
]

if records == expected_sorted and type(count) == int and count > 0:
    print("PASS: insertion_sort_count")
else:
    print(
        f"FAIL: insertion_sort_count — "
        f"expected sorted list and positive int, got {records}, {count}"
    )


# 8. Binary search count
records = [
    {"title": "Alpha"},
    {"title": "Beta"},
    {"title": "Charlie"},
    {"title": "Delta"},
    {"title": "Echo"},
]

result = binary_search_count(records, "Charlie", "title")

if (
    type(result) == dict
    and result["index"] == 2
    and type(result["comparison_count"]) == int
    and result["comparison_count"] > 0
):
    print("PASS: binary_search_count")
else:
    print(
        f"FAIL: binary_search_count — "
        f"expected index 2 and positive comparison count, got {result}"
    )


# 9. Linear search count - absent value
records = [
    {"title": "Alpha"},
    {"title": "Beta"},
    {"title": "Charlie"},
    {"title": "Delta"},
]

result = linear_search_count(records, "Not Found", "title")

if (
    type(result) == dict
    and result["index"] == -1
    and result["comparison_count"] == len(records)
):
    print("PASS: linear_search_count")
else:
    print(
        f"FAIL: linear_search_count — "
        f"expected index -1 and comparison count {len(records)}, "
        f"got {result}"
    )