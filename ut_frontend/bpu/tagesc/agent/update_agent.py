from toffee.agent import Agent

from ..bundle import BranchUpdateDriver

__all__ = ["UpdateAgent"]


class UpdateAgent(Agent):
    def __init__(self, driver: BranchUpdateDriver):
        super().__init__(driver)
        driver.set_all(0)
        self.driver = driver

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
        self.driver.assign({"valid": True, "bits": update_dict})
        await self.driver.step()
        self.driver.valid.value = 0
        await self.driver.step(3)
        self.driver.set_all(0)
