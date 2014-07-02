# Copyright (c) 2012, GPy authors (see AUTHORS.txt).
# Licensed under the BSD 3-clause license (see LICENSE.txt)


import numpy as np
import pylab as pb
import sys, pdb
from GPy.models.sparse_gp_regression import SparseGPRegression
from GPy.models.gplvm import GPLVM
# from .. import kern
# from ..core import model
# from ..util.linalg import pdinv, PCA

class SparseGPLVM(SparseGPRegression):
    """
    Sparse Gaussian Process Latent Variable Model

    :param Y: observed data
    :type Y: np.ndarray
    :param input_dim: latent dimensionality
    :type input_dim: int
    :param init: initialisation method for the latent space
    :type init: 'PCA'|'random'

    """
    def __init__(self, Y, input_dim, X=None, kernel=None, init='PCA', num_inducing=10):
        if X is None:
            from ..util.initialization import initialize_latent
            X, fracs = initialize_latent(init, input_dim, Y)
        SparseGPRegression.__init__(self, X, Y, kernel=kernel, num_inducing=num_inducing)

    def parameters_changed(self):
        super(SparseGPLVM, self).parameters_changed()
        self.X.gradient = self.kern.gradients_X(self.grad_dict['dL_dKnm'], self.X, self.Z)

    def plot_latent(self, labels=None, which_indices=None,
                resolution=50, ax=None, marker='o', s=40,
                fignum=None, plot_inducing=True, legend=True,
                plot_limits=None, 
                aspect='auto', updates=False, predict_kwargs={}, imshow_kwargs={}):
        assert "matplotlib" in sys.modules, "matplotlib package has not been imported."
        from ..plotting.matplot_dep import dim_reduction_plots

        return dim_reduction_plots.plot_latent(self, labels, which_indices,
                resolution, ax, marker, s,
                fignum, plot_inducing, legend,
                plot_limits, aspect, updates, predict_kwargs, imshow_kwargs)
