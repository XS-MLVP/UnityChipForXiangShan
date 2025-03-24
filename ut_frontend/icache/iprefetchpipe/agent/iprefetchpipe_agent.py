from toffee import Agent
from ..bundle import IPrefetchPipeBundle


class IPrefetchPipeAgent(Agent):
    def __inti__(self, bundle: IPrefetchPipeBundle):
        super().__init__(bundle)
        bundle.set_all(0)
        self.bundle = bundle

    async def set_s1_flush(self):
        self.bundle.reset.value = 1
        await self.bundle.step()
        self.bundle.reset.value = 0
        await self.bundle.step()

        print(
            "\nBefore setting, s1_flush is: ", self.bundle.IPrefetchPipe_s1_flush.value
        )
        self.bundle.io._flush.value = 1
        await self.bundle.step()
        print("After setting, s1_flush is: ", self.bundle.IPrefetchPipe_s1_flush.value)
