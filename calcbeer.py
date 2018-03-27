
import math

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

def getIBU(waterQuantity, boilTime, amount, percAlpha, OriginalGrav, boilQuantity):
    Utilization = getPercentUtilization(boilTime)  / 100.0
    boilGravity = getBoilGravity(waterQuantity, boilQuantity, OriginalGrav)
    gravAdjustment = getGravityAdjustment(boilGravity)
    ibu = (amount * Utilization * (percAlpha / 100) * 7462.0) / (waterQuantity * (1 + gravAdjustment))
    return ibu

def defHopsForDesiredIBU(desiredIBU, waterQuantity, boilTime, percAlpha, boilGravity):
    Utilization = getPercentUtilization(boilTime) / 100.0
    gravAdjustment = getGravityAdjustment(boilGravity)
    desiredIBU = (waterQuantity * (1+gravAdjustment) * desiredIBU) / (Utilization * (percAlpha / 100.0)*7462.0)
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
    
    brix = (((182.4601 * Og -775.6821) * Og +1262.7794) * Og -669.5622)
    return brix
	
def OgToBrix2(Og):
    """ -676.67 + 1286.4*SG - 800.47*(SG^2) + 190.74*(SG^3) """

    brix = -676.67 + 1286.4*Og - 800.47*(Og**2) + 190.74*(Og**3)
    return brix
	
def RefractoFg2(OrigBrix, FinalBrix):
    """RefractoFg will convert refractometer Final gravity from original and final Brix readings from refractometer

        FG = 1.00358522 – 0.00123861*RIi + 0.00380186*RIf

        OrigBrix (RIi)  =   Original Brix reading 
        FinalBrix (RIf) =   Final Brix Reading from refractometer 
        FG =                Final Gravity measured
    """
    FG = 1.00358522 - 0.00123861*OrigBrix + 0.00380186*FinalBrix

    return FG

def RefractoFg3(OrigBrix, FinalBrix):
    """RefractoFg will convert refractometer Final gravity from original and final Brix readings from refractometer

        FG = 1.0111958 – 0.00813003RIi + 0.0144032RIf + 0.000523555RIi² – 0.00166862RIf² – 0.0000125754RIi³ + 0.0000812663RIf³
 
        OrigBrix (RIi)  =   Original Brix reading 
        FinalBrix (RIf) =   Final Brix Reading from refractometer 
        FG =                Final Gravity measured
    """
    FG = 1.0111958 - 0.00813003 * OrigBrix + 0.0144032 * FinalBrix + 0.000523555 * OrigBrix**2 - 0.00166862 * FinalBrix**2 - \
         0.0000125754 * OrigBrix**3 + 0.0000812663 * FinalBrix**3

    return FG

def RefractoFg4(OrigBrix, FinalBrix):
    """RefractoFg will convert refractometer Final gravity from original and final Brix readings from refractometer

        SG = 1.001843 - 0.002318474(OB) - 0.000007775(OB^2) - 0.000000034(OB^3) + 0.00574(AB) + 0.00003344(AB^2) + 0.000000086(AB^3)

        OrigBrix (RIi)  =   Original Brix reading 
        FinalBrix (RIf) =   Final Brix Reading from refractometer 
        FG =                Final Gravity measured
    """
    FG = 1.001843 - 0.002318474 * (OrigBrix) - 0.000007775 * (OrigBrix**2) - 0.000000034 * (OrigBrix**3) + \
         0.00574 * (FinalBrix) + 0.00003344 * (FinalBrix**2) + 0.000000086 * (FinalBrix**3)

    return FG

def _refN1(OrigBrix, FinalBrix):
    return 1.001843 - 0.002318474*OrigBrix - 0.000007775*(OrigBrix**2) - 0.000000034*(OrigBrix**3) + 0.00574*FinalBrix + 0.00003344*(FinalBrix**2) + 0.000000086*(FinalBrix**3)

def _refN2(OrigBrix, FinalBrix):
    return 1.000898 + 0.003859118*OrigBrix + 0.00001370735*(OrigBrix**2) + 0.00000003742517*(OrigBrix**3)

def _refN3(OrigBrix, FinalBrix):
    return 668.72 * _refN2(OrigBrix, FinalBrix) - 463.37 - 205.347 * (_refN2(OrigBrix, FinalBrix)**2)

def RefractoFg(OrigBrix, FinalBrix):
    """RefractoFg will convert refractometer Final gravity from original and final Brix readings from refractometer

        OrigBrix (RIi)  =   Original Brix reading 
        FinalBrix (RIf) =   Final Brix Reading from refractometer 
        FG =                Final Gravity measured

        FG = (1.001843 – 0.002318474*RIi – 0.000007775*RIi² – 0.000000034*RIi³ + 0.00574*RIf + 0.00003344*RIf² + 0.000000086*RIf³) + 0.0216*LN(1 –
            (0.1808*(668.72*(1.000898 + 0.003859118*RIi + 0.00001370735*RIi² + 0.00000003742517*RIi³) – 463.37 – 
            205.347*(1.000898 + 0.003859118*RIi + 0.00001370735*RIi² + 0.00000003742517*RIi³)²) + 
            0.8192*(668.72*(1.001843 – 0.002318474*RIi – 0.000007775*RIi² – 0.000000034*RIi³ + 0.00574*RIf + 0.00003344*RIf² + 0.000000086*RIf³) – 463.37 – 
            205.347*(1.001843 – 0.002318474*RIi – 0.000007775*RIi² – 0.000000034*RIi³ + 0.00574*RIf + 0.00003344*RIf² + 0.000000086*RIf³)²)) / 
            (668.72*(1.000898 + 0.003859118*RIi + 0.00001370735*RIi² + 0.00000003742517*RIi³) – 463.37 – 
            205.347*(1.000898 + 0.003859118*RIi + 0.00001370735*RIi² + 0.00000003742517*RIi³)²)) + 0.0116
    """
    refN1 = _refN1(OrigBrix, FinalBrix)
    refN2 = _refN2(OrigBrix, FinalBrix)
    refN3 = _refN3(OrigBrix, FinalBrix)

    FG = refN1 + 0.0216 * math.log(1 - (0.1808*(668.72 * refN2 - 463.37 - 205.347 * refN2**2) + 0.8192 * (668.72 * refN1 - 463.37 - 205.347 * refN1**2)) / refN3) + 0.0116
    return FG


def HandleCalc(command, channel):
    """
        Handle request for beer calculations 
    """
    help = "Try: \"@umbot OgToBrix 1.054\""
    response = ""
    words = command.split(" ")
    print("words: %s" %(words))

    if words[1].lower() == 'brixtoog' and len(words) > 2:
        og = BrixToOg(float(words[2]))
        response = "Original gravity is %.4f" % (og)

    elif words[1].lower() == 'ogtobrix' and len(words) > 2:
        og = float(words[2])
        brix = OgToBrix(og)
        brix2 = OgToBrix2(og)
        response = "Brix is %.2f  Brix2 if %.2f" % (brix, brix2)

    elif words[1].lower().find('refractotofg') == 0 and len(words) > 3:
        
        OrigBrix = float(words[2])
        FinalBrix = float(words[3])
        refracto = words[1].lower()

        if len(refracto) == 13:
            type = refracto[12]
            if type == '2':
                fg = RefractoFg2(OrigBrix, FinalBrix)
            elif type == '3':
                fg = RefractoFg3(OrigBrix, FinalBrix)
            elif type == '4':
                fg = RefractoFg4(OrigBrix, FinalBrix)
            else:
                fg = RefractoFg(OrigBrix, FinalBrix)
        else:
            fg = RefractoFg(OrigBrix, FinalBrix)

        abv = ABV(BrixToOg(OrigBrix), fg)
        response = "Final gravity is %.4f with ABV of %.2f%%" % (fg, abv)

    if not response:
        response = help

    return response   
