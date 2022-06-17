import numpy as np
from scipy.optimize import curve_fit


def axisTransformFit(x,*p):
    eyy,ezz,eyz = p
    theta = 5.8*np.pi/180 #change!
    chi = x
    #'((sind(theta))^2)*(0)+((cosd(theta))^2)*((sind(chi))^2)*eyy+((cosd(theta))^2)*((cosd(chi))^2)*ezz-((sind(2*theta)))*((cosd(chi)))*0+((cosd(theta))^2)*((sind(2*chi)))*eyz'
    #((sind(2*theta)))*((cosd(chi)))*0+((cosd(theta))^2)*((sind(2*chi)))*eyz
    return ((np.cos(theta))**2)*((np.sin(chi))**2)*eyy+((np.cos(theta))**2)*((np.cos(chi))**2)*ezz+((np.cos(theta))**2)*((np.sin(2*chi)))*eyz

def poly1(x,a, b, c):
    return a*x+b

def doFit(azimuthalAngles,x0,x0_err,d0,wavelength):
    trashData_count = np.count_nonzero([(np.array(x0)/np.array(x0_err)) <= 0.01]) #count how much rows are unusable doe to high error
            
    if(trashData_count < len(azimuthalAngles)-6):
        strains = ((wavelength/(2*np.sin((x0/2)*np.pi/180)))-d0)/d0 #calculate strain via brag equation
        
        poly1_params = curve_fit(poly1,np.sin(azimuthalAngles*np.pi/180)**2,strains)[0]
        initialGuess = [poly1_params[0]+poly1_params[1],poly1_params[1],0]

        normalStrains, normalStrains_covariance  = curve_fit(axisTransformFit,azimuthalAngles*np.pi/180,strains,initialGuess,ftol=10**(-12))
        normalStrains_error = np.sqrt(np.diag(normalStrains_covariance))


                
        return {"strainXX":normalStrains[0],"strainZZ":normalStrains[1],"strainXZ":normalStrains[2],"strainXX_Err":normalStrains_error[0],"strainZZ_Err":normalStrains_error[1],"strainXZ_Err":normalStrains_error[2]}
    else:
        return {"strainXX":0,"strainZZ":0,"strainXZ":0,"strainXX_Err":0,"strainZZ_Err":0,"strainXZ_Err":0}
    
    
def calculatePrincipalStresses(E,poisson,strainYY,strainZZ,strainYZ):

        stressXX=(E/((1+poisson)*(1-2*poisson)))*((1-poisson)*strainYY)+(E/((1+poisson)*(1-2*poisson)))*((poisson)*strainZZ)+(E/((1+poisson)*(1-2*poisson)))*((poisson)*0)
        stressZZ=(E/((1+poisson)*(1-2*poisson)))*((1-poisson)*strainZZ)+(E/((1+poisson)*(1-2*poisson)))*((poisson)*strainYY)+(E/((1+poisson)*(1-2*poisson)))*((poisson)*0)
        stressXZ=(E/((1+poisson)*(1-2*poisson)))*((1-2*poisson)*strainYZ)


        stressXX=(E/((1+poisson)*(1-2*poisson)))*((1-poisson)*0)+(E/((1+poisson)*(1-2*poisson)))*((poisson)*strainZZ)+(E/((1+poisson)*(1-2*poisson)))*((poisson)*strainYY)

        stressMises=np.sqrt((1/2)*((stressXX-stressXX)**2+(stressXX-stressZZ)**2+(stressZZ-stressXX)**2+6*stressXZ**2))

        stressHydro=(stressXX+stressXX+stressZZ)/3

        return {"stressXX":stressXX,"stressZZ":stressXX,"stressXZ":stressXZ,"stressHydro":stressHydro,"stressMises":stressMises}
    