
from Tasks.AxisTransformationFitTask import AxisTransformationTask
from Tasks.AzimuthalIntegrationTask import AzimuthalIntegrationTask
from Tasks.VoigtFitTask import VoigtFitTask

from Utils.Param import Param

taskRegister = {
    AzimuthalIntegrationTask.getFuncName(): {
                "description": AzimuthalIntegrationTask.getDescription(),
                "dependencies": AzimuthalIntegrationTask.getDependencies(),
                "input_params": [Param.getOutputDirectory,Param.getRadSteps,Param.getNptAzim,Param.getRadialRange,Param.getPathToAzimJson,Param.getDirectoryPaths,Param.getProgressBarHandles],
                "handle":AzimuthalIntegrationTask.runTask,
                "logging":True        
    },
    VoigtFitTask.getFuncName(): {
                "description": "doesABC",
                "dependencies": VoigtFitTask.getDependencies(),
                "input_params": [Param.getOutputDirectory,Param.getMinTheta,Param.getMaxTheta,Param.getDirectoryPaths,Param.getThetaAV,Param.getPeak,Param.getProgressBarHandles],
                "handle":VoigtFitTask.runTask,
                "logging":True        
    },
    "axisTransform_fit": {
                "description": "do axis transform",
                "dependencies": {VoigtFitTask.getFuncName():1},
                "input_params": [Param.getOutputDirectory,Param.getMinTheta,Param.getDirectoryPaths,Param.getWavelength,Param.getPeak,Param.getEModules,Param.getPoissonNumber,Param.getD0,Param.getPositionsZ,Param.getPositionsY,Param.getProgressBarHandles],
                "handle":AxisTransformationTask.runTask,
                "logging":True    
    }
}
    
