from enum import Enum

class ScalarOpts(str,Enum):
    pass

class CurveOpts(str,Enum):
    KE = "Kinetic energy (ke)"
    IE = "Internal energy (ie)"
    HE = "Hourglass energy (he)"
    # sliding
    SIE = "Sliding interface energy (sie)"
    TE = "Total energy (te)"
    
class DeformOpts(str,Enum):
    D = "Displacements"
    A = "Accelerations"
    V = "Velocities"
    
    