#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  PFM - Python-based phase field solver
 # 
 #  FILE: "substitutionalVariable.py"
 #                                    created: 12/18/03 {12:18:05 AM} 
 #                                last update: 1/13/04 {11:46:48 AM} 
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
 #  See the file "license.terms" for information on usage and  redistribution
 #  of this file, and for a DISCLAIMER OF ALL WARRANTIES.
 #  
 # ###################################################################
 ##

from componentVariable import ComponentVariable
from tools.dimensions import physicalField

class SubstitutionalVariable(ComponentVariable):
    def __init__(self, mesh, parameters, systemParameters, value=0., hasOld = 1):
	ComponentVariable.__init__(self, mesh = mesh, parameters = parameters, systemParameters = systemParameters, value = value, hasOld = hasOld)
	self.solventParameters = systemParameters['solvent']
## 	self.standardPotential -= physicalField.PhysicalField(self.solventParameters['standard potential'])
## 	self.barrierHeight -= physicalField.PhysicalField(self.solventParameters['barrier height'])
	self.standardPotential -= physicalField.Scale(self.solventParameters['standard potential'],"ENERGY")
	self.barrierHeight -= physicalField.Scale(self.solventParameters['barrier height'],"ENERGY")
	if self.solventParameters.has_key('valence'):
	    self.valence -= self.solventParameters['valence']