import numpy as np
from scipy.optimize import curve_fit

def gauss(x, *p):
    LorCoeff, A, x0,FWHM,a,b = p
    
    return (LorCoeff*A*(1/(1+((x-x0)/(FWHM/2))**2))+(1-LorCoeff)*A*np.exp(-np.log(2)*((x-x0)/(FWHM/2))**2))+a*x+b

def doFit(intensity,twoTheta,thetaPeak):
        
    initialGuess =np.array([0, np.max(intensity)-np.min(intensity), thetaPeak*2, 0.028, 0, np.min(intensity)])
        
    param, param_covariance = curve_fit(gauss,twoTheta,intensity,initialGuess,ftol=10**(-10))
    param_error = np.sqrt(np.diag(param_covariance))
        
    return {"LorCoeff":param[0],"A":param[1],"x0":param[2],"FWHM":param[3],"LorCoeff_Err":param_error[0],"A_Err":param_error[1],"x0_Err":param_error[2],"FWHM_Err":param_error[3]}