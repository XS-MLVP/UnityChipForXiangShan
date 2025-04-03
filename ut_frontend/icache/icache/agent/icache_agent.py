from toffee import Agent
from ..bundle import ICacheBundle


class ICacheAgent(Agent):
    def __init__(self, bundle: ICacheBundle):
        super().__init__(bundle)
        self.bundle = bundle

    async def fencei_meta_array_func(self, value):

        print(
            f"\nBefore setting fencei: ICacheMetaArray.io_read_ready.value is:",
            self.bundle.ICache__metaArray_io_read_ready.value,
        )

        self.bundle.io._fencei.value = value
        await self.bundle.step()

        print(
            f"\nAfter setting fencei = {value}: ICacheMetaArray.io_read_ready.value is:",
            self.bundle.ICache__metaArray_io_read_ready.value,
        )
