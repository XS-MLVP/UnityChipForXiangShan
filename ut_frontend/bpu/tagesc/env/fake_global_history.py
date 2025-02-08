__all__ = ["FakeGlobalHistory"]

GLOBAL_HISTORY_LEN = 256
GLOBAL_HISTORY_MASK = (1 << GLOBAL_HISTORY_LEN) - 1


class FakeGlobalHistory:
    def __init__(self, init_val: int = 0):
        self.value = init_val

    def update(self, taken: bool) -> None:
        g = self.value
        self.value = ((g << 1) | taken) & GLOBAL_HISTORY_MASK

    @staticmethod
    def calc_fh(full_hist: int, folded_len: int, hist_len: int) -> int:
        if folded_len == 0:
            return 0
        res = 0
        g = full_hist & ((1 << hist_len) - 1)
        mask = (1 << folded_len) - 1
        for _ in range(0, min(GLOBAL_HISTORY_LEN, hist_len), folded_len):
            res ^= g & mask
            g >>= folded_len

        return res

    def get_fh(self, folded_len: int, hist_len: int) -> int:
        return self.calc_fh(self.value, folded_len, hist_len)
