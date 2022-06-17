from Tasks.AxisTransformationFitTask import AxisTransformationTask
from Tasks.AzimuthalIntegrationTask import AzimuthalIntegrationTask
from Tasks.PseudoVoigtFitTask import PseudoVoigtFitTask
from Tasks.Config import TaskConfigs

from Utils.Param import Param

taskRegister = {
    AzimuthalIntegrationTask.getFuncName(): {
                "description": AzimuthalIntegrationTask.getDescription(),
                "dependencies": AzimuthalIntegrationTask.getDependencies(),
                "input_params": [Param.getOutputDirectory,Param.getRadSteps,Param.getNptAzim,Param.getRadialRange,Param.getPathToAzimJson,Param.getDirectoryPaths,Param.getProgressBarHandles],
                "handle":AzimuthalIntegrationTask.runTask,
                "MultiProcessing":True        
    },
    PseudoVoigtFitTask.getFuncName(): {
                "description": "doesABC",
                "dependencies": PseudoVoigtFitTask.getDependencies(),
                "input_params": [Param.getOutputDirectory,Param.getMinTheta,Param.getMaxTheta,Param.getDirectoryPaths,Param.getThetaAV,Param.getPeak,Param.getProgressBarHandles],
                "handle":PseudoVoigtFitTask.runTask,
                "MultiProcessing":True        
    },
    "axisTransform_fit": {
                "description": "do axis transform",
                "dependencies": {PseudoVoigtFitTask.getFuncName():1},
                "input_params": [Param.getOutputDirectory,Param.getMinTheta,Param.getDirectoryPaths,Param.getWavelength,Param.getPeak,Param.getEModules,Param.getPoissonNumber,Param.getD0,Param.getPositionsZ,Param.getPositionsY,Param.getProgressBarHandles],
                "handle":AxisTransformationTask.runTask,
                "MultiProcessing":True    
    }
}
    
