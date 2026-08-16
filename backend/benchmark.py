from app.algorithms import (
    insertion_sort_count,
    binary_search_count,
    linear_search_count
)


def generate_records(size):
    records = []

    for i in range(size, 0, -1):
        records.append({
            "title": f"Task {i:05d}",
            "priority": "medium",
            "due_date": None
        })

    return records


sizes = [10, 500, 3000]

print("\nTaskFlow Algorithm Benchmark")
print("=" * 60)

for size in sizes:
    print(f"\nDATA SIZE: {size}")
    print("-" * 60)

    # -------------------------
    # Insertion Sort
    # -------------------------
    records = generate_records(size)

    insertion_comparisons = insertion_sort_count(
        records,
        "title"
    )

    print(
        f"Insertion Sort comparisons: "
        f"{insertion_comparisons}"
    )

    # -------------------------
    # Binary Search
    # -------------------------
    # records are already sorted
    target = f"Task {size // 2:05d}"

    binary_result = binary_search_count(
        records,
        target,
        "title"
    )

    print(
        f"Binary Search: "
        f"index={binary_result['index']}, "
        f"comparisons={binary_result['comparison_count']}"
    )

    # -------------------------
    # Linear Search
    # -------------------------
    linear_result = linear_search_count(
        records,
        target,
        "title"
    )

    print(
        f"Linear Search: "
        f"index={linear_result['index']}, "
        f"comparisons={linear_result['comparison_count']}"
    )

print("\nBenchmark completed successfully.")