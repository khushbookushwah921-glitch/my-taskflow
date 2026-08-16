from backend.algorithms import (
    insertion_sort,
    binary_search,
    linear_search,
    insertion_sort_count,
    binary_search_count,
    linear_search_count
)


def check(case_name, result, expected):
    if result == expected:
        print(f"PASS: {case_name}")
    else:
        print(f"FAIL: {case_name} — expected {expected}, got {result}")


# 1. Empty list
records = []
insertion_sort(records, "title")
check(
    "Insertion sort empty list",
    records,
    []
)


# 2. Single element
records = [{"title": "Task A"}]
insertion_sort(records, "title")
check(
    "Insertion sort single element",
    records,
    [{"title": "Task A"}]
)


# 3. Sort normal list
records = [
    {"title": "Charlie"},
    {"title": "Alpha"},
    {"title": "Bravo"}
]

insertion_sort(records, "title")

check(
    "Insertion sort correctly sorts",
    records,
    [
        {"title": "Alpha"},
        {"title": "Bravo"},
        {"title": "Charlie"}
    ]
)


# Sorted list for binary search
sorted_records = [
    {"title": "Alpha"},
    {"title": "Bravo"},
    {"title": "Charlie"},
    {"title": "Delta"},
    {"title": "Echo"}
]


# 4. Binary search first
result = binary_search(sorted_records, "Alpha", "title")
check(
    "Binary search first index",
    result,
    0
)


# 5. Binary search middle
result = binary_search(sorted_records, "Charlie", "title")
check(
    "Binary search middle index",
    result,
    2
)


# 6. Binary search last
result = binary_search(sorted_records, "Echo", "title")
check(
    "Binary search last index",
    result,
    4
)


# 7. Binary search not found
result = binary_search(sorted_records, "Zebra", "title")
check(
    "Binary search not found",
    result,
    -1
)


# 8. Insertion sort count
records = [
    {"title": "Charlie"},
    {"title": "Alpha"},
    {"title": "Bravo"}
]

count = insertion_sort_count(records, "title")

if (
    records
    == [
        {"title": "Alpha"},
        {"title": "Bravo"},
        {"title": "Charlie"}
    ]
    and type(count) == int
    and count > 0
):
    print("PASS: Insertion sort count")
else:
    print(
        f"FAIL: Insertion sort count — "
        f"sorted={records}, count={count}"
    )


# 9. Binary search count
records = [
    {"title": "Alpha"},
    {"title": "Bravo"},
    {"title": "Charlie"},
    {"title": "Delta"},
    {"title": "Echo"}
]

result = binary_search_count(
    records,
    "Charlie",
    "title"
)

if (
    type(result) == dict
    and result["index"] == 2
    and type(result["comparison_count"]) == int
    and result["comparison_count"] > 0
):
    print("PASS: Binary search count")
else:
    print(
        f"FAIL: Binary search count — "
        f"expected index 2, got {result}"
    )


# 10. Linear search count - absent value
records = [
    {"title": "Alpha"},
    {"title": "Bravo"},
    {"title": "Charlie"},
    {"title": "Delta"}
]

result = linear_search_count(
    records,
    "Zebra",
    "title"
)

if (
    type(result) == dict
    and result["index"] == -1
    and result["comparison_count"] == len(records)
):
    print("PASS: Linear search count absent value")
else:
    print(
        f"FAIL: Linear search count absent value — "
        f"expected index -1 and comparisons {len(records)}, "
        f"got {result}"
    )