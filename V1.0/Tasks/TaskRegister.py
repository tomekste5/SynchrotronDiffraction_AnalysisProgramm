from Tasks.AxisTransformationFitTask import AxisTransformationTask
from Tasks.AzimuthalIntegrationTask import AzimuthalIntegrationTask
from Tasks.PseudoVoigtFitTask import PseudoVoigtFitTask

from Utils.Param import Param
from Tasks.Config import TaskConfigs

"""If u have written a new Task please follow these steps:
    Example Entry:
    
    ,taskName: {
                "description": "does nothing",
                "dependencies": {"task2Name":1}, 
                "input_params": [Param.getOutputDirectory],
                "handle":YourTaskClass.runTask,
                "MultiProcessing":False        
    }


    1. Copy the example entry in the task register then replace all values with your real ones. 
    2. If a TaskConfig of the new task is already present in TaskConfigs one can use function calls as seen below
"""

taskRegister = {
    TaskConfigs.AzimuthalIntegrationTask_Config.taskName: {
                "description":TaskConfigs.AzimuthalIntegrationTask_Config.taskDescription,
                "dependencies": TaskConfigs.AzimuthalIntegrationTask_Config.taskDependencies,
                "input_params": [Param.getGUIInstance,Param.getOutputDirectory,Param.getElabFtwJson,Param.getRadSteps,Param.getNptAzim,Param.getRadialRange,Param.getPathToAzimJson,Param.getDirectoryPaths,Param.getProgressBarHandles],
                "handle":AzimuthalIntegrationTask.runTask,
                "MultiProcessing":True        
    },
    TaskConfigs.PseudoVoigtFitTask_Config.taskName: {
                "description": TaskConfigs.PseudoVoigtFitTask_Config.taskDescription,
                "dependencies": TaskConfigs.PseudoVoigtFitTask_Config.taskDependencies,
                "input_params": [Param.getGUIInstance,Param.getOutputDirectory,Param.getElabFtwJson,Param.getMinTheta,Param.getMaxTheta,Param.getDirectoryPaths,Param.getThetaAV,Param.getPeak,Param.getProgressBarHandles],
                "handle":PseudoVoigtFitTask.runTask,
                "MultiProcessing":True        
    },
    TaskConfigs.AxisTransformFitTask_Config.taskName: {
                "description": TaskConfigs.AxisTransformFitTask_Config.taskDescription,
                "dependencies": TaskConfigs.AxisTransformFitTask_Config.taskDependencies,
                "input_params": [Param.getGUIInstance,Param.getOutputDirectory,Param.getElabFtwJson,Param.getDirectoryPaths,Param.getWavelength,Param.getPeak,Param.getEModules,Param.getPoissonNumber,Param.getD0,Param.getPositionsZ,Param.getPositionsY,Param.getProgressBarHandles],
                "handle":AxisTransformationTask.runTask,
                "MultiProcessing":True    
    }
}
    
