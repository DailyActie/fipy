#!/usr/bin/env python

## 
 # -*-Pyth-*-
 # ###################################################################
 #  PFM - Python-based phase field solver
 # 
 #  FILE: "linearCGSSolver.py"
 #                                    created: 11/14/03 {3:56:49 PM} 
 #                                last update: 1/13/04 {11:50:46 AM} 
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
 #  2003-11-14 JEG 1.0 original
 # ###################################################################
 ##

from solver import Solver
import precon
import itsolvers
import sys

class LinearCGSSolver(Solver):
    def __init__(self, tolerance, steps):
	Solver.__init__(self, tolerance, steps)
	
    def solve(self, L, x, b):

## 	print "L: ", L
## 	print "b: ", b
## 	print "x: ", x
	
	A = L.to_csr()

        info, iter, relres = itsolvers.cgs(A,b,x,self.tolerance,self.steps)
        
## 	print info, iter, relres
	
## 	y = x.copy()
## 	L.matvec(x,y)
## 	print "L * x: ", y
	
	if (info != 0):
	    print >> sys.stderr, 'cg not converged'
