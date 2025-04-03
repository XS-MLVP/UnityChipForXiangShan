from toffee import Agent
from ..bundle import ICacheMissUnitBundle


class ICacheMissUnitAgent(Agent):
    def __init__(self, bundle: ICacheMissUnitBundle):
        super().__init__(bundle)
        self.bundle = bundle

    async def fencei_func(self, value):

        print(f"\nBefore setting fencei :")

        for i in range(10):
            print(
                f"prefetchMSHRs.{i}.io.req.ready.value:",
                getattr(
                    self.bundle.ICacheMissUnit_._prefetchMSHRs, f"_{i}"
                )._io._req_ready.value,
            )
            print(
                f"prefetchMSHRs.{i}.io.acquire.valid.value:",
                getattr(
                    self.bundle.ICacheMissUnit_._prefetchMSHRs, f"_{i}"
                )._io._acquire_valid.value,
            )
            
        for i in range(4):
            print(
                f"fetchMSHRs.{i}.io.req.ready.value:",
                getattr(
                    self.bundle.ICacheMissUnit_._fetchMSHRs, f"_{i}"
                )._io._req_ready.value,
            )
            print(
                f"fetchMSHRs.{i}.io.acquire.valid.value:",
                getattr(
                    self.bundle.ICacheMissUnit_._fetchMSHRs, f"_{i}"
                )._io._acquire_valid.value,
            )

        self.bundle.io._fencei.value = value
        await self.bundle.step()

        print(f"\nAfter setting fencei = {value}")

        for i in range(10):
            print(
                f"prefetchMSHRs.{i}.io.req.ready.value:",
                getattr(
                    self.bundle.ICacheMissUnit_._prefetchMSHRs, f"_{i}"
                )._io._req_ready.value,
            )
            print(
                f"prefetchMSHRs.{i}.io.acquire.valid.value:",
                getattr(
                    self.bundle.ICacheMissUnit_._prefetchMSHRs, f"_{i}"
                )._io._acquire_valid.value,
            )

        for i in range(4):
            print(
                f"fetchMSHRs.{i}.io.req.ready.value:",
                getattr(
                    self.bundle.ICacheMissUnit_._fetchMSHRs, f"_{i}"
                )._io._req_ready.value,
            )
            print(
                f"fetchMSHRs.{i}.io.acquire.valid.value:",
                getattr(
                    self.bundle.ICacheMissUnit_._fetchMSHRs, f"_{i}"
                )._io._acquire_valid.value,
            )
