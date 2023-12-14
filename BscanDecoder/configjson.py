class ConfigurationSet:

    def __init__(self,ConfigurationName,ConfigurationPinGroup, measurements):
        self.ConfigurationName = ConfigurationName
        self.ConfigurationPinGroup = ConfigurationPinGroup
        self.Measurements = measurements

    def __repr__(self):
        return "ConfigName: {}, ConfigPinGrp: {}, Measurements: {}"\
            .format(self.ConfigurationName, self.ConfigurationPinGroup, self.Measurements)

class Measurements:

    def __init__(self,measurementgroup,measurementpingroup, settings):
        self.MeasurementGroup = measurementgroup
        self.MeasurementPinGroup = measurementpingroup
        self.Settings = settings

    def __repr__(self):
        return "MeasurementGroup: {}, MeasurementPinGroup: {}, Settings:{} "\
            .format(self.MeasurementGroup, self.MeasurementPinGroup, self.Settings)


class Settings:

    def __init__(self, pinlist, pinsetting):
        self.Pins = pinlist
        self.PinSetting = pinsetting

    def __repr__(self):
        return "Pins: {}, PinSetting: {}"\
            .format(self.Pins, self.PinSetting)


class PinSetting:

    def __init__(self,forcehigh, forcelow, irange, limithigh, limitlow, clamphigh, clamplow):
        self.ClampHigh = clamphigh
        self.ClampLow = clamplow
        self.ForceHigh = forcehigh
        self.ForceLow = forcelow
        self.IRange = irange
        self.LimitHigh = limithigh
        self.LimitLow = limitlow
        self.ClampHigh = clamphigh
        self.ClampLow = clamplow

    def __repr__(self):
        return "ForceHigh: {}, ForceLow: {}, IRange: {}, LimitHigh: {}, LimitLow: {}, ClampHigh:{}, ClampLow:{}"\
            .format(self.ForceHigh,self.ForceLow,self.IRange,self.LimitHigh,self.LimitLow,self.ClampHigh,self.ClampLow)

