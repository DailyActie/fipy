#!/usr/bin/env python

## 
 # ###################################################################
 #  PFM - Python-based phase field solver
 # 
 #  FILE: "testStdyConvectionDiffusion.py"
 #                                    created: 12/16/03 {3:23:47 PM}
 #                                last update: 1/13/04 {11:59:28 AM} 
 #  Author: Jonathan Guyer
 #  E-mail: guyer@nist.gov
 #  Author: Daniel Wheeler
 #  E-mail: daniel.wheeler@nist.gov
 #    mail: NIST
 #     www: http://ctcms.nist.gov
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  PFM is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-10 JEG 1.0 original
 # ###################################################################
 ##

from terms.exponentialConvectionTerm import ExponentialConvectionTerm
from convectionDiffusionSystem import ConvectionDiffusionSystem
from boundaryConditions.fixedValue import FixedValue
from boundaryConditions.fixedFlux import FixedFlux

class Exponential1DScSystem(ConvectionDiffusionSystem):

    def __init__(self):
        self.L = 1.
        self.nx = 1
        self.ny = 1000
        self.diffCoeff = 1.
        self.convCoeff = (0.,10.)
        self.sourceCoeff = 1.
        self.convectionScheme = ExponentialConvectionTerm
        ConvectionDiffusionSystem.__init__(self)

    def getBoundaryConditions(self):
        return (
            FixedFlux(faces = self.mesh.getFacesLeft(),value = 0.),
            FixedFlux(faces = self.mesh.getFacesRight(),value = 0.),
            FixedValue(faces = self.mesh.getFacesTop(),value = self.valueRight),
            FixedValue(faces = self.mesh.getFacesBottom(),value = self.valueLeft)
            )

if __name__ == '__main__':
    system = Exponential1DScSystem()
    system.run()

            
            
