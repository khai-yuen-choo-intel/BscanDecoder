class Bsdl:

    class differentialPair:
        def __init__(self):
            self.port = None
            self.pinmap = None
            self.channel = None
            self.socket = None

        def __repr__(self):
            return self.port

    def __init__(self,num = "", cell="",function="",safe="",port="",ccell="",disval="",rslt=""):
        self.num = num
        self.cell = cell
        self.port = port
        self.function = function
        self.safe = safe
        self.ccell = ccell
        self.disval = disval
        self.rslt = rslt
        self.acio = None
        self.toggle = None
        self.differential = None
        self.pinmap = None
        self.socket = None
        self.channel = None
        

    def __repr__(self):
       return "Num:{} Port:{}, Cell:{}, Function:{}, Safe:{}, ACIO: {}, Toggle: {}".format(self.num, self.port,self.cell,self.function,self.safe, self.acio, self.toggle)
    
    def is_output(self):
        return 1 if "output" in self.function else 0

    def is_observe(self):
        return 1 if "observe" in self.function else 0

    def is_observe_xac(self):
        return 1 if "observe" in self.function and "ac" not in self.cell.lower() else 0

    def is_input(self):
        return 1 if self.function == "input" else 0

    def is_bidir(self):
        return 1 if self.function == "bidir" else 0

    def is_internal(self):
        return 1 if self.function == "internal" else 0

    def is_power(self):
        return 1 if self.function == "power" else 0

    def is_segmentsel(self):
        return 1 if self.function == "segment select" else 0

    def is_delay(self):
        return 1 if self.function == "delay" else 0

    def is_acrx(self):
        if self.acio:
            if self.function == "observe_only" or self.function == "input":
                return 1
        return 0

    def is_actx(self):
        if self.acio == True:
            if "output" in self.function:
                return 1
        return 0

    def is_togglepin(self):
        return 1 if self.toggle else 0

    def is_differential_output(self):
        return 1 if self.differential and (self.is_output or self.is_observe or self.is_bidir) else 0

    def is_differential_input(self):
        return 1 if self.differential and (self.is_input or self.is_bidir) else 0

    def is_pin(self):
        if self.is_output():
            return True
        elif self.is_observe():
            return True
        elif self.is_input():
            return True
        elif self.is_bidir():
            return True
        else:
            return False

        