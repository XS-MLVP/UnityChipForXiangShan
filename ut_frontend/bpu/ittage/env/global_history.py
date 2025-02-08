__all__ = ["GlobalHistory"]

GLOBAL_HISTORY_LEN = 256
GLOBAL_HISTORY_MASK = (1 << GLOBAL_HISTORY_LEN) - 1


class GlobalHistory:
    def __init__(self, init_val: int = 0, gh_len: int = GLOBAL_HISTORY_LEN):
        self.value = init_val
        self._len = gh_len

    def update(self, taken: bool) -> None:
        g = self.value
        self.value = (g << 1) | taken & GLOBAL_HISTORY_MASK

    def get_fh(self, folded_len: int, hist_len: int) -> int:
        if folded_len == 0:
            return 0
        res = 0
        g = self.value & ((1 << hist_len) - 1)
        mask = (1 << folded_len) - 1
        for _ in range(0, min(self._len, hist_len), folded_len):
            res ^= g & mask
            g >>= folded_len

        return res