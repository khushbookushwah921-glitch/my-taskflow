from backend.app.algorithms import (
    insertion_sort_count,
    binary_search_count,
    linear_search_count,
)


def make_records(size):
    records = []

    for i in range(size, 0, -1):
        records.append({
            "title": f"Task {i:05d}",
            "priority": "high" if i % 3 == 0 else (
                "medium" if i % 3 == 1 else "low"
            ),
            "due_date": None
        })

    return records


sizes = [10, 500, 3000]

print("TaskFlow Algorithm Benchmark")
print("=" * 60)

for size in sizes:
    records = make_records(size)

    # Insertion sort benchmark
    insertion_records = [record.copy() for record in records]
    insertion_count = insertion_sort_count(
        insertion_records,
        "title"
    )

    # Binary search benchmark
    binary_records = [record.copy() for record in insertion_records]
    binary_result = binary_search_count(
        binary_records,
        f"Task {size // 2:05d}",
        "title"
    )

    # Linear search benchmark
    linear_records = [record.copy() for record in records]
    linear_result = linear_search_count(
        linear_records,
        f"Task {size // 2:05d}",
        "title"
    )

    print(f"\nData size: {size}")
    print(f"Insertion sort comparisons: {insertion_count}")
    print(
        f"Binary search comparisons: "
        f"{binary_result['comparison_count']}"
    )
    print(
        f"Linear search comparisons: "
        f"{linear_result['comparison_count']}"
    )

print("\nBenchmark completed.")