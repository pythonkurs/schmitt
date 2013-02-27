import __builtin__

def doProfile(func):
    """Calls profile decorator if profiling is enabled"""
    
    if "profile" in __builtin__.__dict__:
        print "Profile"
        return profile(func)
    else:
        print "No profile"
        return func
