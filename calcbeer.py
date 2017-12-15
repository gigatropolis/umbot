

def getPercentUtilization(boilTime):
    """ Calculate the correct percent Utilization 
        based on time in boil
        Return the Utilization in percent """
    if boilTime < 6:
        percUtil = 5.0
    elif boilTime < 11:
        percUtil = 6.0
    elif boilTime < 16:
        percUtil = 8.0
    elif boilTime < 21:
        percUtil = 10.1
    elif boilTime < 26:
        percUtil = 12.1
    elif boilTime < 31:
        percUtil = 15.3
    elif boilTime < 41:
        percUtil = 22.8
    elif boilTime < 46:
        percUtil = 26.9
    elif boilTime < 51:
        percUtil = 28.1
    else:
        percUtil = 30.0
        
    return percUtil
        
def getBoilGravity(batchSize, boilQnty, origGravity ):
    if boilQnty >= batchSize:
        return origGravity
    return ((origGravity-1) * (batchSize/boilQnty))+1

def getGravityAdjustment(boilGravity):
    if boilGravity < 1.050:
        return 0
    ga = (boilGravity-1.050) / 0.2
    return ga

def getIBU(waterQuantity, boilTime, amount, bitterness, OriginalGrav, boilQuantity):
    Utilization = getPercentUtilization(boilTime)  / 100.0
    boilGravity = getBoilGravity(waterQuantity, boilQuantity, OriginalGrav)
    gravAdjustment = getGravityAdjustment(boilGravity)
    ibu = (amount * Utilization * (bitterness / 100) * 7462.0) / (waterQuantity * (1 + gravAdjustment))
    return ibu

def defHopsForDesiredIBU(desiredIBU, waterQuantity, boilTime, bitterness, boilGravity):
    Utilization = getPercentUtilization(boilTime) / 100.0
    gravAdjustment = getGravityAdjustment(boilGravity)
    desiredIBU = (waterQuantity * (1+gravAdjustment) * desiredIBU) / (Utilization * (bitterness/100.0)*7462.0)
    return desiredIBU

def ABV(og, fg):
    return (og-fg) * 131.25
   
def KilToOz(kilAmount):
    #return kilAmount * 34.274
    return kilAmount /  0.02834952

def KilToGal(kilAmount):
    return kilAmount * 0.26417

def KilToLb(kilAmount):
    return kilAmount / 0.453592374

def McuToSrm(mcuAmount):
    return 1.4922 * (mcuAmount ** 0.6859)
    
def BrixToOg(Brix):
	return (Brix / (258.6-((Brix / 258.2)*227.1))) + 1
	
def OgToBrix(Og):
	return (((182.4601 * Og -775.6821) * Og +1262.7794) * Og -669.5622)
	
def RefractoFg(OrigBrix, FinalBrix):
	"""SG = 1.001843 - 0.002318474*OB - 0.000007775*OB*OB - 0.000000034*OB*OB*OB + 0.00574*FB + 0.00003344*FB*FB + 0.000000086*FB*FB*FB 

		SG = estimated specific gravity of the sample 
		OB = Original Brix 
		FB = Final Brix 
	"""
	Fg = 1.001843 - 0.002318474*OrigBrix - 0.000007775*OrigBrix**2 - 0.000000034*OrigBrix**3 + 0.00574*FinalBrix + 0.00003344*FinalBrix**2 + 0.000000086*FinalBrix**3
	return Fg
