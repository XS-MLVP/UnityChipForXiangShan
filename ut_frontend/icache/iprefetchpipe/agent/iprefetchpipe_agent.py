from toffee import Agent
from ..bundle import IPrefetchPipeBundle
import random


class IPrefetchPipeAgent(Agent):
    def __init__(self, bundle: IPrefetchPipeBundle):
        super().__init__(bundle)
        self.bundle = bundle

    async def set_s1_flush(self):
        self.bundle.reset.value = 1
        await self.bundle.step()
        self.bundle.reset.value = 0
        await self.bundle.step()

        print(
            "\nBefore setting, s1_flush is: ",
            self.bundle.IPrefetchPipe._s1._flush.value,
        )
        self.bundle.io._flush.value = 1
        await self.bundle.step()
        print(
            "After setting, s1_flush is: ", self.bundle.IPrefetchPipe._s1._flush.value
        )


    async def receive_prefetch(self):
        self.bundle.io._req._bits._startAddr.value = random.randint(0, (1<<49)-1)<<1
        self.bundle.io._req._bits._nextlineStart.value = random.randint(0, (1<<49)-1)<<1
        self.bundle.io._req._bits._isSoftPrefetch.value = random.getrandbits(1)
        self.bundle.io._req._bits._ftqIdx._flag.value = random.getrandbits(1)
        self.bundle.io._req._bits._ftqIdx._value.value = random.randint(0, (1<<6)-1)
        self.bundle.io._req._bits._backendException.value = random.randint(0, (1<<6)-1)

        # set s0_fire
        self.bundle.io._req._valid.value = 1
        self.bundle.io._metaRead._toIMeta._ready.value = 1
        await self.bundle.step()
        self.bundle.io._flush.value = 0

        await self.bundle.step()

        assert (
            self.bundle.IPrefetchPipe._s1._req._vaddr._0.value
            == self.bundle.io._req._bits._startAddr.value
        ), "vaddr_0 is not equal"
        assert (
            self.bundle.IPrefetchPipe._s1._req._vaddr._1.value
            == self.bundle.io._req._bits._nextlineStart.value
        ), "vaddr_1 is not equal"
        assert (
            self.bundle.IPrefetchPipe._s1._isSoftPrefetch.value
            == self.bundle.io._req._bits._isSoftPrefetch.value
        ), "isSoftPrefetch is not equal"
        assert self.bundle.IPrefetchPipe._s1._doubleline.value == int(
            (bin(self.bundle.io._req._bits._startAddr.value)[2:])[-6]
        ), "doubleline is not equal"
        assert (
            self.bundle.IPrefetchPipe._s1._req._ftqIdx._flag.value
            == self.bundle.io._req._bits._ftqIdx._flag.value
        ), "ftqIdx_flag is not equal"
        assert (
            self.bundle.IPrefetchPipe._s1._req._ftqIdx._value.value
            == self.bundle.io._req._bits._ftqIdx._value.value
        ), "ftqIdx_value is not equal"
        assert (
            self.bundle.IPrefetchPipe._s1._backendException._0.value
            == self.bundle.io._req._bits._backendException.value
        ), "backendException_0 is not equal"
        assert (
            self.bundle.IPrefetchPipe._s1._backendException._1.value
            == self.bundle.io._req._bits._backendException.value
        ), "backendException_1 is not equal"

        await self.bundle.step(2)
