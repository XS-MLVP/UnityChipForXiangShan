import math
from typing import Self
FTQSIZE = 64
def is_pow2(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0

def log2_up(n: int) -> int:
    return max(1, n.bit_length())

class CircularQueuePtr:
    def __init__(self, entries = FTQSIZE, flag: bool = False, value: int = 0):
        if entries <= 0:
            raise ValueError("entries must be positive")
        if not (0 <= value < entries):
            raise ValueError(f"value {value} out of range [0, {entries})")
        self.entries = entries
        self.flag = bool(flag)
        self.value = value

    def __repr__(self):
        return f"CircularQueuePtr(entries={self.entries}, flag={self.flag}, value={self.value})"

    def __eq__(self, other: 'CircularQueuePtr') -> bool:
        if not isinstance(other, CircularQueuePtr):
            return False
        return self.entries == other.entries and self.flag == other.flag and self.value == other.value

    def __ne__(self, other: 'CircularQueuePtr') -> bool:
        return not self.__eq__(other)

    def __add__(self, v: int) -> 'CircularQueuePtr':
        if v < 0:
            raise ValueError("v must be non-negative")

        entries = self.entries

        if is_pow2(entries):
            value_width = entries.bit_length() - 1
            ptr_width = value_width + 1

            mask = (1 << ptr_width) - 1

            combined = ((1 if self.flag else 0) << value_width) | self.value

            new_combined = (combined + v) & mask

            new_flag = bool(new_combined >> value_width)
            new_value = new_combined & (entries - 1)

            return CircularQueuePtr(entries, new_flag, new_value)

        else:
            new_value_raw = self.value + v
            wraps = new_value_raw // entries
            new_value = new_value_raw % entries
            new_flag = self.flag ^ (wraps % 2 == 1)
            return CircularQueuePtr(entries, new_flag, new_value)


    def __sub__(self, v: int) -> 'CircularQueuePtr':
        if v < 0:
            raise ValueError("v must be non-negative")
        # Equivalent to: self + (entries - v % entries), then flip flag
        entries = self.entries
        v_mod = v % entries
        if v_mod == 0:
            # Subtracting multiple of entries: flip flag twice? Actually, net zero change in position, but we follow Chisel
            # Chisel does: self + (entries - v), then flip result.flag
            temp = self + (entries - v_mod)
        else:
            temp = self + (entries - v_mod)
        # Flip flag
        return CircularQueuePtr(entries, not temp.flag, temp.value)

    def __gt__(self, other: 'CircularQueuePtr') -> bool:
        if self.entries != other.entries:
            raise ValueError("Can't compare pointers with different entries")
        different_flag = self.flag != other.flag
        value_compare = self.value > other.value
        return different_flag != value_compare  # XOR

    def __lt__(self, other: 'CircularQueuePtr') -> bool:
        if self.entries != other.entries:
            raise ValueError("Can't compare pointers with different entries")
        different_flag = self.flag != other.flag
        value_compare = self.value < other.value
        return different_flag != value_compare

    def __ge__(self, other: 'CircularQueuePtr') -> bool:
        return self > other or self == other

    def __le__(self, other: 'CircularQueuePtr') -> bool:
        return self < other or self == other

    def clone(self) -> 'CircularQueuePtr':
        return CircularQueuePtr(self.entries, self.flag, self.value)


# Helper functions (equivalent to HasCircularQueuePtrHelper)
def is_empty(enq_ptr: CircularQueuePtr, deq_ptr: CircularQueuePtr) -> bool:
    return enq_ptr == deq_ptr

def is_full(enq_ptr: CircularQueuePtr, deq_ptr: CircularQueuePtr) -> bool:
    return (enq_ptr.flag != deq_ptr.flag) and (enq_ptr.value == deq_ptr.value)

def distance_between(enq_ptr: CircularQueuePtr, deq_ptr: CircularQueuePtr) -> int:
    if enq_ptr.entries != deq_ptr.entries:
        raise ValueError("Pointers must have same entries")
    entries = enq_ptr.entries
    if enq_ptr.flag == deq_ptr.flag:
        return enq_ptr.value - deq_ptr.value
    else:
        return entries + enq_ptr.value - deq_ptr.value

def has_free_entries(enq_ptr: CircularQueuePtr, deq_ptr: CircularQueuePtr) -> int:
    used = distance_between(enq_ptr, deq_ptr)
    return enq_ptr.entries - used

def is_after(left: CircularQueuePtr, right: CircularQueuePtr) -> bool:
    return left > right

def is_before(left: CircularQueuePtr, right: CircularQueuePtr) -> bool:
    return left < right

# # --- Example usage / test ---
# if __name__ == "__main__":
#     entries = 5  # non-power-of-two example

#     # Start: empty queue
#     enq = CircularQueuePtr(entries, False, 0)
#     deq = CircularQueuePtr(entries, False, 0)

#     print("Empty?", is_empty(enq, deq))  # True
#     print("Full?", is_full(enq, deq))    # False
#     print("Distance:", distance_between(enq, deq))  # 0

#     # Enqueue 3 items
#     enq = enq + 3
#     print("After enq+3:", enq)  # flag=False, value=3
#     print("Distance:", distance_between(enq, deq))  # 3
#     print("Free:", has_free_entries(enq, deq))      # 2

#     # Enqueue 2 more → full
#     enq = enq + 2
#     print("After enq+2:", enq)  # flag=True, value=0 (wrapped)
#     print("Full?", is_full(enq, deq))               # True (flag ≠, value == 0)
#     print("Distance:", distance_between(enq, deq))  # 5

#     # Dequeue 1
#     deq = deq + 1
#     print("After deq+1:", deq)  # flag=False, value=1
#     print("Distance:", distance_between(enq, deq))  # 5 + 0 - 1 = 4

#     # Test comparison
#     p1 = CircularQueuePtr(4, False, 3)
#     p2 = CircularQueuePtr(4, True, 0)
#     print("p1 > p2?", p1 > p2)  # True (p1 wrapped less than p2 which just wrapped)

#     # Power-of-two case
#     entries2 = 4
#     a = CircularQueuePtr(entries2, False, 3)
#     b = a + 1
#     print("a+1 (pow2):", b)  # flag=True, value=0