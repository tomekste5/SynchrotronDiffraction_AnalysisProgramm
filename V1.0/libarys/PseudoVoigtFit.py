import numpy as np
from scipy.optimize import curve_fit

def pseudoVoigtFunction(x, *p):
    """Computes Pseudo-Voigt function for given x and constant values Pseudo-Voigt function

    Args:
        x (list): list of 2 Theta values

    Returns:
        np.array: pseudoVoigt(x)
    """
    LorCoeff, A, x0,FWHM,a,b = p
    
    return (LorCoeff*A*(1/(1+((x-x0)/(FWHM/2))**2))+(1-LorCoeff)*A*np.exp(-np.log(2)*((x-x0)/(FWHM/2))**2))+a*x+b

def doFit(intensity,twoTheta,thetaPeak):
    """Fits a pseudo-voig function to given intensity curve in 2 Theta domain

    Args:
        intensity (list): intensity values
        twoTheta (list): twoTheta values
        thetaPeak (list): initialGuess for peak position

    Returns:
        dictionary: A Dictionary which contains the chosen constants of the fit as well as there errors
    """
        
    initialGuess =np.array([0, np.max(intensity)-np.min(intensity), thetaPeak*2, 0.028, 0, np.min(intensity)])
        
    param, param_covariance = curve_fit(pseudoVoigtFunction,twoTheta,intensity,initialGuess,ftol=10**(-10))
    param_error = np.sqrt(np.diag(param_covariance))
        
    return {"LorCoeff":param[0],"A":param[1],"x0":param[2],"FWHM":param[3],"LorCoeff_Err":param_error[0],"A_Err":param_error[1],"x0_Err":param_error[2],"FWHM_Err":param_error[3]}