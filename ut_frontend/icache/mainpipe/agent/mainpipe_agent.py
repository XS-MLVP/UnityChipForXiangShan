from toffee import Agent
from ..bundle import ICacheMainPipeBundle


class ICacheMainPipeAgent(Agent):
    def __init__(self, bundle: ICacheMainPipeBundle):
        super().__init__(bundle)
        bundle.set_all(0)
        self.bundle = bundle

    async def flush_s0_fire(self):

        # set s0_fire
        self.bundle.io._dataArray._toIData._3._ready.value = 1
        self.bundle.io._wayLookupRead._valid.value = 1
        self.bundle.io._fetch._req._valid.value = 1
        await self.bundle.step()
        
        print( f"\nBefore setting: s0_fire is: ",self.bundle.ICacheMainPipe._s0_fire.value)

        self.bundle.io._flush.value = 1
        await self.bundle.step()

        print( f"After setting: s0_fire is: ",self.bundle.ICacheMainPipe._s0_fire.value)
