import pyFAI

class AzimuthalIntegrator:

        def __init__(self, azimIntegrator_settingJson, args):
            """Load azimuthal integrator settings from json file and sets callArguments

            Args:
                azimIntegrator_settingJson (string): path to azimuthalIntegration setting json
                args (list): additional call arguments like npt_azim etc. (See: https://pyfai.readthedocs.io/en/master/api/pyFAI.html#module-pyFAI.azimuthalIntegrator)
            """
            self.__pyFAI_azimIntegrator  = pyFAI.load(azimIntegrator_settingJson)
            self.__pyFAI_callArgs = args
        
        def integrate2D(self,detectorFile,filename):
            """Does a azimuthal integration of passed detector file

            Args:
                detectorFile (fabioimage): fabioimage instance (See: https://pythonhosted.org/fabio/getting_started.html)
                filename (string): filename of detector file

            Returns:
                list: integration results
            """            ""
            azimData = self.__pyFAI_azimIntegrator.integrate2d_ng(data=detectorFile.data, npt_rad=self.__pyFAI_callArgs[0],npt_azim=self.__pyFAI_callArgs[1],radial_range= (0,10),unit="2th_deg",filename=filename)
            return [*azimData]