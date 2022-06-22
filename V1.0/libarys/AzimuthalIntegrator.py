import pyFAI

class AzimuthalIntegrator:

        def __init__(self, settingJson, args):
            self.__pyFAI_azimIntegrator  = pyFAI.load(settingJson)
            self.__pyFAI_callArgs = args
        
        def integrate2D(self,detectorData,filename):
            azimData = self.__pyFAI_azimIntegrator.integrate2d_ng(data=detectorData.data, npt_rad=self.__pyFAI_callArgs[0],npt_azim=self.__pyFAI_callArgs[1],radial_range=self.__pyFAI_callArgs[2],unit="2th_deg",filename=filename)
            return [*azimData]