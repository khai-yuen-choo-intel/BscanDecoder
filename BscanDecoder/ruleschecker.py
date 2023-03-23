
class RulesField:

    def __init__(self, spffile = "", line = "", category = "", desc = ""):
        self.spffile = spffile
        self.line = line
        self.category = category
        self.desc = desc

    def __repr__(self):
       return "SPF:{} Line:{}, Category:{}, Desc:{}".format(self.spffile, self.line, self.category, self.desc)

def check_expandata(expandata):
    return 0 if expandata >=1 else 1

def check_pinlabel(instrobe_pincount, pinlabel_count):
    return 0 if instrobe_pincount == pinlabel_count else 1
        
def check_outputstrobe(out_pincount, vector_strobe):
    return 0 if out_pincount == vector_strobe else 1

def check_inputstrobe(in_pincount, instrobe_pincount):
    return 0 if in_pincount == instrobe_pincount else 1

def check_inputforce(instrobe_pincount, vectorforce_pincount):
    return 0 if instrobe_pincount == vectorforce_pincount else 1
