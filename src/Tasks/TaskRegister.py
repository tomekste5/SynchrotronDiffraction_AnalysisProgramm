
from Tasks.AxisTransformationFitTask import AxisTransformationTask
from Tasks.AzimuthalIntegrationTask import AzimuthalIntegrationTask
from Tasks.VoigtFitTask import VoigtFitTask

from Utils.Param import Param

taskRegister = {
    AzimuthalIntegrationTask.getFuncName(): {
                "description": AzimuthalIntegrationTask.getDescription(),
                "dependencies": AzimuthalIntegrationTask.getDependencies(),
                "input_params": [Param.getRadSteps,Param.getNptAzim,Param.getRadialRange,Param.getPathToAzimJson,Param.getDirectoryPaths,Param.getIsMultiprocessingAllowed,Param.getMode,Param.getProgressBarHandles],
                "handle":AzimuthalIntegrationTask.runTask,         
    },
    VoigtFitTask.getFuncName(): {
                "description": "doesABC",
                "dependencies": VoigtFitTask.getDependencies(),
                "input_params": [Param.getMinTheta,Param.getMaxTheta,Param.getDirectoryPaths,Param.getIsMultiprocessingAllowed,Param.getThetaAV,Param.getPeak,Param.getMode,Param.getProgressBarHandles],
                "handle":VoigtFitTask.runTask,        
    },
    "axisTransformFit": {
                "description": "do axis transform",
                "dependencies": {AxisTransformationTask.getFuncName():1},
                "input_params": [Param.getMinTheta,Param.getDirectoryPaths,Param.getIsMultiprocessingAllowed,Param.getWavelength,Param.getPeak,Param.getEModules,Param.getPoissonNumber,Param.getD0,Param.getPositionsZ,Param.getPositionsY,Param.getProgressBarHandles],
                "handle":AxisTransformationTask.runTask,        
    }
}
    