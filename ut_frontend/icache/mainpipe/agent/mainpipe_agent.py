from toffee import Agent
from ..bundle import ICacheMainPipeBundle


class ICacheMainPipeAgent(Agent):
    def __init__(self, bundle: ICacheMainPipeBundle):
        super().__init__(bundle)
        bundle.set_all(0)
        self.bundle = bundle

    async def set_flush(self):

        print(
            f"\nBefore setting: \n \
            s2_fire is: {self.bundle.ICacheMainPipe_s2._fire.value}\n \
            _toMSHRArbiter_io_in_0_valid is: {self.bundle.ICacheMainPipe__toMSHRArbiter_io_in._0._valid_T._4.value}\n \
            _toMSHRArbiter_io_in_1_valid is: {self.bundle.ICacheMainPipe__toMSHRArbiter_io_in._1._valid_T._4.value}\n \
            s2_valid is: {self.bundle.ICacheMainPipe_s2._valid.value}\n \
            "
        )

        self.bundle.io._flush.value = 1
        await self.bundle.step()

        print(
            f"After setting: \n \
            s2_fire is: {self.bundle.ICacheMainPipe_s2._fire.value}\n \
            _toMSHRArbiter_io_in_0_valid is: {self.bundle.ICacheMainPipe__toMSHRArbiter_io_in._0._valid_T._4.value}\n \
            _toMSHRArbiter_io_in_1_valid is: {self.bundle.ICacheMainPipe__toMSHRArbiter_io_in._1._valid_T._4.value}\n \
            s2_valid is: {self.bundle.ICacheMainPipe_s2._valid.value}\n \
            "
        )
