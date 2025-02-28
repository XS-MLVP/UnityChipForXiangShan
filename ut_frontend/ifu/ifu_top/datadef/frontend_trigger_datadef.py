class BreakpointSetter():
	matchType = 0
	action = 0
	tdata2 = 0
	select = False
	chain = False
	addr = 0
	valid = False

class FrontendTriggerReq():
	bpSetter = BreakpointSetter()
	tEnableVec = [False, False, False, False]
	debugMode = False
	triggerCanRaiseBPExp = False
	fsIsOff = False




