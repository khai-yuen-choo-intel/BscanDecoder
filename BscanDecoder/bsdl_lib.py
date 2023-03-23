class Bsdl:

    def __init__(self,num = "", cell="",function="",safe="",port=""):
        self.num = num
        self.port = port
        self.cell = cell
        self.function = function
        self.safe = safe

    def __repr__(self):
       return "Num:{} Port:{}, Cell:{}, Function:{}, Safe:{}".format(self.num, self.port,self.cell,self.function,self.safe)
    
    def is_output(self):
        return 1 if "output" in self.function else 0

    def is_observe(self):
        return 1 if "observe" in self.function else 0

    def is_input(self):
        return 1 if self.function == "input" else 0

    def is_bidir(self):
        return 1 if self.function == "bidir" else 0

    def is_internal(self):
        return 1 if self.function == "internal" else 0

    def is_power(self):
        return 1 if self.function == "power" else 0

    def is_segmentsel(self):
        return 1 if self.function == "segment_select" else 0

    def is_ac(self):
        return 1 if "ac" in self.cell.lower() else 0