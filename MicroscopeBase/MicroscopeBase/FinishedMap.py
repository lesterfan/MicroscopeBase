
class FinishedMap(object):

    """ Struct storing the details of a finished map """

    map_name = ""
    fmspedir = ""
    xmldir   = ""
    imagedir = ""
    numx     = ""
    distbwx  = ""
    numy     = ""
    distbwy  = ""
    date     = ""
    time     = ""
    units    = ""

    def __init__(self, map_name, fmspedir, xmldir, imagedir, numx, distbwx, numy, distbwy, date, time, units):
        self.map_name = map_name
        self.fmspedir = fmspedir
        self.xmldir   = xmldir  
        self.imagedir = imagedir
        self.numx     = numx    
        self.distbwx  = distbwx 
        self.numy     = numy    
        self.distbwy  = distbwy 
        self.date     = date    
        self.time     = time    
        self.units    = units