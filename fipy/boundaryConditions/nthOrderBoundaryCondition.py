## -*-Pyth-*-
 # ###################################################################
 #  FiPy - a finite volume PDE solver in Python
 # 
 #  FILE: "nthOrderBoundaryCondition.py"
 #                                    created: 6/9/04 {4:09:25 PM} 
 #                                last update: 7/28/04 {6:18:48 PM} 
 #  Author: Jonathan Guyer
 #  E-mail: guyer@nist.gov
 #    mail: NIST
 #     www: http://ctcms.nist.gov
 #  
 # ========================================================================
 # This document was prepared at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this document is not subject to copyright
 # protection and is in the public domain.  nthOrder.py
 # is an experimental work.  NIST assumes no responsibility whatsoever
 # for its use by other parties, and makes no guarantees, expressed
 # or implied, about its quality, reliability, or any other characteristic.
 # We would appreciate acknowledgement if the document is used.
 # 
 # This document can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  See the file "license.terms" for information on usage and  redistribution
 #  of this file, and for a DISCLAIMER OF ALL WARRANTIES.
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2004-06-09 JEG 1.0 original
 # ###################################################################
 ##

__docformat__ = 'restructuredtext'

import Numeric

from fipy.boundaryConditions.boundaryCondition import BoundaryCondition
from fipy.boundaryConditions.fixedFlux import FixedFlux
from fipy.boundaryConditions.fixedValue import FixedValue

class NthOrderBoundaryCondition(BoundaryCondition):
    def __init__(self,faces,value,order):
        self.order = order
        BoundaryCondition.__init__(self,faces,value)

    def getContribution(self,cell1dia,cell1off):
        """Leave L and b unchanged
        
        Arguments:
            
            'cell1dia' -- *unused*

            'cell1off' -- *unused*
        """
        return (Numeric.array([]),Numeric.array([]),Numeric.array([]))
        
    def getDerivative(self, order):
	newOrder = self.order - order
        if newOrder > 1:
            return NthOrderBoundaryCondition(self.faces, self.value, newOrder)
        elif newOrder == 1:
            return FixedFlux(self.faces, self.value) 
        elif newOrder == 0:
            return FixedValue(self.faces, self.value) 
        else:
            return None

