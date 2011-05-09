#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "unaryTerm.py"
 #
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
 #    mail: NIST
 #     www: http://www.ctcms.nist.gov/fipy/
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  FiPy is an experimental
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
 # ###################################################################
 ##

__docformat__ = 'restructuredtext'

from fipy.tools import numerix
from fipy.terms.term import Term
from fipy.terms import SolutionVariableRequiredError

class _UnaryTerm(Term):

    @property
    def _vars(self):
        return [self.var]

    @property
    def _transientVars(self):
        return []
                
    @property
    def _uncoupledTerms(self):
        return [self]
    
    def __repr__(self):
        """
        The representation of a `Term` object is given by,
        
           >>> print __UnaryTerm(123.456)
           __UnaryTerm(coeff=123.456)

        """
        if self.var is None:
            varString = ''
        else:
            varString = ', var=%s' % repr(self.var)

        return "%s(coeff=%s%s)" % (self.__class__.__name__, repr(self.coeff), varString)

    @property
    def _buildExplcitIfOther(self):
        return False

    def _buildAndAddMatrices(self, var, SparseMatrix, boundaryConditions=(), dt=1.0, transientGeomCoeff=None, diffusionGeomCoeff=None, buildExplicitIfOther=False):
        """Build matrices of constituent Terms and collect them

        Only called at top-level by `_prepareLinearSystem()`
        
        """

        if var is self.var or self.var is None:
            return self._buildMatrix(var,
                                     SparseMatrix,
                                     boundaryConditions=boundaryConditions,
                                     dt=dt,
                                     transientGeomCoeff=transientGeomCoeff,
                                     diffusionGeomCoeff=diffusionGeomCoeff)
        elif buildExplicitIfOther:
            tmp, matrix, RHSvector = self._buildMatrix(self.var,
                                                       SparseMatrix,
                                                       boundaryConditions=boundaryConditions,
                                                       dt=dt,
                                                       transientGeomCoeff=transientGeomCoeff,
                                                       diffusionGeomCoeff=diffusionGeomCoeff)
            return var, SparseMatrix(mesh=var.mesh), RHSvector - matrix * self.var.value
        else:
            return var, SparseMatrix(mesh=var.mesh), 0

    def _test(self):
        """
        Offset tests

        >>> from fipy import *
        >>> m = Grid1D(nx=3)
        >>> v0 = CellVariable(mesh=m, value=1.)
        >>> v1 = CellVariable(mesh=m, value=0.)
        >>> eq = TransientTerm(var=v0) & DiffusionTerm(coeff=4., var=v1)
        >>> var, matrix, RHSvector = eq._buildAndAddMatrices(var=eq._verifyVar(None), SparseMatrix=DefaultSolver()._matrixClass)
        >>> print var.globalValue
        [ 1.  1.  1.  0.  0.  0.]
        >>> print RHSvector.globalValue
        [ 1.  1.  1.  0.  0.  0.]
        >>> print numerix.allequal(matrix.numpyArray,
        ...                        [[ 1,  0,  0,  0,  0,  0],
        ...                         [ 0,  1,  0,  0,  0,  0],
        ...                         [ 0,  0,  1,  0,  0,  0],
        ...                         [ 0,  0,  0, -4,  4,  0],
        ...                         [ 0,  0,  0,  4, -8,  4],
        ...                         [ 0,  0,  0,  0,  4, -4]])
        True

        >>> m = Grid1D(nx=6)
        >>> v0 = CellVariable(mesh=m, value=0.)
        >>> v1 = CellVariable(mesh=m, value=1.)        
        >>> eq0 = DiffusionTerm(coeff=1., var=v0)
        >>> eq1 = TransientTerm(var=v1) - DiffusionTerm(coeff=3., var=v0) - DiffusionTerm(coeff=4., var=v1) 
        >>> eq = eq0 & eq1
        >>> var, matrix, RHSvector = eq._buildAndAddMatrices(var=eq._verifyVar(None), SparseMatrix=DefaultSolver()._matrixClass) 
        >>> print var.globalValue
        [ 0.  0.  0.  0.  0.  0.  1.  1.  1.  1.  1.  1.]
        >>> print RHSvector.globalValue
        [ 0.  0.  0.  0.  0.  0.  1.  1.  1.  1.  1.  1.]
        >>> print numerix.allequal(matrix.numpyArray,
        ...                        [[-1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        ...                         [ 1, -2,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        ...                         [ 0,  1, -2,  1,  0,  0,  0,  0,  0,  0,  0,  0],
        ...                         [ 0,  0,  1, -2,  1,  0,  0,  0,  0,  0,  0,  0],
        ...                         [ 0,  0,  0,  1, -2,  1,  0,  0,  0,  0,  0,  0],
        ...                         [ 0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0],
        ...                         [ 3, -3,  0,  0,  0,  0,  5, -4,  0,  0,  0,  0],
        ...                         [-3,  6, -3,  0,  0,  0, -4,  9, -4,  0,  0,  0],
        ...                         [ 0, -3,  6, -3,  0,  0,  0, -4,  9, -4,  0,  0],
        ...                         [ 0,  0, -3,  6, -3,  0,  0,  0, -4,  9, -4,  0],
        ...                         [ 0,  0,  0, -3,  6, -3,  0,  0,  0, -4,  9, -4],
        ...                         [ 0,  0,  0,  0, -3,  3,  0,  0,  0,  0, -4,  5]])
        True
        
        >>> m = Grid1D(nx=3)
        >>> v0 = CellVariable(mesh=m, value=0.)
        >>> v1 = CellVariable(mesh=m, value=1.)
        >>> diffTerm = DiffusionTerm(coeff=1., var=v0)
        >>> eq00 = TransientTerm(var=v0) - DiffusionTerm(coeff=1., var=v0)
        >>> eq0 = eq00 - DiffusionTerm(coeff=2., var=v1)
        >>> eq1 = TransientTerm(var=v1)
        >>> eq0.cacheMatrix()
        >>> diffTerm.cacheMatrix()
        >>> (eq0 & eq1).solve()
        >>> print numerix.allequal(eq0.matrix.numpyArray,
        ...                        [[ 2, -1,  0,  2, -2,  0],
        ...                         [-1,  3, -1, -2,  4, -2],
        ...                         [ 0, -1,  2,  0, -2,  2],
        ...                         [ 0,  0,  0,  0,  0,  0],
        ...                         [ 0,  0,  0,  0,  0,  0],
        ...                         [ 0,  0,  0,  0,  0,  0]])
        True
        >>> ## This currectly returns None because we lost the handle to the DiffusionTerm when it's negated.
        >>> print diffTerm.matrix 
        None

        """
        
class __UnaryTerm(_UnaryTerm): 
    """
    Dummy subclass for tests
    """
    pass 

def _test(): 
    import doctest
    return doctest.testmod()

if __name__ == "__main__":
    _test()