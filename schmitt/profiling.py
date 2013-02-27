import __builtin__

def doProfile(func):
    """Calls profile decorator if profiling is enabled"""
    
    if "profile" in __builtin__.__dict__:
        return profile(func)
    else:
        return func
