from toffee.agent import Agent

from ..bundle import UpdateBundle

__all__ = ['TrainAgent']


class TrainAgent(Agent):
    def __init__(self, bundle: UpdateBundle):
        super().__init__(bundle.step)
        bundle.set_all(0)
        self.io_update = bundle

    async def exec_update(self, pc: int, br_slot_valid, tail_slot_valid,
                          tail_slot_sharing, meta: int, fgh: int,
                          br_taken_mask_0, br_taken_mask_1,
                          mispred_mask_0, mispred_mask_1,
                          strong_bias_0, strong_bias_1) -> None:
        update_dict = {
            'pc': pc,
            'meta': meta,
            'br_taken_mask_0': br_taken_mask_0,
            'br_taken_mask_1': br_taken_mask_1,
            'mispred_mask_0': mispred_mask_0,
            'mispred_mask_1': mispred_mask_1,
            'ghist': fgh,
            'ftb_entry': {
                'strong_bias_0': strong_bias_0,
                'strong_bias_1': strong_bias_1,
                'br_slot': {'valid': br_slot_valid},
                'tail_slot': {'valid': tail_slot_valid, 'sharing': tail_slot_sharing},
            },
        }
        self.io_update.assign({"valid": True, "bits": update_dict})
        await self.io_update.step(1)
        self.io_update.valid.value = 0
        await self.io_update.step(3)
        self.io_update.set_all(0)
