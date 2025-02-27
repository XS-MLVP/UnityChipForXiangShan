#coding=utf8

try:
    from . import xspcomm as xsp
except Exception as e:
    import xspcomm as xsp

if __package__ or "." in __name__:
    from .libUT_FtqRedirectMem import *
else:
    from libUT_FtqRedirectMem import *


class DUTFtqRedirectMem(object):

    # initialize
    def __init__(self, *args, **kwargs):
        self.dut = DutUnifiedBase(*args)
        self.xclock = xsp.XClock(self.dut.simStep)
        self.xport  = xsp.XPort()
        self.xclock.Add(self.xport)
        self.event = self.xclock.getEvent()
        self.internal_signals = {}
        # set output files
        if kwargs.get("waveform_filename"):
            self.dut.SetWaveform(kwargs.get("waveform_filename"))
        if kwargs.get("coverage_filename"):
            self.dut.SetCoverage(kwargs.get("coverage_filename"))

        # all Pins
        self.clock = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.reset = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_ren_0 = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_ren_1 = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_ren_2 = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_raddr_0 = xsp.XPin(xsp.XData(6, xsp.XData.In), self.event)
        self.io_raddr_1 = xsp.XPin(xsp.XData(6, xsp.XData.In), self.event)
        self.io_raddr_2 = xsp.XPin(xsp.XData(6, xsp.XData.In), self.event)
        self.io_rdata_0_histPtr_flag = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_rdata_0_histPtr_value = xsp.XPin(xsp.XData(8, xsp.XData.Out), self.event)
        self.io_rdata_0_ssp = xsp.XPin(xsp.XData(4, xsp.XData.Out), self.event)
        self.io_rdata_0_sctr = xsp.XPin(xsp.XData(3, xsp.XData.Out), self.event)
        self.io_rdata_0_TOSW_flag = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_rdata_0_TOSW_value = xsp.XPin(xsp.XData(5, xsp.XData.Out), self.event)
        self.io_rdata_0_TOSR_flag = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_rdata_0_TOSR_value = xsp.XPin(xsp.XData(5, xsp.XData.Out), self.event)
        self.io_rdata_0_NOS_flag = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_rdata_0_NOS_value = xsp.XPin(xsp.XData(5, xsp.XData.Out), self.event)
        self.io_rdata_0_topAddr = xsp.XPin(xsp.XData(50, xsp.XData.Out), self.event)
        self.io_rdata_1_histPtr_flag = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_rdata_1_histPtr_value = xsp.XPin(xsp.XData(8, xsp.XData.Out), self.event)
        self.io_rdata_1_ssp = xsp.XPin(xsp.XData(4, xsp.XData.Out), self.event)
        self.io_rdata_1_sctr = xsp.XPin(xsp.XData(3, xsp.XData.Out), self.event)
        self.io_rdata_1_TOSW_flag = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_rdata_1_TOSW_value = xsp.XPin(xsp.XData(5, xsp.XData.Out), self.event)
        self.io_rdata_1_TOSR_flag = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_rdata_1_TOSR_value = xsp.XPin(xsp.XData(5, xsp.XData.Out), self.event)
        self.io_rdata_1_NOS_flag = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_rdata_1_NOS_value = xsp.XPin(xsp.XData(5, xsp.XData.Out), self.event)
        self.io_rdata_2_histPtr_value = xsp.XPin(xsp.XData(8, xsp.XData.Out), self.event)
        self.io_wen_0 = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_waddr_0 = xsp.XPin(xsp.XData(6, xsp.XData.In), self.event)
        self.io_wdata_0_histPtr_flag = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_wdata_0_histPtr_value = xsp.XPin(xsp.XData(8, xsp.XData.In), self.event)
        self.io_wdata_0_ssp = xsp.XPin(xsp.XData(4, xsp.XData.In), self.event)
        self.io_wdata_0_sctr = xsp.XPin(xsp.XData(3, xsp.XData.In), self.event)
        self.io_wdata_0_TOSW_flag = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_wdata_0_TOSW_value = xsp.XPin(xsp.XData(5, xsp.XData.In), self.event)
        self.io_wdata_0_TOSR_flag = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_wdata_0_TOSR_value = xsp.XPin(xsp.XData(5, xsp.XData.In), self.event)
        self.io_wdata_0_NOS_flag = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_wdata_0_NOS_value = xsp.XPin(xsp.XData(5, xsp.XData.In), self.event)
        self.io_wdata_0_topAddr = xsp.XPin(xsp.XData(50, xsp.XData.In), self.event)


        # BindDPI
        self.clock.BindDPIPtr(self.dut.GetDPIHandle("clock", 0), self.dut.GetDPIHandle("clock", 1))
        self.reset.BindDPIPtr(self.dut.GetDPIHandle("reset", 0), self.dut.GetDPIHandle("reset", 1))
        self.io_ren_0.BindDPIPtr(self.dut.GetDPIHandle("io_ren_0", 0), self.dut.GetDPIHandle("io_ren_0", 1))
        self.io_ren_1.BindDPIPtr(self.dut.GetDPIHandle("io_ren_1", 0), self.dut.GetDPIHandle("io_ren_1", 1))
        self.io_ren_2.BindDPIPtr(self.dut.GetDPIHandle("io_ren_2", 0), self.dut.GetDPIHandle("io_ren_2", 1))
        self.io_raddr_0.BindDPIPtr(self.dut.GetDPIHandle("io_raddr_0", 0), self.dut.GetDPIHandle("io_raddr_0", 1))
        self.io_raddr_1.BindDPIPtr(self.dut.GetDPIHandle("io_raddr_1", 0), self.dut.GetDPIHandle("io_raddr_1", 1))
        self.io_raddr_2.BindDPIPtr(self.dut.GetDPIHandle("io_raddr_2", 0), self.dut.GetDPIHandle("io_raddr_2", 1))
        self.io_rdata_0_histPtr_flag.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_0_histPtr_flag", 0), self.dut.GetDPIHandle("io_rdata_0_histPtr_flag", 1))
        self.io_rdata_0_histPtr_value.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_0_histPtr_value", 0), self.dut.GetDPIHandle("io_rdata_0_histPtr_value", 1))
        self.io_rdata_0_ssp.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_0_ssp", 0), self.dut.GetDPIHandle("io_rdata_0_ssp", 1))
        self.io_rdata_0_sctr.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_0_sctr", 0), self.dut.GetDPIHandle("io_rdata_0_sctr", 1))
        self.io_rdata_0_TOSW_flag.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_0_TOSW_flag", 0), self.dut.GetDPIHandle("io_rdata_0_TOSW_flag", 1))
        self.io_rdata_0_TOSW_value.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_0_TOSW_value", 0), self.dut.GetDPIHandle("io_rdata_0_TOSW_value", 1))
        self.io_rdata_0_TOSR_flag.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_0_TOSR_flag", 0), self.dut.GetDPIHandle("io_rdata_0_TOSR_flag", 1))
        self.io_rdata_0_TOSR_value.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_0_TOSR_value", 0), self.dut.GetDPIHandle("io_rdata_0_TOSR_value", 1))
        self.io_rdata_0_NOS_flag.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_0_NOS_flag", 0), self.dut.GetDPIHandle("io_rdata_0_NOS_flag", 1))
        self.io_rdata_0_NOS_value.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_0_NOS_value", 0), self.dut.GetDPIHandle("io_rdata_0_NOS_value", 1))
        self.io_rdata_0_topAddr.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_0_topAddr", 0), self.dut.GetDPIHandle("io_rdata_0_topAddr", 1))
        self.io_rdata_1_histPtr_flag.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_1_histPtr_flag", 0), self.dut.GetDPIHandle("io_rdata_1_histPtr_flag", 1))
        self.io_rdata_1_histPtr_value.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_1_histPtr_value", 0), self.dut.GetDPIHandle("io_rdata_1_histPtr_value", 1))
        self.io_rdata_1_ssp.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_1_ssp", 0), self.dut.GetDPIHandle("io_rdata_1_ssp", 1))
        self.io_rdata_1_sctr.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_1_sctr", 0), self.dut.GetDPIHandle("io_rdata_1_sctr", 1))
        self.io_rdata_1_TOSW_flag.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_1_TOSW_flag", 0), self.dut.GetDPIHandle("io_rdata_1_TOSW_flag", 1))
        self.io_rdata_1_TOSW_value.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_1_TOSW_value", 0), self.dut.GetDPIHandle("io_rdata_1_TOSW_value", 1))
        self.io_rdata_1_TOSR_flag.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_1_TOSR_flag", 0), self.dut.GetDPIHandle("io_rdata_1_TOSR_flag", 1))
        self.io_rdata_1_TOSR_value.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_1_TOSR_value", 0), self.dut.GetDPIHandle("io_rdata_1_TOSR_value", 1))
        self.io_rdata_1_NOS_flag.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_1_NOS_flag", 0), self.dut.GetDPIHandle("io_rdata_1_NOS_flag", 1))
        self.io_rdata_1_NOS_value.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_1_NOS_value", 0), self.dut.GetDPIHandle("io_rdata_1_NOS_value", 1))
        self.io_rdata_2_histPtr_value.BindDPIPtr(self.dut.GetDPIHandle("io_rdata_2_histPtr_value", 0), self.dut.GetDPIHandle("io_rdata_2_histPtr_value", 1))
        self.io_wen_0.BindDPIPtr(self.dut.GetDPIHandle("io_wen_0", 0), self.dut.GetDPIHandle("io_wen_0", 1))
        self.io_waddr_0.BindDPIPtr(self.dut.GetDPIHandle("io_waddr_0", 0), self.dut.GetDPIHandle("io_waddr_0", 1))
        self.io_wdata_0_histPtr_flag.BindDPIPtr(self.dut.GetDPIHandle("io_wdata_0_histPtr_flag", 0), self.dut.GetDPIHandle("io_wdata_0_histPtr_flag", 1))
        self.io_wdata_0_histPtr_value.BindDPIPtr(self.dut.GetDPIHandle("io_wdata_0_histPtr_value", 0), self.dut.GetDPIHandle("io_wdata_0_histPtr_value", 1))
        self.io_wdata_0_ssp.BindDPIPtr(self.dut.GetDPIHandle("io_wdata_0_ssp", 0), self.dut.GetDPIHandle("io_wdata_0_ssp", 1))
        self.io_wdata_0_sctr.BindDPIPtr(self.dut.GetDPIHandle("io_wdata_0_sctr", 0), self.dut.GetDPIHandle("io_wdata_0_sctr", 1))
        self.io_wdata_0_TOSW_flag.BindDPIPtr(self.dut.GetDPIHandle("io_wdata_0_TOSW_flag", 0), self.dut.GetDPIHandle("io_wdata_0_TOSW_flag", 1))
        self.io_wdata_0_TOSW_value.BindDPIPtr(self.dut.GetDPIHandle("io_wdata_0_TOSW_value", 0), self.dut.GetDPIHandle("io_wdata_0_TOSW_value", 1))
        self.io_wdata_0_TOSR_flag.BindDPIPtr(self.dut.GetDPIHandle("io_wdata_0_TOSR_flag", 0), self.dut.GetDPIHandle("io_wdata_0_TOSR_flag", 1))
        self.io_wdata_0_TOSR_value.BindDPIPtr(self.dut.GetDPIHandle("io_wdata_0_TOSR_value", 0), self.dut.GetDPIHandle("io_wdata_0_TOSR_value", 1))
        self.io_wdata_0_NOS_flag.BindDPIPtr(self.dut.GetDPIHandle("io_wdata_0_NOS_flag", 0), self.dut.GetDPIHandle("io_wdata_0_NOS_flag", 1))
        self.io_wdata_0_NOS_value.BindDPIPtr(self.dut.GetDPIHandle("io_wdata_0_NOS_value", 0), self.dut.GetDPIHandle("io_wdata_0_NOS_value", 1))
        self.io_wdata_0_topAddr.BindDPIPtr(self.dut.GetDPIHandle("io_wdata_0_topAddr", 0), self.dut.GetDPIHandle("io_wdata_0_topAddr", 1))


        # Add2Port
        self.xport.Add("clock", self.clock.xdata)
        self.xport.Add("reset", self.reset.xdata)
        self.xport.Add("io_ren_0", self.io_ren_0.xdata)
        self.xport.Add("io_ren_1", self.io_ren_1.xdata)
        self.xport.Add("io_ren_2", self.io_ren_2.xdata)
        self.xport.Add("io_raddr_0", self.io_raddr_0.xdata)
        self.xport.Add("io_raddr_1", self.io_raddr_1.xdata)
        self.xport.Add("io_raddr_2", self.io_raddr_2.xdata)
        self.xport.Add("io_rdata_0_histPtr_flag", self.io_rdata_0_histPtr_flag.xdata)
        self.xport.Add("io_rdata_0_histPtr_value", self.io_rdata_0_histPtr_value.xdata)
        self.xport.Add("io_rdata_0_ssp", self.io_rdata_0_ssp.xdata)
        self.xport.Add("io_rdata_0_sctr", self.io_rdata_0_sctr.xdata)
        self.xport.Add("io_rdata_0_TOSW_flag", self.io_rdata_0_TOSW_flag.xdata)
        self.xport.Add("io_rdata_0_TOSW_value", self.io_rdata_0_TOSW_value.xdata)
        self.xport.Add("io_rdata_0_TOSR_flag", self.io_rdata_0_TOSR_flag.xdata)
        self.xport.Add("io_rdata_0_TOSR_value", self.io_rdata_0_TOSR_value.xdata)
        self.xport.Add("io_rdata_0_NOS_flag", self.io_rdata_0_NOS_flag.xdata)
        self.xport.Add("io_rdata_0_NOS_value", self.io_rdata_0_NOS_value.xdata)
        self.xport.Add("io_rdata_0_topAddr", self.io_rdata_0_topAddr.xdata)
        self.xport.Add("io_rdata_1_histPtr_flag", self.io_rdata_1_histPtr_flag.xdata)
        self.xport.Add("io_rdata_1_histPtr_value", self.io_rdata_1_histPtr_value.xdata)
        self.xport.Add("io_rdata_1_ssp", self.io_rdata_1_ssp.xdata)
        self.xport.Add("io_rdata_1_sctr", self.io_rdata_1_sctr.xdata)
        self.xport.Add("io_rdata_1_TOSW_flag", self.io_rdata_1_TOSW_flag.xdata)
        self.xport.Add("io_rdata_1_TOSW_value", self.io_rdata_1_TOSW_value.xdata)
        self.xport.Add("io_rdata_1_TOSR_flag", self.io_rdata_1_TOSR_flag.xdata)
        self.xport.Add("io_rdata_1_TOSR_value", self.io_rdata_1_TOSR_value.xdata)
        self.xport.Add("io_rdata_1_NOS_flag", self.io_rdata_1_NOS_flag.xdata)
        self.xport.Add("io_rdata_1_NOS_value", self.io_rdata_1_NOS_value.xdata)
        self.xport.Add("io_rdata_2_histPtr_value", self.io_rdata_2_histPtr_value.xdata)
        self.xport.Add("io_wen_0", self.io_wen_0.xdata)
        self.xport.Add("io_waddr_0", self.io_waddr_0.xdata)
        self.xport.Add("io_wdata_0_histPtr_flag", self.io_wdata_0_histPtr_flag.xdata)
        self.xport.Add("io_wdata_0_histPtr_value", self.io_wdata_0_histPtr_value.xdata)
        self.xport.Add("io_wdata_0_ssp", self.io_wdata_0_ssp.xdata)
        self.xport.Add("io_wdata_0_sctr", self.io_wdata_0_sctr.xdata)
        self.xport.Add("io_wdata_0_TOSW_flag", self.io_wdata_0_TOSW_flag.xdata)
        self.xport.Add("io_wdata_0_TOSW_value", self.io_wdata_0_TOSW_value.xdata)
        self.xport.Add("io_wdata_0_TOSR_flag", self.io_wdata_0_TOSR_flag.xdata)
        self.xport.Add("io_wdata_0_TOSR_value", self.io_wdata_0_TOSR_value.xdata)
        self.xport.Add("io_wdata_0_NOS_flag", self.io_wdata_0_NOS_flag.xdata)
        self.xport.Add("io_wdata_0_NOS_value", self.io_wdata_0_NOS_value.xdata)
        self.xport.Add("io_wdata_0_topAddr", self.io_wdata_0_topAddr.xdata)


        # Cascaded ports
        self.io = self.xport.NewSubPort("io_")
        self.io_raddr = self.xport.NewSubPort("io_raddr_")
        self.io_rdata = self.xport.NewSubPort("io_rdata_")
        self.io_rdata_0 = self.xport.NewSubPort("io_rdata_0_")
        self.io_rdata_0_NOS = self.xport.NewSubPort("io_rdata_0_NOS_")
        self.io_rdata_0_TOSR = self.xport.NewSubPort("io_rdata_0_TOSR_")
        self.io_rdata_0_TOSW = self.xport.NewSubPort("io_rdata_0_TOSW_")
        self.io_rdata_0_histPtr = self.xport.NewSubPort("io_rdata_0_histPtr_")
        self.io_rdata_1 = self.xport.NewSubPort("io_rdata_1_")
        self.io_rdata_1_NOS = self.xport.NewSubPort("io_rdata_1_NOS_")
        self.io_rdata_1_TOSR = self.xport.NewSubPort("io_rdata_1_TOSR_")
        self.io_rdata_1_TOSW = self.xport.NewSubPort("io_rdata_1_TOSW_")
        self.io_rdata_1_histPtr = self.xport.NewSubPort("io_rdata_1_histPtr_")
        self.io_rdata_2 = self.xport.NewSubPort("io_rdata_2_")
        self.io_ren = self.xport.NewSubPort("io_ren_")
        self.io_waddr = self.xport.NewSubPort("io_waddr_")
        self.io_wdata = self.xport.NewSubPort("io_wdata_")
        self.io_wdata_0 = self.xport.NewSubPort("io_wdata_0_")
        self.io_wdata_0_NOS = self.xport.NewSubPort("io_wdata_0_NOS_")
        self.io_wdata_0_TOSR = self.xport.NewSubPort("io_wdata_0_TOSR_")
        self.io_wdata_0_TOSW = self.xport.NewSubPort("io_wdata_0_TOSW_")
        self.io_wdata_0_histPtr = self.xport.NewSubPort("io_wdata_0_histPtr_")
        self.io_wen = self.xport.NewSubPort("io_wen_")


    def __del__(self):
        self.Finish()

    ################################
    #         User APIs            #
    ################################
    def InitClock(self, name: str):
        self.xclock.Add(self.xport[name])

    def Step(self, i:int = 1):
        self.xclock.Step(i)

    def StepRis(self, callback, args=(), kwargs={}):
        self.xclock.StepRis(callback, args, kwargs)

    def StepFal(self, callback, args=(), kwargs={}):
        self.xclock.StepFal(callback, args, kwargs)

    def SetWaveform(self, filename: str):
        self.dut.SetWaveform(filename)
    
    def FlushWaveform(self):
        self.dut.FlushWaveform()

    def SetCoverage(self, filename: str):
        self.dut.SetCoverage(filename)
    
    def CheckPoint(self, name: str) -> int:
        self.dut.CheckPoint(name)

    def Restore(self, name: str) -> int:
        self.dut.Restore(name)

    def GetInternalSignal(self, name: str):
        if name not in self.internal_signals:
            signal = xsp.XData.FromVPI(self.dut.GetVPIHandleObj(name),
                                       self.dut.GetVPIFuncPtr("vpi_get"),
                                       self.dut.GetVPIFuncPtr("vpi_get_value"),
                                       self.dut.GetVPIFuncPtr("vpi_put_value"), name)
            if signal is None:
                return None
            self.internal_signals[name] = xsp.XPin(signal, self.event)
        return self.internal_signals[name]

    def VPIInternalSignalList(self, prefix="", deep=99):
        return self.dut.VPIInternalSignalList(prefix, deep)

    def Finish(self):
        self.dut.Finish()

    def RefreshComb(self):
        self.dut.RefreshComb()

    ################################
    #      End of User APIs        #
    ################################

    def __getitem__(self, key):
        return xsp.XPin(self.port[key], self.event)

    # Async APIs wrapped from XClock
    async def AStep(self,i: int):
        return await self.xclock.AStep(i)

    async def Acondition(self,fc_cheker):
        return await self.xclock.ACondition(fc_cheker)

    def RunStep(self,i: int):
        return self.xclock.RunStep(i)

    def __setattr__(self, name, value):
        assert not isinstance(getattr(self, name, None),
                              (xsp.XPin, xsp.XData)), \
        f"XPin and XData of DUT are read-only, do you mean to set the value of the signal? please use `{name}.value = ` instead."
        return super().__setattr__(name, value)


if __name__=="__main__":
    dut=DUTFtqRedirectMem()
    dut.Step(100)
