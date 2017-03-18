

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
    return kilAmount * 34.274

def KilToGal(kilAmount):
    return kilAmount * 0.26417

def KilToLb(kilAmount):
    return kilAmount / 0.453592374

def McuToSrm(mcuAmount):
    return 1.4922 * (mcuAmount ** 0.6859)