class BreakpointSetter():
	def __init__(self):
		self.matchType = 0
		self.action = 0
		self.tdata2 = 0
		self.select = False
		self.chain = False
		self.addr = 0
		self.valid = False

class FrontendTriggerReq():
	def __init__(self):
		self.bpSetter = BreakpointSetter()
		self.tEnableVec = [False, False, False, False]
		self.debugMode = False
		self.triggerCanRaiseBPExp = False




