# 
# Package for the SciLifeLab python course 2013
#
# Thomas Schmitt thms.schmitt@gmail.com
# 


#Getting data

def loadEscalatorOutage(outageURL="http://www.grandcentral.org/developers/data/nyct/nyct_ene.xml"):
    """Loads the escalator outage status. Returns untangled xml."""
    
    import untangle
    import requests
    
    r = requests.get(outageURL)
    
    if r.status_code != requests.codes.ok:
        r.raise_for_status()
    
    outageDoc = untangle.parse(r.text)
    
    return outageDoc
    


def countEscalatorOutageReason(esculatorOutages, reason="REPAIR"):
    """Extracts the number of outages with the given reason and the total number of outages"""
    
    total=0
    withGivenReason=0
    
    if len(esculatorOutages.NYCOutages.get_elements(name="outage")) > 0:
    
        for outage in esculatorOutages.NYCOutages.outage:
            
            total+=1
            if outage.reason.cdata.lower() == reason.lower():
                withGivenReason+=1
        
    return (withGivenReason,total)


