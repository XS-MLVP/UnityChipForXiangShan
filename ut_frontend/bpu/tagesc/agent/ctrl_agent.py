from toffee.agent import Agent

from ..bundle import CtrlBundle, PipelineBundle

__all__ = ['ControlAgent']


class ControlAgent(Agent):
    def __init__(self, ctrl_bundle: CtrlBundle, stage_bundle: PipelineBundle):
        super().__init__(stage_bundle.step)
        ctrl_bundle.set_all(1)
        stage_bundle.set_all(0)
        self.io_ctrl = ctrl_bundle
        self.io_stage = stage_bundle

    async def exec_activate(self) -> None:
        for i in range(4):
            getattr(self.io_stage, f"s0_fire_{i}").value = 1
        await self.io_stage.step()

        for i in range(4):
            getattr(self.io_stage, f"s0_fire_{i}").value = 0
        for i in range(4):
            getattr(self.io_stage, f"s1_fire_{i}").value = 1
        await self.io_stage.step()

        for i in range(4):
            getattr(self.io_stage, f"s1_fire_{i}").value = 0
        for i in range(4):
            getattr(self.io_stage, f"s2_fire_{i}").value = 1
        await self.io_stage.step()

        for i in range(4):
            getattr(self.io_stage, f"s2_fire_{i}").value = 0
        await self.io_stage.step()
