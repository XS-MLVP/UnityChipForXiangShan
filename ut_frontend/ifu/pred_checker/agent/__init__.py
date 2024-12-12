from toffee.agent import *
from ..bundle import PredCheckerBundle,_13Bundle
from ... import PREDICT_WIDTH, RVC_LABEL, RET_LABEL, BRTYPE_LABEL

class PredCheckerAgent(Agent):
    def __init__(self, bundle: _13Bundle):
        super().__init__(bundle)
        self.bundle = bundle
        
    @driver_method()
    async def agent_pred_check(self, ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire):
        self.bundle.io._in._ftqOffset._valid.value = ftqValid
        self.bundle.io._in._ftqOffset._bits.value = ftqOffBits
        self.bundle.io._in._target.value = tgt
        self.bundle.io._in._fire_in.value = fire
        # print(self.bundle.io._in.ftqOffset_valid.value)
        print("binds_single_finished")
        # print(len(self.bundle.io._in.pc))
        for i in range(PREDICT_WIDTH):
            getattr(self.bundle.io._in._pc, f'_{i}').value = pc[i]
            getattr(self.bundle.io._in._instrRange, f'_{i}').value = instrRange[i]
            getattr(self.bundle.io._in._instrValid, f'_{i}').value = instrValid[i]
            getattr(self.bundle.io._in._jumpOffset, f'_{i}').value = jumpOffset[i]
            
            # pd = getattr(self.bundle.io._in, f'pds_{i}_')
            # pd = self.bundle.io._in.pds[i]
            getattr(self.bundle.io._in._pds, f'_{i}')._isRVC.value = pds[i][RVC_LABEL]
            getattr(self.bundle.io._in._pds, f'_{i}')._brType.value = pds[i][BRTYPE_LABEL]
            getattr(self.bundle.io._in._pds, f'_{i}')._isRet.value = pds[i][RET_LABEL]
            # print(pd.brType.value)
        await self.bundle.step(2)
        # await self.bundle.step()
        stg1_fixedRange = [getattr(self.bundle.io._out._stage1Out._fixedRange, f'_{i}').value for i in range(PREDICT_WIDTH)]
        stg1_fixedTaken = [getattr(self.bundle.io._out._stage1Out._fixedTaken, f'_{i}').value for i in range(PREDICT_WIDTH)]

        stg2_fixedTarget = [getattr(self.bundle.io._out._stage2Out._fixedTarget, f'_{i}').value for i in range(PREDICT_WIDTH)]
        stg2_fixedMissPred = [getattr(self.bundle.io._out._stage2Out._fixedMissPred, f'_{i}').value for i in range(PREDICT_WIDTH)]
        stg2_jalTarget = [getattr(self.bundle.io._out._stage2Out._jalTarget, f'_{i}').value for i in range(PREDICT_WIDTH)]

        return stg1_fixedRange, stg1_fixedTaken, \
                stg2_fixedTarget, stg2_jalTarget, stg2_fixedMissPred