from Tasks.AxisTransformationFitTask import AxisTransformationTask
from Tasks.AzimuthalIntegrationTask import AzimuthalIntegrationTask
from Tasks.PseudoVoigtFitTask import PseudoVoigtFitTask

from Utils.Param import param

taskRegister = {
    AzimuthalIntegrationTask.getFuncName(): {
                "description": AzimuthalIntegrationTask.getDescription(),
                "dependencies": AzimuthalIntegrationTask.getDependencies(),
                "input_params": [param.getOutputDirectory,param.getElabFtwJson,param.getRadSteps,param.getNptAzim,param.getRadialRange,param.getPathToAzimJson,param.getDirectoryPaths,param.getProgressBarHandles],
                "handle":AzimuthalIntegrationTask.runTask,
                "MultiProcessing":True        
    },
    PseudoVoigtFitTask.getFuncName(): {
                "description": "doesABC",
                "dependencies": PseudoVoigtFitTask.getDependencies(),
                "input_params": [param.getOutputDirectory,param.getElabFtwJson,param.getMinTheta,param.getMaxTheta,param.getDirectoryPaths,param.getThetaAV,param.getPeak,param.getProgressBarHandles],
                "handle":PseudoVoigtFitTask.runTask,
                "MultiProcessing":True        
    },
    "axisTransform_fit": {
                "description": "do axis transform",
                "dependencies": {PseudoVoigtFitTask.getFuncName():1},
                "input_params": [param.getOutputDirectory,param.getElabFtwJson,param.getDirectoryPaths,param.getWavelength,param.getPeak,param.getEModules,param.getPoissonNumber,param.getD0,param.getPositionsZ,param.getPositionsY,param.getProgressBarHandles],
                "handle":AxisTransformationTask.runTask,
                "MultiProcessing":True    
    }
}
    
