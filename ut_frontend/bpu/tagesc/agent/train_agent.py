from toffee.agent import Agent

from ..bundle import UpdateBundle

__all__ = ['TrainAgent']


class TrainAgent(Agent):
    def __init__(self, bundle: UpdateBundle):
        super().__init__(bundle.step)
        bundle.set_all(0)
        self.io_update = bundle

    async def exec_update(self, pc: int, br_slot_valid: int | bool, tail_slot_valid: int | bool,
                          tail_slot_sharing: int | bool, meta: int, fgh: int,
                          br_taken_mask_0: int | bool, br_taken_mask_1: int | bool,
                          mispred_mask_0: int | bool, mispred_mask_1: int | bool,
                          always_taken_0: int | bool, always_taken_1: int | bool) -> None:
        update_dict = {
            'pc': pc,
            'meta': meta,
            'br_taken_mask_0': br_taken_mask_0,
            'br_taken_mask_1': br_taken_mask_1,
            'mispred_mask_0': mispred_mask_0,
            'mispred_mask_1': mispred_mask_1,
            'ghist': fgh,
            'ftb_entry': {
                'always_taken_0': always_taken_0,
                'always_taken_1': always_taken_1,
                'br_slot': {'valid': br_slot_valid},
                'tail_slot': {'valid': tail_slot_valid, 'sharing': tail_slot_sharing},
            },
        }
        self.io_update.assign({"valid": True, "bits": update_dict})
        await self.io_update.step(1)
        self.io_update.set_all(0)
        await self.io_update.step(3)
