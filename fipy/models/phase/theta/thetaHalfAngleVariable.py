#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  PyFiVol - Python-based finite volume PDE solver
 # 
 #  FILE: "ThetaHalfAngleVariable.py"
 #                                    created: 11/12/03 {10:39:23 AM} 
 #                                last update: 1/16/04 {11:19:34 AM} { 4:14:24 PM}
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
 #  2003-11-12 JEG 1.0 original
 # ###################################################################
 ##

import Numeric

from fivol.variables.cellVariable import CellVariable
from fivol.inline.inline import runInline

class ThetaHalfAngleVariable(CellVariable):
    def __init__(self, parameters = None, phase = None, theta = None):
        CellVariable.__init__(self, phase.getMesh(), hasOld = 0)
	self.parameters = parameters
	self.phase = self.requires(phase)
        self.theta = self.requires(theta)

    def calcValue(self):
	N = self.parameters['symmetry']
        dphi = self.phase.getGrad()[:,:]

        z = Numeric.arctan2(dphi[:,1],dphi[:,0])
        z = N * (z - self.theta[:])
        self.value = Numeric.tan(z / 2.)

##        runInline(
##            """
##            z = atan2(dphi(i,1),dphi(i,0));
##            z = N * (z - thetaFace(i));
##            value(i) = tan(z / 2.);
##            """,
##            z = 0., dphi = dphi, N = N, thetaFace = thetaFace, value = self.value,
##            ni = len(dphi[:,1]), nj = 0, nk= 0)
            


