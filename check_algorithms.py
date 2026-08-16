from backend.app.algorithms import (
    insertion_sort,
    binary_search,
    linear_search,
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
records = [{"title": "Only"}]
insertion_sort(records, "title")
check(
    "insertion_sort single element",
    records,
    [{"title": "Only"}]
)


# 3. Binary search - first
records = [
    {"title": "Alpha"},
    {"title": "Beta"},
    {"title": "Gamma"},
]
check(
    "binary_search first index",
    binary_search(records, "Alpha", "title"),
    0
)


# 4. Binary search - middle
check(
    "binary_search middle index",
    binary_search(records, "Beta", "title"),
    1
)


# 5. Binary search - last
check(
    "binary_search last index",
    binary_search(records, "Gamma", "title"),
    2
)


# 6. Binary search - absent
check(
    "binary_search not found",
    binary_search(records, "Delta", "title"),
    -1
)


# 7. insertion_sort_count
records = [
    {"title": "C"},
    {"title": "A"},
    {"title": "B"},
]

count = insertion_sort_count(records, "title")

if records == [
    {"title": "A"},
    {"title": "B"},
    {"title": "C"},
] and type(count) == int and count > 0:
    print("PASS: insertion_sort_count")
else:
    print(
        f"FAIL: insertion_sort_count — "
        f"sorted={records}, count={count}"
    )


# 8. binary_search_count
records = [
    {"title": "Alpha"},
    {"title": "Beta"},
    {"title": "Gamma"},
]

result = binary_search_count(records, "Beta", "title")

if (
    isinstance(result, dict)
    and result.get("index") == 1
    and type(result.get("comparison_count")) == int
    and result.get("comparison_count") > 0
):
    print("PASS: binary_search_count")
else:
    print(f"FAIL: binary_search_count — got {result}")


# 9. linear_search_count absent
records = [
    {"title": "Alpha"},
    {"title": "Beta"},
    {"title": "Gamma"},
]

result = linear_search_count(records, "Delta", "title")

if (
    isinstance(result, dict)
    and result.get("index") == -1
    and result.get("comparison_count") == len(records)
):
    print("PASS: linear_search_count")
else:
    print(f"FAIL: linear_search_count — got {result}")


print("\nAlgorithm checks completed.")