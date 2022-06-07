from sympy import true


class Param():
    def __init__(self) -> None:
        
        mintheta = 5.5
        maxtheta  = 6.5


        #Resolution der 2d integration
        npt_rad=2048
        npt_azim=72

        #integration range
        radial_range=(0,10)
        #wavelength in 10^1 Ängstrom
        w=0.012037300291262137
        #Abstand der betrachteten ebene bei keiner spannung
        zero=0.11684

        #zu betrachtender peak
        peak = 2

        #norm temp des materials
        starttemp = 20

        #Ebenen spezifische E Module
        E=[220000,165000,220000,220000,181000,148000]

        #Ebenen spezifische possionszahlen (v)
        poisson=[0.28,0.33,0.28,0.28,0.32,0.25]

        #Positions punkte
        ypunkte=[20, 25, 28, 29, 30, 31, 32, 35, 40]
        import numpy as np
        ypunkte = np.array(ypunkte) - 30
        zpunkte = np.linspace(-7.06,-7.36,16)

        thetav=[1.25,2.5,2.94748158,3.5,3.9,4.3]
        
        self.__EModules  = E

        self.__poissonNumbers =poisson

        self.__positionsY = ypunkte
        self.__positionsZ =  zpunkte
        self.__minTheta = mintheta
        self.__maxTheta = maxtheta
        self.__radSteps = npt_rad
        self.__nptAzim = npt_azim
        self.__radialRange = radial_range
        self.__wavelength = w
        self.__temp = starttemp
        self.__thetaAV = thetav
        self.__peak = peak
        self.__d0 = zero
        self.__mode = 1
        from glob import glob
        self.__directoryPaths = [i+"pilatus\\" for i in glob("F:/NextCloud/University/2. FS/EDV/Versuch3/Versuch3/*/", recursive = True) if "v3_insitu" in i]
        self.__azimJsonPath = "insitu20x200.azimint.json"
        self.__progressBarHandles = []
        self.__tasks = ["axisTransform_fit","voigt_fit"]#"azimuthal_integration" "pseudoVoigt_fit" ["azimuthal_integration"]["pseudoVoigt_fit"]
    #Setter
    def setMode(self, mode):
        self.__mode = mode
    def setEModules(self,EModules):
        self.__EModules  = EModules
    def setPoissonNumbers(self, poissonNumbers):
        self.__poissonNumbers =poissonNumbers
    def setPositionsY(self, positionsY):
        self.__positionsY = positionsY
    def setPositionsX(self, positionsZ):
        self.__positionsZ = positionsZ
    def setMinTheta(self, minTheta):
        self.__minTheta = minTheta
    def setMaxTheta(self,maxTheta):
        self.__maxTheta = maxTheta
    def setRadSteps(self,radSteps):
        self.__radSteps = radSteps
    def setNptAzim(self,nptAzim):
        self.__nptAzim = nptAzim
    def setRadialRange(self,radialRange):
        self.__radialRange = radialRange
    def setWavelength(self, wavelength):
        self.__wavelength = wavelength
    def setStartTemp(self, temp):
        self.__temp = temp
    def thetaAV(self, thetaAV):
        self.__thetaAV = thetaAV
    def setPeak(self, peak):
        self.__peak = peak
    def setD0(self, d0):
        self.__d0 = d0
    def setDirectoryPaths(self, directoryPaths):
        self.__directoryPaths = directoryPaths
    def setPathToAzimJson(self, azimJsonPath):
        self.__azimJsonPath = azimJsonPath
    def setProgressBarHandles(self, progressBarHandles):
        self.__progressBarHandles = progressBarHandles
    def setTasks(self,tasks):
        self.__tasks = tasks
        
        

    #Getter
    def getMode(self):
        return self.__mode
    def getIsMultiprocessingAllowed(self):
        return true
    def getIsMultithreadingAllowed(self):
        return true
    def getTasks(self):
        return self.__tasks
    def getEModules(self):
        return self.__EModules 
    def getPoissonNumber(self):
        return self.__poissonNumbers 
    def getPositionsY(self):
        return self.__positionsY
    def getPositionsZ(self):
        return self.__positionsZ 
    def getMinTheta(self):
        return self.__minTheta 
    def getMaxTheta(self):
        return self.__maxTheta 
    def getRadSteps(self):
        return self.__radSteps 
    def getNptAzim(self):
        return self.__nptAzim 
    def getRadialRange(self):
        return self.__radialRange 
    def getWavelength(self):
        return self.__wavelength  
    def getStartTemp(self):
        return self.__temp
    def getThetaAV(self):
        return self.__thetaAV
    def getPeak(self):
        return self.__peak
    def getD0(self):
        return self.__d0
    def getDirectoryPaths(self):
        return self.__directoryPaths
    def getPathToAzimJson(self):
        return self.__azimJsonPath
    def getProgressBarHandles(self):
        return self.__progressBarHandles 
        
    
    #ignore
    ParamRegister = {
        "EModules":getEModules,
        "PoissonNumbers": getPoissonNumber,
        "PositionsX":getPositionsZ,
        "PositionsY":getPositionsY
    }
    