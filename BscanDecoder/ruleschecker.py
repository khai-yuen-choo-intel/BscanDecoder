
class RulesField:

    def __init__(self, spffile = "", rule = "", line = "", category = "", desc = ""):
        self.spffile = spffile
        self.rule = rule
        self.line = line
        self.category = category
        self.desc = desc

    def __repr__(self):
       return "SPF:{} RULE:{} Line:{}, Category:{}, Desc:{}".format(self.spffile, self.rule, self.line, self.category, self.desc)

class TestSummaryField:

    def __init__(self, spffile = "", vector_strobeH = "",  vector_strobeL = "", vector_force1 = "", vector_force0 = "", tdo_strobe = "", pin_label = ""):
        self.spffile = spffile
        self.vector_strobeH = vector_strobeH
        self.vector_strobeL = vector_strobeL
        self.vector_force1 = vector_force1
        self.vector_force0 = vector_force0
        self.tdo_strobe = tdo_strobe
        self.pin_label = pin_label

class conditionalBscanRule:

    def __init__(self, testName, bsdlObjList, spfObjList):
        self.bsdlObjList = bsdlObjList
        self.spfObjList = spfObjList
        self.testName = testName

        self.inputpinlist = []
        self.outputpinlist = []
        self.observepinlist = []
        self.bidirpinlist = []
        self.acrxpinlist = []
        self.actxpinlist = []
        self.togglepinlist = []
        self.pinlabellist = []
        self.vectorstrobehighlist = []
        self.vectorstrobelowlist = []
        self.vectorforcehighlist = []
        self.vectorforcelowlist = []
        self.bidir_strobe_list = []
        self.input_strobe_list = []
        self.acrxstrobelist = []

        for obj in self.bsdlObjList:
            if obj.is_input():
                self.inputpinlist.append(obj.port.lower())
            if obj.is_output():
                self.outputpinlist.append(obj.port.lower())
            if obj.is_observe():
                self.observepinlist.append(obj.port.lower())
            if obj.is_bidir():
                self.bidirpinlist.append(obj.port.lower())
            if obj.is_acrx():
                self.acrxpinlist.append(obj.port.lower())
            if obj.is_actx():
                self.actxpinlist.append(obj.port.lower())
            if obj.is_togglepin():
                self.togglepinlist.append(obj.port.lower())

        self.input_pincount = len(set(self.inputpinlist))
        self.output_pincount = len(set(self.outputpinlist))
        self.bidir_pincount = len(set(self.bidirpinlist))
        self.observe_pincount = len(set(self.observepinlist))
        self.acrx_pincount = len(set(self.acrxpinlist))
        self.actx_pincount = len(set(self.actxpinlist))
        self.toggle_pincount = len(set(self.togglepinlist))

    

        for obj in self.spfObjList:
            if obj.is_vectorstrobehigh():
                if obj.field.lower() not in self.vectorstrobehighlist:
                    self.vectorstrobehighlist.append(obj.pinmap.lower())
            if obj.is_vectorstrobelow():
                if obj.field.lower() not in self.vectorstrobelowlist:
                    self.vectorstrobelowlist.append(obj.pinmap.lower())
            if obj.is_vectorforcehigh():
                if obj.field.lower() not in self.vectorforcehighlist:
                    self.vectorforcehighlist.append(obj.pinmap.lower())
            if obj.is_vectorforcelow():
                if obj.field.lower() not in self.vectorforcelowlist:
                    self.vectorforcelowlist.append(obj.pinmap.lower()) 
            if obj.is_pinlabel():
                if obj.field.lower() not in self.pinlabellist:
                    self.pinlabellist.append(obj.pinmap.lower())
            if obj.is_bidirstrobe():
                if obj.field.lower() not in self.bidir_strobe_list:
                    self.bidir_strobe_list.append(obj.field.lower())
            if obj.is_inputstrobe():
                if obj.field.lower() not in self.input_strobe_list:
                    self.input_strobe_list.append(obj.field.lower())
            if obj.is_acrxstrobe():
                if obj.field.lower() not in self.acrxstrobelist:
                    self.acrxstrobelist.append(obj.field.lower())

        self.vectorstrobelist = list(dict.fromkeys(self.vectorstrobehighlist + self.vectorstrobelowlist))
        self.vectorstrobe_count = len(set(self.vectorstrobehighlist + self.vectorstrobelowlist))
        self.vectorforce_count = len(set(self.vectorforcehighlist + self.vectorforcelowlist))
        self.bidir_strobe_pincount = len(set(self.bidir_strobe_list))
        self.input_strobe_pincount = len(set(self.input_strobe_list))
        self.acrxstrobe_pincount = len(set(self.acrxstrobelist))

    def format_violation(self,text):
        return "Bscan Rules Violation:[{}]".format(text)

    #Rule1.1: Input Pin Count not equal to Input Pin Strobe Count
    def Rule1_1(self):
        rulesFieldList = []
        if (self.input_pincount + self.bidir_pincount) != (self.bidir_strobe_pincount + self.input_strobe_pincount):
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.1", category = "ERROR", desc = self.format_violation("Input Pin Count ({}) and Input TDO Strobe Count ({}) mismatch.".format(self.input_pincount + self.bidir_pincount, self.bidir_strobe_pincount + self.input_strobe_pincount))))
    
            for pin in self.inputpinlist + self.bidirpinlist:
                if pin not in self.bidir_strobe_list + self.input_strobe_list:
                     rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.1", category = "ERROR", desc = self.format_violation("Input Pin ({}) not strobed.".format(pin))))
            
            for pinstrobe in self.bidir_strobe_list + self.input_strobe_list:
                if pinstrobe not in self.inputpinlist + self.bidirpinlist:
                     rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.1", category = "ERROR", desc = self.format_violation("Non-input Pin ({}) strobed.".format(pinstrobe))))
        
        return rulesFieldList
    
    #Rule1.2: Input Pin Strobe Count not equal to Input Pin Force Count
    def Rule1_2(self):
        rulesFieldList = []
        if (self.bidir_strobe_pincount + self.input_strobe_pincount) != self.vectorforce_count:
            self.rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.2", category = "ERROR", desc = self.format_violation("Input Pin Strobe count ({}) and Vector Forcing Pin count ({}) mismatch.".format(self.bidir_strobe_pincount + self.input_strobe_pincount,self.vectorforce_count))))
            
            for vectorforce in self.vectorforcelowlist + self.vectorforcehighlist:
                if vectorforce not in self.bidir_strobe_list + self.input_strobe_list:
                     rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.2", category = "ERROR", desc = self.format_violation("Pin ({}) forced without strobing.".format(vectorforce))))
            
            for pinstrobe in self.bidir_strobe_list + self.input_strobe_list:
                if pinstrobe not in self.vectorforcelowlist + self.vectorforcehighlist:
                     rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.2", category = "ERROR", desc = self.format_violation("Pin ({}) strobed without forcing.".format(pinstrobe))))
        
        return rulesFieldList

    #Rule1.3: Input Pin Strobe Count not equal to Input Pin Label Count
    def Rule1_3(self):

        rulesFieldList = []

        pinlabel_count = len(self.pinlabellist)
    
        if self.input_strobe_pincount + self.bidir_strobe_pincount != pinlabel_count:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.3", category = "ERROR", desc = self.format_violation("Input Pin strobe count ({}) and Pin Label count ({}) mismatch.".format(self.input_strobe_pincount + self.bidir_strobe_pincount, pinlabel_count))))
            
            for pinstrobe in self.bidir_strobe_list + self.input_strobe_list:
                if pinstrobe not in self.pinlabellist:
                     rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.3", category = "ERROR", desc = self.format_violation("Pin Label for Input Pin ({}) not found.".format(pinstrobe))))

        return rulesFieldList

    #Rule1.4: Control bit not set to safe for input test
    def Rule1_4(self):
        rulesFieldList = []
        for spfObj in self.spfObjList:
            if spfObj.is_controlnotsafe():
                rulesFieldList.append(RulesField(spffile = self.testName, line = self.spfObjList.index(spfObj), rule = "Rule1.4", category = "ERROR", desc = self.format_violation("Control bit not set to safe for input test.")))

        return rulesFieldList
    
    #Rule2.1: Output Pin Count not equal to Output Pin Vector Strobe Count
    def Rule2_1(self):
        rulesFieldList = []
        if self.output_pincount + self.bidir_pincount + self.observe_pincount != self.vectorstrobe_count:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.1", category = "ERROR", desc = self.format_violation("Output Pin Count ({}) and Pin Vector Strobe Count ({}) mismatch.".format(self.output_pincount + self.bidir_pincount + self.observe_pincount, self.vectorstrobe_count))))
            
            for pin in self.bidirpinlist + self.outputpinlist + self.observepinlist:
                if pin not in self.vectorstrobehighlist + self.vectorstrobelowlist:
                     rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.1", category = "ERROR", desc = self.format_violation("Output Pin ({}) not strobed.".format(pin))))
            
            for vectorstrobe in self.vectorstrobehighlist + self.vectorstrobelowlist:
                if vectorstrobe not in self.bidirpinlist + self.outputpinlist + self.observepinlist:
                     rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.1", category = "ERROR", desc = self.format_violation("Non-output Pin ({}) strobed.".format(vectorstrobe))))

        return rulesFieldList
    
    #Rule2.2: Control bit set to safe for output test
    def Rule2_2(self):
        
        rulesFieldList = []

        for spfObj in self.spfObjList:
            if spfObj.is_controlsafe():
                rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.2", line = self.spfObjList.index(spfObj), category = "ERROR", desc = self.format_violation("Control bit set to safe for output test.")))

        return rulesFieldList
    
    #Rule2.3: Vector Strobe RPT count less than 10
    def Rule2_3(self):

        rulesFieldList = []

        for spfObj in self.spfObjList:
            if not spfObj.is_vectorstroberptcountmorethan10():
                rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.3", line = self.spfObjList.index(spfObj), category = "WARNING", desc = self.format_violation("Vector Strobe RPT count ({}) less than 10.".format(spfObj.rpt))))

        return rulesFieldList
    
    #Rule2.4: Pin Vector Strobing without H->L/ L->H transition
    def Rule2_4(self):

        rulesFieldList = []

        vectorStrobe_Dict = {}
        for spfObj in self.spfObjList:          
            if spfObj.is_vectorstrobehigh():
                if spfObj.field not in vectorStrobe_Dict:
                    vectorStrobe_Dict[spfObj.field] = ['H']  
                else:
                    vectorStrobe_Dict[spfObj.field].append('H')

            if spfObj.is_vectorstrobelow():
                if spfObj.field not in vectorStrobe_Dict:
                    vectorStrobe_Dict[spfObj.field] = ['L']  
                else:
                    vectorStrobe_Dict[spfObj.field].append('L')

        for pin in vectorStrobe_Dict.keys():
            transition_index = [i for i in range(1,len(vectorStrobe_Dict[pin])) if vectorStrobe_Dict[pin][i]!=vectorStrobe_Dict[pin][i-1] ]
            if len(transition_index) < 2:
                if vectorStrobe_Dict[pin][0] == 'L':
                    rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.4", category = "ERROR", desc = self.format_violation("No H -> L transition found on pin vector ({})".format(pin))))
                if vectorStrobe_Dict[pin][0] == 'H':
                    rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.4", category = "ERROR", desc = self.format_violation("No L -> H transition found on pin vector ({})".format(pin))))

        return rulesFieldList

    #Rule3.1: Toggle Pin Count not equal to Toggle Pin Vector Strobe Count
    def Rule3_1(self):
        pintoggleDict = {}
        rulesFieldList = []

        for spfObj in self.spfObjList:          
            if spfObj.is_vectorstrobehigh():
                if spfObj.field not in pintoggleDict:
                    pintoggleDict[spfObj.field] = ['H']  
                else:
                    pintoggleDict[spfObj.field].append('H')

            if spfObj.is_vectorstrobelow():
                if spfObj.field not in pintoggleDict:
                    pintoggleDict[spfObj.field] = ['L']  
                else:
                    pintoggleDict[spfObj.field].append('L')

        if self.toggle_pincount != len(pintoggleDict.keys()):
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule3.1", category = "ERROR", desc = self.format_violation("Toggle Support Pin Count ({}) and Pin Vector Strobe Count ({}) mismatch.".format(self.toggle_pincount, len(pintoggleDict.keys())))))

            for pin in self.togglepinlist:
                if pin not in pintoggleDict.keys():
                     rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule3.1", category = "ERROR", desc = self.format_violation("Toggle Pin ({}) not strobed.".format(pin))))
            
            for vectorstrobe in pintoggleDict.keys():
                if vectorstrobe not in self.togglepinlist:
                     rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule3.1", category = "ERROR", desc = self.format_violation("Non-toggle Pin ({}) strobed.".format(vectorstrobe))))
        
        return rulesFieldList

    #Rule6.1: No strobe found for AC RX pin
    def Rule6_1(self):

        rulesFieldList = []

        if self.acrxstrobe_pincount == 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule6.1", category = "ERROR", desc = self.format_violation("AC RX TDO Strobe not found.")))

        return rulesFieldList
    
    #Rule6.2: AC Input Pin Count not equal to AC Input Pin Strobe Count
    def Rule6_2(self):

        rulesFieldList = []

        if self.acrx_pincount != self.acrxstrobe_pincount:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule6.2", category = "ERROR", desc = self.format_violation("AC RX Pin count ({}) and AC RX Pin strobe count ({}) mismatch.".format(self.acrx_pincount,self.acrxstrobe_pincount))))

            for pin in self.acrxpinlist:
                if pin not in self.acrxstrobelist:
                     rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule6.2", category = "ERROR", desc = self.format_violation("AC Input Pin ({}) not strobed.".format(pin))))
            
            for pinstrobe in self.acrxstrobelist:
                if pinstrobe not in self.acrxpinlist:
                     rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule6.2", category = "ERROR", desc = self.format_violation("Non-input AC Pin ({}) strobed.".format(pinstrobe))))

        return rulesFieldList
    
    #Rule6.3: AC Output Pin Count not equal to AC Output Pin Vector Strobe Count
    def Rule6_3(self):

        rulesFieldList = []

        if self.vectorstrobe_count != self.actx_pincount:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule6.3", category = "WARNING", desc = self.format_violation("AC TX Pin Count ({}) and AC TX Pin Vector Strobe Count ({}) mismatch.".format(self.actx_pincount, self.vectorstrobe_count))))

            for pin in self.actxpinlist:
                if pin not in self.vectorstrobelist:
                     rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule6.3", category = "WARNING", desc = self.format_violation("AC Output Pin ({}) not strobed.".format(pin))))
            
            for vectorstrobe in self.vectorstrobelist:
                if vectorstrobe not in self.actxpinlist:
                     rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule6.3", category = "WARNING", desc = self.format_violation("Non-output AC Pin ({}) strobed.".format(vectorstrobe))))
        
        return rulesFieldList
    
    def RuleUndefined(self, rule):
        rulesFieldList = []

        rulesFieldList.append(RulesField(spffile = self.testName, category = "ERROR", desc = "Rule({}) Undefined.".format(rule) ))

        return rulesFieldList
