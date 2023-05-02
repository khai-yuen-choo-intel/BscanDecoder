class SpfField:
    strobe_charlist = ["0","1","H","L"]

    def __init__(self,configurationType = "",focus_tap = "",register="",field="",cell="",function="",safe="",write="",read="", rpt=""):
        self.configurationType = configurationType
        self.focus_tap = focus_tap
        self.register = register
        self.field = field
        self.cell = cell
        self.function = function
        self.safe = safe
        self.write = write
        self.read = read
        self.rpt = rpt
        self.pinmap = field

    def __repr__(self):
       return "Type:{}, Tap:{}, Reg:{}, Field:{}, Cell:{}, Function:{}, Write:{}, Read:{}\n".format(self.configurationType,self.focus_tap,self.register,self.field,self.cell,self.function,self.write,self.read)

    def is_cyclemorethan1000(self):
        if self.configurationType == "cycle":
            if self.write.isdigit():
                delay = int(self.write)
                return delay if delay > 1000 else 0
        else:
            return 0

    def is_expandata(self):
        return 1 if self.configurationType == "expandata" else 0

    def is_pinlabel(self):
        return 1 if self.configurationType == "pin_label" else 0

    def is_output(self):
        return 1 if "output" in self.field else 0

    def is_observedonly(self):
        return 1 if "observe" in self.field else 0

    def is_input(self):
        return 1 if self.field == "input" else 0

    def is_bidir(self):
        return 1 if self.field == "bidir" else 0

    def is_internal(self):
        return 1 if self.field == "internal" else 0

    def is_power(self):
        return 1 if self.field == "power" else 0

    def is_segmentsel(self):
        return 1 if self.field == "segment_select" else 0

    def is_controlnotsafe(self):
        if self.function == "control":
            return 1 if self.write != self.safe else 0
        return 0
                
    def is_controlsafe(self):
        if self.function == "control":
            return 1 if self.write == self.safe else 0
        return 0

    def is_powernotsafe(self):
        if self.function == "power":
            return 1 if self.write != self.safe else 0
        return 0

    def is_segmentselnotsafe(self):
        if self.function == "segment select":
            return 1 if self.write != self.safe else 0
        return 0

    def is_bidirstrobe(self):
        if self.function == "bidir":
            return 1 if self.read in self.strobe_charlist else 0
        return 0

    def is_inputstrobe(self):
        if self.function == "input":
            return 1 if self.read in self.strobe_charlist else 0
        return 0

    def is_acrxstrobe(self):
        if "ac" in self.cell.lower():
            if "input" in self.function or "observe" in self.function:
                return 1 if self.read in self.strobe_charlist else 0
            return 0
        else:
            return 0

    def is_actxstrobe(self):
        if "ac" in self.cell.lower():
            if "output" in self.function or "observe" in self.function:
                return 1 if self.write in ['H','L'] else 0
            return 0
        else:
            return 0

    def is_vectorforcehigh(self):
        if self.configurationType == "vector":
            return 1 if self.write == "1" else 0
        return 0

    def is_vectorforcelow(self):
        if self.configurationType == "vector":
            return 1 if self.write == "0" else 0
        return 0

    def is_vectorstrobehigh(self):
        if self.configurationType == "vector":
            return 1 if self.write == "H" else 0
        return 0

    def is_vectorstrobelow(self):
        if self.configurationType == "vector":
            return 1 if self.write == "L" else 0
        return 0

    def is_vectorstroberptcountmorethan10(self):
        if self.is_vectorstrobehigh() or self.is_vectorstrobelow():
            if self.rpt.isdigit():
                rptcount = int(self.rpt)
                return 1 if rptcount >= 10 else 0
            else:
                return 0
        else:
            return 1

    def is_scani(self):
        return 1 if self.configurationType == "scani" else 0

    def is_irtdi(self):
        return 1 if self.configurationType == "ir_tdi" else 0
