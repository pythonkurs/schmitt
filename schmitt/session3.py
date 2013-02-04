# 
# Session 3 SciLifeLab python course 2013 -- context and decorator
# 
#
# Thomas Schmitt thms.schmitt@gmail.com
#

import os

class directoryContext(object):
    """Guarantees that the working directory changes to the given directory when entring the context and is reset when leaving the context"""
    
    def __init__(self, dir):
        self.currentDir = os.getcwd()
        self.contextDir = dir

    def __enter__(self):
        os.chdir(self.contextDir)

    def __exit__(self, type, value, tb):
        os.chdir(self.currentDir)

class CourseRepo(object):
    
    _requirements = (".git","setup.py","README.md","scripts/getting_data.py","scripts/check_repo.py","{}/__init__.py","{}/session3.py")

    def __init__(self,surname):
        
        if surname == "":
            raise ValueError("Surname may not be empty")
            
        self.surname = surname    
        
    @property
    def surname(self):
        return self._surname
        
    @surname.setter
    def surname(self,value):
        """Sets the surname and updates the required file names."""
        self._surname = value
        self.required = map(lambda a : a.format(self._surname),self._requirements)
        

    def check(self):
        """Returns True if all required files exist and False otherwise."""
        
        import os.path
        
        for _file in self.required:
            
            if not os.path.exists(_file):
                return False
        
        return True