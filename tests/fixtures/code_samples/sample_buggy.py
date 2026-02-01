"""
Buggy Data Processing Module

This code contains INTENTIONAL logic bugs for testing code review evaluators.
DO NOT use this code in production!

Expected evaluator verdict: CHANGES_REQUESTED
Expected findings:
- Off-by-one errors
- Null/None handling issues
- Resource leaks
- Race conditions
- Incorrect boundary conditions
- Type confusion
- Infinite loops potential
"""

import threading
import time
from typing import Optional


class DataProcessor:
    """Processes data with various logic bugs."""

    def __init__(self):
        self.data = []
        self.cache = {}
        self._lock = threading.Lock()
        self._processing = False

    def process_range(self, items: list, start: int, end: int) -> list:
        """
        Process a range of items.

        BUG: Off-by-one error - excludes the last item
        """
        results = []
        # BUG: Should be range(start, end + 1) or range(start, end) depending on intent
        # The end parameter is ambiguous - is it inclusive or exclusive?
        for i in range(start, end):  # BUG: Off-by-one if end is meant to be inclusive
            if i < len(items):
                results.append(items[i] * 2)
        return results

    def find_max(self, numbers: list) -> Optional[int]:
        """
        Find the maximum number in a list.

        BUG: Doesn't handle empty list correctly
        BUG: Initialization with 0 fails for all-negative lists
        """
        # BUG: Returns 0 for empty list instead of None or raising exception
        # BUG: max_val = 0 means negative-only lists return 0
        max_val = 0
        for num in numbers:
            if num > max_val:
                max_val = num
        return max_val

    def calculate_average(self, numbers: list) -> float:
        """
        Calculate the average of a list of numbers.

        BUG: Division by zero when list is empty
        BUG: Integer division in Python 2 style (though Python 3 handles this)
        """
        total = 0
        for num in numbers:
            total += num
        # BUG: ZeroDivisionError if numbers is empty
        return total / len(numbers)

    def get_item_safely(self, items: list, index: int):
        """
        Get an item from a list safely.

        BUG: Negative index handling is incorrect
        BUG: Returns None silently instead of raising or logging
        """
        # BUG: Doesn't handle negative indices correctly
        # Python allows negative indices, but this check doesn't account for them
        if index < len(items):  # BUG: Should also check index >= 0 or handle negatives
            return items[index]
        return None

    def merge_dicts(self, dict1: dict, dict2: dict) -> dict:
        """
        Merge two dictionaries.

        BUG: Modifies the original dict1
        """
        # BUG: This modifies dict1 in place, which is unexpected
        for key, value in dict2.items():
            dict1[key] = value
        return dict1

    def process_user_data(self, user: dict) -> dict:
        """
        Process user data.

        BUG: Doesn't handle missing keys
        BUG: Type assumption on 'age' field
        """
        # BUG: KeyError if 'name' or 'age' don't exist
        processed = {
            "full_name": user["name"].upper(),  # BUG: KeyError if 'name' missing
            "birth_year": 2024 - user["age"],  # BUG: KeyError if 'age' missing, TypeError if not int
            "active": user["status"] == "active",  # BUG: KeyError if 'status' missing
        }
        return processed

    def read_file_lines(self, filepath: str) -> list:
        """
        Read lines from a file.

        BUG: File handle never closed (resource leak)
        """
        # BUG: Resource leak - file is never closed
        f = open(filepath, "r")
        lines = f.readlines()
        # BUG: Missing f.close() or context manager
        return lines

    def write_data(self, filepath: str, data: str) -> bool:
        """
        Write data to a file.

        BUG: Resource leak on exception
        BUG: Swallows exceptions silently
        """
        try:
            f = open(filepath, "w")
            f.write(data)
            f.close()
            return True
        except Exception:
            # BUG: Exception swallowed, file handle leaked if exception occurs after open
            return False

    def parse_number(self, value: str) -> int:
        """
        Parse a string to a number.

        BUG: Doesn't handle non-numeric strings
        BUG: Truncates floats unexpectedly
        """
        # BUG: ValueError if value is not a valid number
        # BUG: int("3.14") raises ValueError, should use float() first if floats expected
        return int(value)

    def search_items(self, items: list, target) -> int:
        """
        Search for an item and return its index.

        BUG: Returns 0 for not found (ambiguous with first item)
        BUG: Breaks on first match, but docstring doesn't specify behavior
        """
        index = 0  # BUG: 0 is also a valid index, can't distinguish from "not found"
        for i, item in enumerate(items):
            if item == target:
                index = i
                break
        return index

    def paginate(self, items: list, page: int, page_size: int) -> list:
        """
        Paginate a list of items.

        BUG: Negative page number not handled
        BUG: Off-by-one in page calculation
        """
        # BUG: page=0 and page=1 return the same result (off-by-one)
        start = page * page_size  # BUG: Should be (page - 1) * page_size for 1-indexed pages
        end = start + page_size
        return items[start:end]

    def increment_counter(self, counter_name: str) -> int:
        """
        Increment a named counter.

        BUG: Race condition in read-modify-write
        """
        # BUG: Race condition - not atomic
        if counter_name not in self.cache:
            self.cache[counter_name] = 0
        current = self.cache[counter_name]
        # BUG: Another thread could modify cache[counter_name] between read and write
        time.sleep(0.001)  # Simulates processing, makes race condition more likely
        self.cache[counter_name] = current + 1
        return self.cache[counter_name]

    def safe_increment(self, counter_name: str) -> int:
        """
        Safely increment a counter with locking.

        BUG: Deadlock potential if called recursively
        BUG: Lock not released on exception
        """
        self._lock.acquire()  # BUG: Should use 'with self._lock:' for safety
        if counter_name not in self.cache:
            self.cache[counter_name] = 0
        self.cache[counter_name] += 1
        result = self.cache[counter_name]
        self._lock.release()  # BUG: Not released if exception occurs above
        return result

    def process_batch(self, items: list, batch_size: int):
        """
        Process items in batches.

        BUG: Infinite loop if batch_size <= 0
        BUG: Misses last batch if not evenly divisible
        """
        processed = []
        i = 0
        # BUG: Infinite loop if batch_size is 0 or negative
        while i < len(items):
            batch = items[i : i + batch_size]
            processed.extend([x * 2 for x in batch])
            i += batch_size

        return processed  # BUG: Actually this works, but batch_size <= 0 causes infinite loop

    def compare_floats(self, a: float, b: float) -> bool:
        """
        Compare two floating point numbers.

        BUG: Direct float comparison is unreliable
        """
        # BUG: Float comparison with == is unreliable due to precision
        return a == b  # BUG: 0.1 + 0.2 == 0.3 returns False

    def validate_age(self, age) -> bool:
        """
        Validate that age is reasonable.

        BUG: Type coercion issues
        BUG: Boundary conditions wrong
        """
        # BUG: "25" (string) passes the comparison due to type coercion in some contexts
        # BUG: age of 0 might be valid for newborns
        # BUG: Upper bound of 150 is arbitrary but not documented
        return age > 0 and age < 150  # BUG: Should be >= 0 for newborns

    def remove_duplicates(self, items: list) -> list:
        """
        Remove duplicates while preserving order.

        BUG: Doesn't preserve order (set is unordered in Python < 3.7)
        BUG: Fails for unhashable items
        """
        # BUG: set() doesn't preserve order in older Python versions
        # BUG: Raises TypeError for unhashable items (like dicts or lists)
        return list(set(items))

    def filter_none_values(self, items: list) -> list:
        """
        Filter out None values from a list.

        BUG: Also filters out 0, empty string, and False (falsy values)
        """
        # BUG: Filters all falsy values, not just None
        return [item for item in items if item]  # BUG: Should be 'if item is not None'
