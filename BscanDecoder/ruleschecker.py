class RulesField:

    def __init__(self, spffile = "", rule = "", line = "", category = "", pin = "", desc = "", reference = ""):
        self.spffile = spffile
        self.rule = rule
        self.line = line
        self.category = category
        self.pin = pin
        self.desc = desc
        self.reference = reference
        self.justification = None

    def __repr__(self):
       return "SPF:{} RULE:{} Line:{}, Category:{}, Desc:{}".format(self.spffile, self.rule, self.line, self.category, self.desc)

class TestSummaryField:

    def __init__(self, spffile = "", input_pin = "", output_pin = "",  bidir_pin = "", observe_pin = "", vector_strobeH = "",  vector_strobeL = "", vector_force1 = "", vector_force0 = "", tdo_strobe = "", pin_label = "", rules = "", status = ''):
        self.spffile = spffile
        self.input_pin = input_pin
        self.output_pin = output_pin
        self.bidir_pin = bidir_pin
        self.observe_pin = observe_pin
        self.vector_strobeH = vector_strobeH
        self.vector_strobeL = vector_strobeL
        self.vector_force1 = vector_force1
        self.vector_force0 = vector_force0
        self.tdo_strobe = tdo_strobe
        self.pin_label = pin_label
        self.rules = rules
        self.status = status

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
        self.actxdiffpinlist = []
        self.togglepinlist = []
        self.nochannelpinlist = []
        self.pinlabellist = []
        self.vectorstrobehighlist = []
        self.vectorstrobelowlist = []
        self.vectorforcehighlist = []
        self.vectorforcelowlist = []
        self.bidir_strobe_list = []
        self.input_strobe_list = []
        self.bsdl_strobe_list = []
        self.acrxstrobelist = []
        self.differential_output = []

        for obj in self.bsdlObjList:
            #store with bsdl name
            if obj.is_input() and obj.channel == True:
                self.inputpinlist.append(obj.port)
            if obj.is_bidir() and obj.channel == True:
                self.bidirpinlist.append(obj.port)
            if obj.is_output() and obj.channel == True:
                self.outputpinlist.append(obj.port)
            if obj.is_observe() and obj.channel == True:
                self.observepinlist.append(obj.port)
            if obj.is_togglepin() and obj.channel == True:
                self.togglepinlist.append(obj.port)
            if obj.is_differential_output():
                self.differential_output.append(obj.differential)
            if obj.is_acrx() and obj.channel == True:
                self.acrxpinlist.append(obj.port)
            if obj.is_actx() and obj.channel == True:
                self.actxpinlist.append(obj.port)
            if obj.is_actx() and obj.channel == True:
                if obj.differential:
                    self.actxdiffpinlist.append(obj.differential.port)
            
            if obj.channel == False:
                self.nochannelpinlist.append(obj.pinmap)

        self.input_pincount = len(set(self.inputpinlist))
        self.output_pincount = len(set(self.outputpinlist))
        self.bidir_pincount = len(set(self.bidirpinlist))
        self.observe_pincount = len(set(self.observepinlist))
        self.acrx_pincount = len(set(self.acrxpinlist))
        self.actx_pincount = len(set(self.actxpinlist))
        self.toggle_pincount = len(set(self.togglepinlist))
        

        for obj in self.spfObjList:
            if obj.is_vectorstrobehigh():
                if obj.field not in self.vectorstrobehighlist:
                    self.vectorstrobehighlist.append(obj.field)
            if obj.is_vectorstrobelow():
                if obj.field not in self.vectorstrobelowlist:
                    self.vectorstrobelowlist.append(obj.field)
            if obj.is_vectorforcehigh():
                if obj.field not in self.vectorforcehighlist:
                    self.vectorforcehighlist.append(obj.field)
            if obj.is_vectorforcelow():
                if obj.field not in self.vectorforcelowlist:
                    self.vectorforcelowlist.append(obj.field) 
            if obj.is_pinlabel():
                if obj.field not in self.pinlabellist:
                    self.pinlabellist.append(obj.field)
            if obj.is_strobe() and obj.channel == True:
                if obj.field not in self.bsdl_strobe_list:
                    self.bsdl_strobe_list.append(obj.field)
            if obj.is_inputstrobe() and obj.channel == True:
                if obj.field not in self.input_strobe_list:
                    self.input_strobe_list.append(obj.field)
            if obj.is_bidirstrobe() and obj.channel == True:
                if obj.field not in self.bidir_strobe_list:
                    self.bidir_strobe_list.append(obj.field)
            if obj.is_acrxstrobe():
                if obj.field not in self.acrxstrobelist:
                    self.acrxstrobelist.append(obj.field)

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

        inputnostrobe = []
        bidirnostrobe = []
        noninputstrobe = []


        for bsdlpin in self.inputpinlist:
            #bsdlpin = [obj.port for obj in self.bsdlObjList if obj.pinmap == pin or obj.pinmap == pin.upper()][0]
            if bsdlpin not in self.bsdl_strobe_list:
                if bsdlpin not in inputnostrobe:
                    inputnostrobe.append(bsdlpin)
                    
        for bsdlpin in self.bidirpinlist:
            #bsdlpin = [obj.port for obj in self.bsdlObjList if obj.pinmap == pin or obj.pinmap == pin.upper()][0]
            if bsdlpin not in self.bsdl_strobe_list:
                if bsdlpin not in bidirnostrobe:
                    bidirnostrobe.append(bsdlpin)

        for bsdlpinstrobe in self.bsdl_strobe_list:
            #pin = [obj.pinmap.lower() for obj in self.bsdlObjList if obj.port == pinstrobe or obj.port == pinstrobe.upper()][0]
            if bsdlpinstrobe not in self.inputpinlist + self.bidirpinlist:
                if bsdlpinstrobe not in noninputstrobe:
                    noninputstrobe.append(bsdlpinstrobe)
        
        if len(inputnostrobe) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.1", category = "ERROR", pin = str(inputnostrobe), desc = self.format_violation("({}) Input Pin not strobed.".format(len(inputnostrobe)))))
        
        if len(bidirnostrobe) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.1", category = "ERROR", pin = str(bidirnostrobe), desc = self.format_violation("({}) Bidir Pin not strobed.".format(len(bidirnostrobe)))))
           
        if len(noninputstrobe) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.1", category = "ERROR", pin = str(noninputstrobe), desc = self.format_violation("({}) non Input/Bidir Function Pin strobed.".format(len(noninputstrobe)))))

        if len(rulesFieldList) == 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.1", category = "PASS", desc = "Pin Strobe Count match with Input/Bidir Pin Count."))
        
        return rulesFieldList
    
    #Rule1.2: Input Pin Strobe Count not equal to Input Pin Force Count
    def Rule1_2(self):
        rulesFieldList = []

        inputstrobe_noforce = []
        bidirstrobe_noforce = []
        diffpin_nostrobe = []
        pinforce_nostrobe = []

        for bsdlpinstrobe in self.input_strobe_list:
            pin_obj = [obj for obj in self.bsdlObjList if obj.port == bsdlpinstrobe][0]
            testerpin = pin_obj.pinmap
            
            if testerpin not in self.vectorforcelowlist + self.vectorforcehighlist:
                if bsdlpinstrobe not in inputstrobe_noforce:
                    inputstrobe_noforce.append(bsdlpinstrobe)
            
            elif pin_obj.differential:
                if testerpin in self.vectorforcelowlist:
                    if pin_obj.differential.pinmap not in self.vectorforcehighlist:
                        if pin_obj.differential.pinmap not in diffpin_nostrobe:
                            diffpin_nostrobe.append(pin_obj.differential.pinmap)

                elif testerpin in self.vectorforcehighlist:
                    if pin_obj.differential.pinmap not in self.vectorforcelowlist:
                        if pin_obj.differential.pinmap not in diffpin_nostrobe:
                            diffpin_nostrobe.append(pin_obj.differential.pinmap)
        
        for bsdlpinstrobe in self.bidir_strobe_list:
            pin_obj = [obj for obj in self.bsdlObjList if obj.port == bsdlpinstrobe][0]
            testerpin = pin_obj.pinmap

            if testerpin not in self.vectorforcelowlist + self.vectorforcehighlist:
                if bsdlpinstrobe not in bidirstrobe_noforce:
                    bidirstrobe_noforce.append(bsdlpinstrobe)

            elif pin_obj.differential:
                if testerpin in self.vectorforcelowlist:
                    if pin_obj.differential.pinmap not in self.vectorforcehighlist:
                        if pin_obj.differential.pinmap not in diffpin_nostrobe:
                            diffpin_nostrobe.append(pin_obj.differential.pinmap)

                elif testerpin in self.vectorforcehighlist:
                    if pin_obj.differential.pinmap not in self.vectorforcelowlist:
                        if pin_obj.differential.pinmap not in diffpin_nostrobe:
                            diffpin_nostrobe.append(pin_obj.differential.pinmap)
        
        for vectorforce in self.vectorforcelowlist + self.vectorforcehighlist:
            try:
                bsdlpinstrobe = [obj.port for obj in self.bsdlObjList if obj.pinmap == vectorforce][0]
                if bsdlpinstrobe not in self.bsdl_strobe_list:
                    if vectorforce not in pinforce_nostrobe:
                        pinforce_nostrobe.append(vectorforce)
            except:
                rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.2", category = "WARNING", pin = vectorforce, desc = self.format_violation("Unable to map vector ({}) to all pin channel.".format(vectorforce))))
                continue
        
        if len(inputstrobe_noforce) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.2", category = "ERROR", pin = str(inputstrobe_noforce), desc = self.format_violation("({}) Input Pin strobed without forcing.".format(len(inputstrobe_noforce)))))

        if len(bidirstrobe_noforce) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.2", category = "ERROR", pin = str(bidirstrobe_noforce), desc = self.format_violation("({}) Bidir Pin strobed without forcing.".format(len(bidirstrobe_noforce)))))

        if len(diffpin_nostrobe) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.2", category = "ERROR", pin = str(diffpin_nostrobe), desc = self.format_violation("({}) Differential Pin not forced with opposite state.".format(len(diffpin_nostrobe))), reference = 'https://hsdes.intel.com/appstore/article/#/15014071124'))

        if len(pinforce_nostrobe) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.2", category = "WARNING", pin= str(pinforce_nostrobe), desc = self.format_violation("({}) Pin forced without strobing.".format(len(pinforce_nostrobe)))))

        if len(rulesFieldList) == 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.2", category = "PASS", desc = "Pin Force Count match with Input/Bidir Pin Count."))

        return rulesFieldList

    #Rule1.3: Input Pin Strobe Count not equal to Input Pin Label Count
    def Rule1_3(self):

        rulesFieldList = []

        input_nopinlabel = []
        bidir_nopinlabel = []

        for bsdlpinstrobe in self.input_strobe_list:
            testerpin = [obj.socket for obj in self.bsdlObjList if obj.port == bsdlpinstrobe][0]
            if testerpin not in self.pinlabellist:
                if testerpin not in input_nopinlabel:
                    input_nopinlabel.append(testerpin)
         
        for bsdlpinstrobe in self.bidir_strobe_list:
            testerpin = [obj.socket for obj in self.bsdlObjList if obj.port == bsdlpinstrobe][0]
            if testerpin not in self.pinlabellist:
                if testerpin not in bidir_nopinlabel:
                    bidir_nopinlabel.append(testerpin)
        
        if len(self.pinlabellist) != len(self.bsdl_strobe_list):
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.3", category = "ERROR", desc = self.format_violation("Pin label count ({}) mismatch with Pin strobe count({}).".format(len(self.pinlabellist), len(self.bsdl_strobe_list)))))

        if len(input_nopinlabel) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.3", category = "ERROR", pin=str(input_nopinlabel), desc = self.format_violation("Pin Label for ({}) Input Pin not found.".format(len(input_nopinlabel)))))

        if len(bidir_nopinlabel) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.3", category = "ERROR", pin=str(bidir_nopinlabel), desc = self.format_violation("Pin Label for ({}) Bidir Pin not found.".format(len(bidir_nopinlabel)))))


        if len(rulesFieldList) < 1:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.3", category = "PASS", desc = "Pin Strobe Count match with Pin Label Count."))

        return rulesFieldList

    #Rule1.4: Control bit not set to safe for input test
    def Rule1_4(self):
        rulesFieldList = []
        controlbitnotsafe = []

        for spfObj in self.spfObjList:
            if spfObj.is_controlnotsafe():
                controlbitnotsafe.append(self.spfObjList.index(spfObj))

        if len(controlbitnotsafe) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.4", line = str(controlbitnotsafe), category = "ERROR", desc = self.format_violation("Control bit not set to safe for input test.")))

        if len(rulesFieldList) < 1:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule1.4", category = "PASS", desc = "Control bit set to safe for input test."))

        return rulesFieldList
    
    #Rule2.1: Output Pin Count not equal to Output Pin Vector Strobe Count
    def Rule2_1(self):

        rulesFieldList = []
        bidirnostrobe = []
        outputnostrobe = []
        obeservenostrobe =[]
        differentialnostrobe = []
        nochannelstrobe = []
        nonoutputstrobe = []

        for pin in self.bidirpinlist:
            testerpin = [obj.pinmap for obj in self.bsdlObjList if obj.port == pin][0]
            if testerpin not in self.vectorstrobehighlist + self.vectorstrobelowlist:
                if testerpin not in bidirnostrobe:
                    bidirnostrobe.append(testerpin)
        
        for pin in self.outputpinlist:
            testerpin = [obj.pinmap for obj in self.bsdlObjList if obj.port == pin][0]
            if testerpin not in self.vectorstrobehighlist + self.vectorstrobelowlist:
                if testerpin not in outputnostrobe:
                    outputnostrobe.append(testerpin)
        
        for pin in self.observepinlist:
            testerpin = [obj.pinmap for obj in self.bsdlObjList if obj.port == pin][0]
            if testerpin not in self.vectorstrobehighlist + self.vectorstrobelowlist:
                if testerpin not in obeservenostrobe:
                    obeservenostrobe.append(testerpin)
        '''
        for pin in self.differential_output:
            testerpin = [obj.pinmap for obj in self.bsdlObjList if obj.port == pin][0]
            if testerpin not in self.vectorstrobehighlist + self.vectorstrobelowlist:
                if testerpin not in differentialnostrobe:
                    differentialnostrobe.append(testerpin)
        '''
        for pin in self.nochannelpinlist:
            if pin in self.vectorstrobehighlist + self.vectorstrobelowlist:
                if pin not in nochannelstrobe:
                    nochannelstrobe.append(pin)
                    
        for vectorstrobe in self.vectorstrobehighlist + self.vectorstrobelowlist:
            try:
                bsdlpin = [obj.port for obj in self.bsdlObjList if obj.pinmap == vectorstrobe][0]
                if bsdlpin not in self.bidirpinlist + self.outputpinlist + self.observepinlist:
                    if bsdlpin not in nonoutputstrobe:
                        nonoutputstrobe.append(bsdlpin)
            except:
                rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.1", category = "WARNING", pin = vectorstrobe, desc = self.format_violation("Unable to map vector ({}) to all pin channel.".format(vectorstrobe))))
                continue
            

        if self.vectorstrobe_count < self.output_pincount + self.bidir_pincount + self.observe_pincount:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.1", category = "ERROR", desc = self.format_violation("Pin Vector Strobe Count ({}) lesser than Output Pin Count ({}).".format(self.vectorstrobe_count, self.output_pincount + self.bidir_pincount + self.observe_pincount))))
            
        if len(bidirnostrobe) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.1", category = "ERROR", pin = str(bidirnostrobe), desc = self.format_violation("({}) Bidir Pin not strobed.".format(len(bidirnostrobe)))))

        if len(outputnostrobe) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.1", category = "ERROR", pin = str(outputnostrobe), desc = self.format_violation("({}) Output Pin not strobed.".format(len(outputnostrobe)))))
        
        if len(obeservenostrobe) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.1", category = "ERROR", pin = str(obeservenostrobe), desc = self.format_violation("({}) Observe_only Pin not strobed.".format(len(obeservenostrobe)))))
        #differential vector strobe checking not enabled
        '''
        if len(differentialnostrobe) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.1", category = "ERROR", pin = str(differentialnostrobe), desc = self.format_violation("({}) Differential Pin not strobed.".format(len(differentialnostrobe)))))
        '''
        if len(nochannelstrobe) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.1", category = "ERROR", pin = str(nochannelstrobe), desc = self.format_violation("({}) Pin without tester channel strobed.".format(len(nochannelstrobe)))))
        
        if len(nonoutputstrobe) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.1", category = "ERROR", pin = str(nonoutputstrobe), desc = self.format_violation("({}) Non-Output Pin strobed.".format(len(nonoutputstrobe)))))
        
        if len(rulesFieldList) == 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.1", category = "PASS", desc = "Output Pin Count match with Output Pin Vector Strobe Count."))

        return rulesFieldList
    
    #Rule2.2: Control bit set to safe for output test
    def Rule2_2(self):
        
        rulesFieldList = []
        controlbitsafe = []

        for spfObj in self.spfObjList:
            if spfObj.is_controlsafe():
                controlbitsafe.append(self.spfObjList.index(spfObj))

        if len(controlbitsafe) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.2", line = str(controlbitsafe), category = "ERROR", desc = self.format_violation("Control bit set to safe for output test.")))
        
        if len(rulesFieldList) == 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.2", category = "PASS", desc = "Control bit set opposite of safe for output test."))

        return rulesFieldList
    
    #Rule2.3: Vector Strobe RPT count less than 10
    def Rule2_3(self):

        rulesFieldList = []

        vectorstroberptcountmorethan10_list = []

        for spfObj in self.spfObjList:
            if not spfObj.is_vectorstroberptcountmorethan10():
                if spfObj.pinmap not in vectorstroberptcountmorethan10_list:
                    vectorstroberptcountmorethan10_list.append(spfObj.pinmap) 
        
        if len(vectorstroberptcountmorethan10_list) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.3", line = self.spfObjList.index(spfObj), category = "WARNING", pin = str(vectorstroberptcountmorethan10_list), desc = self.format_violation("Found ({}) pin vector(s) have less than 10 RPT count.".format(len(vectorstroberptcountmorethan10_list)))))

        return rulesFieldList
    
    #Rule2.4: Pin Vector Strobing without H->L/ L->H transition
    def Rule2_4(self):

        rulesFieldList = []
        nohightolowpin = []
        nolowtohighpin = []

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
                    if pin not in nohightolowpin:
                        nohightolowpin.append(pin)
                if vectorStrobe_Dict[pin][0] == 'H':
                    if pin not in nolowtohighpin:
                        nolowtohighpin.append(pin)
        
        if len(nohightolowpin) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.4", category = "ERROR", pin = str(nohightolowpin), desc = self.format_violation("({}) Pin vector without H -> L transition.".format(len(nohightolowpin)))))

        if len(nolowtohighpin) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.4", category = "ERROR", pin = str(nolowtohighpin), desc = self.format_violation("({}) Pin vector without L -> H transition.".format(len(nolowtohighpin)))))

        if len(rulesFieldList) == 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.4", category = "PASS", desc = "H->L & L->H transition found for vector strobe pin."))

        return rulesFieldList

    #Rule2.5: Pin Vector Strobing not initiate with min 20 cycles of vector X
    def Rule2_5(self):

        rulesFieldList = []

        vectorStrobe_Dict = {}

        vectorXRpt_Dict = {}

        noX_pinList = []

        Xrptlessthan20_pinList = []

        for spfObj in self.spfObjList:          
            if spfObj.is_vectorstrobehigh():
                if spfObj.field in vectorStrobe_Dict:
                    vectorStrobe_Dict[spfObj.field].append('H')
                else:
                    vectorStrobe_Dict[spfObj.field] = ['H'] 

            elif spfObj.is_vectorstrobelow():
                if spfObj.field in vectorStrobe_Dict:
                     vectorStrobe_Dict[spfObj.field].append('L')
                else:
                    vectorStrobe_Dict[spfObj.field] = ['L']
                    
            elif spfObj.is_vectorstrobeX():
                if spfObj.field not in vectorXRpt_Dict:
                    vectorXRpt_Dict[spfObj.field] = spfObj.rpt

                if spfObj.field in vectorStrobe_Dict:
                     vectorStrobe_Dict[spfObj.field].append('X')
                else:
                    vectorStrobe_Dict[spfObj.field] = ['X']

        for pin in vectorStrobe_Dict.keys():
           
            if vectorStrobe_Dict[pin][0] != "X":
                noX_pinList.append(pin)

        for pin in vectorXRpt_Dict.keys():

            if int(vectorXRpt_Dict[pin]) < 20:
                Xrptlessthan20_pinList.append(pin)
        
        if len(noX_pinList) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.5", category = "ERROR", 
                                            desc = self.format_violation("Pin [{}] Strobe is not initiate with vector X.".format(noX_pinList)),
                                            reference = "https://hsdes.intel.com/appstore/article/#/15014071118"))

        if len(Xrptlessthan20_pinList) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.5", category = "ERROR", 
                                            desc = self.format_violation("Pin [{}] initiate with vector X less than 20 cycles.".format(Xrptlessthan20_pinList)),
                                            reference = "https://hsdes.intel.com/appstore/article/#/15014071118"))
        
        if len(noX_pinList) == 0 and len(Xrptlessthan20_pinList) == 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule2.5", category = "PASS", 
                                            desc = "All Pin Strobe is initiate with min 20 cycles of vector X.",
                                            reference = "https://hsdes.intel.com/appstore/article/#/15014071118"))

        return rulesFieldList

    #Rule3.1: Toggle Pin Count not equal to Toggle Pin Vector Strobe Count
    def Rule3_1(self):
        pintoggleDict = {}
        rulesFieldList = []

        togglepin_nostrobe = []
        nontogglepin_strobe = []

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

        for bsdlpin in self.togglepinlist:
            testerpin = [obj.pinmap for obj in self.bsdlObjList if obj.port == bsdlpin][0]
            if testerpin not in pintoggleDict.keys():
                if bsdlpin not in togglepin_nostrobe:
                    togglepin_nostrobe.append(bsdlpin)
                     
        for vectorstrobe in pintoggleDict.keys():
            try:
                bsdlpin = [obj.port for obj in self.bsdlObjList if obj.pinmap == vectorstrobe][0]
                if bsdlpin not in self.togglepinlist:
                    if bsdlpin not in nontogglepin_strobe:
                        nontogglepin_strobe.append(bsdlpin)
            except:
                rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule3.1", category = "WARNING", pin = vectorstrobe, desc = self.format_violation("Unable to map vector ({}) to all pin channel.".format(vectorstrobe))))
            
        if len(togglepin_nostrobe) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule3.1", category = "ERROR", pin = str(togglepin_nostrobe), desc = self.format_violation("({}) Toggle Pin not strobed.".format(len(togglepin_nostrobe)))))
        
        if len(nontogglepin_strobe) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule3.1", category = "WARNING", pin = str(nontogglepin_strobe) ,desc = self.format_violation("({}) Non-toggle Pin strobed.".format(len(nontogglepin_strobe)))))

        if len(rulesFieldList) == 1:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule3.1", category = "PASS", desc = "Toggle Pin Count match with Toggle Pin Vector Strobe Count."))

        return rulesFieldList

    #Rule6.1: No strobe found for AC RX pin
    def Rule6_1(self):

        rulesFieldList = []

        if self.acrxstrobe_pincount == 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule6.1", category = "ERROR", desc = self.format_violation("AC RX TDO Strobe not found.")))
        else:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule6.1", category = "PASS", desc = "AC Input/Observe_only TDO Strobe found."))

        return rulesFieldList
    
    #Rule6.2: AC Input Pin Count not equal to AC Input Pin Strobe Count
    def Rule6_2(self):

        rulesFieldList = []
        acrx_nostrobe = []
        nonacrx_strobe = []

        for bsdlpin in self.acrxpinlist:
            if bsdlpin not in self.acrxstrobelist:
                acrx_nostrobe.append(bsdlpin)
            
        for pinstrobe in self.acrxstrobelist:
            if pinstrobe not in self.acrxpinlist:
                nonacrx_strobe.append(pinstrobe)
        
        if len(acrx_nostrobe) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule6.2", category = "ERROR", pin = str(acrx_nostrobe), desc = self.format_violation("({}) AC Input Pin not strobed.".format(len(acrx_nostrobe)))))

        if len(nonacrx_strobe) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule6.2", category = "WARNING", pin = str(nonacrx_strobe), desc = self.format_violation("({}) Non-input AC Pin strobed.".format(len(nonacrx_strobe)))))

        if len(rulesFieldList) < 1:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule6.2", category = "PASS", desc = "AC Input Pin Count match with AC Input Pin Strobe Count."))

        return rulesFieldList
    
    #Rule6.3: AC Output Pin Count not equal to AC Output Pin Vector Strobe Count
    def Rule6_3(self):

        rulesFieldList = []

        actxvector_nostrobe = []
        actxdiffvector_nostrobe = []
        nonactxvector_strobe = []

        for bsdlpin in self.actxpinlist:
            testerpin = [obj.pinmap for obj in self.bsdlObjList if obj.port == bsdlpin][0]
            if testerpin not in self.vectorstrobelist:
                if testerpin not in actxvector_nostrobe:
                    actxvector_nostrobe.append(testerpin)

        for bsdlpin in self.actxdiffpinlist:
            for obj in self.bsdlObjList:
                if obj.differential:
                    if obj.differential.port == bsdlpin:
                        testerpin = obj.differential.pinmap
            
            if testerpin not in self.vectorstrobelist:
                if testerpin not in actxdiffvector_nostrobe:
                    actxdiffvector_nostrobe.append(testerpin)
                
        for vectorstrobe in self.vectorstrobelist:
            try:
                bsdlpin = [obj.port for obj in self.bsdlObjList if obj.pinmap == vectorstrobe][0]
                if bsdlpin not in self.actxpinlist + self.actxdiffpinlist:
                    if bsdlpin not in nonactxvector_strobe:
                        nonactxvector_strobe.append(bsdlpin)
            except:
                rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule6.3", category = "WARNING", pin = vectorstrobe, desc = self.format_violation("Unable to map vector ({}) to bsdl port.".format(vectorstrobe))))

        if len(actxvector_nostrobe + actxdiffvector_nostrobe) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule6.3", category = "ERROR", pin = str(actxvector_nostrobe + actxdiffvector_nostrobe), desc = self.format_violation("({}) AC Output Pin not strobed.".format(len(actxvector_nostrobe + actxdiffvector_nostrobe)))))

        if len(nonactxvector_strobe) > 0:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule6.3", category = "WARNING", pin = str(nonactxvector_strobe), desc = self.format_violation("({}) Non-output AC Pin strobed.".format(len(nonactxvector_strobe)))))

        if len(rulesFieldList) < 1:
            rulesFieldList.append(RulesField(spffile = self.testName, rule = "Rule6.3", category = "PASS", desc = "AC Output Pin Count match with AC Output Pin Vector Strobe Count."))

        return rulesFieldList
    
    def RuleUndefined(self, rule):
        rulesFieldList = []

        rulesFieldList.append(RulesField(spffile = self.testName, category = "ERROR", desc = "Rule({}) Undefined.".format(rule) ))

        return rulesFieldList
