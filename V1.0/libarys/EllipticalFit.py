import numpy as np
from scipy.optimize import curve_fit


#poly1 function to fit initial guess
def poly1(x,a, b, c):
    return a*x+b

def doFit(azimuthalAngles,x0,x0_err,d0,wavelength,theta):
    """Fits strain ellipsoid on given x0 and azimuthal angles

    Args:
        azimuthalAngles (list): list of azimuthal angles
        x0 (list): list of peak positions 
        x0_err (_type_): list of peak positions fit error
        d0 (chosen precision): Lattice distance in unstressed case 
        wavelength (chosen precision): Wavelength which was used during the experiment

    Returns:
        dictionary: A Dictionary which contains the chosen constants of the fit as well as there errors
    """
    trashData_count = np.count_nonzero([(np.array(x0)/np.array(x0_err)) <= 0.01]) #count how much rows are unusable doe to high error
    ellipticalFit = lambda x,*p :((np.cos(theta))**2)*((np.sin(x))**2)*p[0]+((np.cos(theta))**2)*((np.cos(x))**2)*p[1]+((np.cos(theta))**2)*((np.sin(2*x)))*p[2]
    if(trashData_count < len(azimuthalAngles)-6):
        strains = ((wavelength/(2*np.sin((x0/2)*np.pi/180)))-d0)/d0 #calculate strain via brag equation
        
        poly1_params = curve_fit(poly1,np.sin(azimuthalAngles*np.pi/180)**2,strains)[0]
        initialGuess = [poly1_params[0]+poly1_params[1],poly1_params[1],0]

        normalStrains, normalStrains_covariance  = curve_fit(ellipticalFit,azimuthalAngles*np.pi/180,strains,initialGuess,ftol=10**(-12))
        normalStrains_error = np.sqrt(np.diag(normalStrains_covariance))


                
        return {"strainXX":normalStrains[0],"strainZZ":normalStrains[1],"strainXZ":normalStrains[2],"strainXX_Err":normalStrains_error[0],"strainZZ_Err":normalStrains_error[1],"strainXZ_Err":normalStrains_error[2]}
    else:
        return {"strainXX":0,"strainZZ":0,"strainXZ":0,"strainXX_Err":0,"strainZZ_Err":0,"strainXZ_Err":0}
    
    
def calculatePrincipalStresses(E,poissonNumbers,strainXX,strainZZ,strainXZ):
        """Calculates stresses in XX,YY,YZ direction and Mises/Hydro

        Args:
            E (list): List of E-Modules for different lattice plane
            poissonNumbers (list): List of poisson numbers for different lattice plane
            strainYY (list): list of strainsYY
            strainZZ (list): list of strainsYY
            strainYZ (list): list of strainsYY

        Returns:
            dictionary: dictionary that contrains stressXX,stressZZ,stressXZ,stressMises,stressHydro
        """

        stressXX=(E/((1+poissonNumbers)*(1-2*poissonNumbers)))*((1-poissonNumbers)*strainXX)+(E/((1+poissonNumbers)*(1-2*poissonNumbers)))*((poissonNumbers)*strainZZ)+(E/((1+poissonNumbers)*(1-2*poissonNumbers)))*((poissonNumbers)*0)
        stressZZ=(E/((1+poissonNumbers)*(1-2*poissonNumbers)))*((1-poissonNumbers)*strainZZ)+(E/((1+poissonNumbers)*(1-2*poissonNumbers)))*((poissonNumbers)*strainXX)+(E/((1+poissonNumbers)*(1-2*poissonNumbers)))*((poissonNumbers)*0)
        stressXZ=(E/((1+poissonNumbers)*(1-2*poissonNumbers)))*((1-2*poissonNumbers)*strainXZ)


        stressXX=(E/((1+poissonNumbers)*(1-2*poissonNumbers)))*((1-poissonNumbers)*0)+(E/((1+poissonNumbers)*(1-2*poissonNumbers)))*((poissonNumbers)*strainZZ)+(E/((1+poissonNumbers)*(1-2*poissonNumbers)))*((poissonNumbers)*strainXX) #FIXME bug

        stressMises=np.sqrt((1/2)*((stressXX-stressXX)**2+(stressXX-stressZZ)**2+(stressZZ-stressXX)**2+6*stressXZ**2))

        stressHydro=(stressXX+stressXX+stressZZ)/3

        return {"stressXX":stressXX,"stressZZ":stressXX,"stressXZ":stressXZ,"stressHydro":stressHydro,"stressMises":stressMises}
    