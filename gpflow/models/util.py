import numpy as np
import tensorflow as tf

from ..inducing_variables import InducingVariables, InducingPoints
from .model import Data, BayesianModel, ExternalDataTrainingLossMixin


def inducingpoint_wrapper(inducing_variable):
    """
    This wrapper allows transparently passing either an InducingVariables
    object or an array specifying InducingPoints positions.
    """
    if not isinstance(inducing_variable, InducingVariables):
        inducing_variable = InducingPoints(inducing_variable)
    return inducing_variable


def _assert_equal_data(data1, data2):
    if isinstance(data1, tf.Tensor) and isinstance(data2, tf.Tensor):
        tf.debugging.assert_equal(data1, data2)
    else:
        for v1, v2 in zip(data1, data2):
            tf.debugging.assert_equal(v1, v2)


def model_training_loss(model: BayesianModel, data: Data) -> tf.Tensor:
    if isinstance(model, ExternalDataTrainingLossMixin):
        return model.training_loss(data)
    else:
        _assert_equal_data(model.data, data)
        return model.training_loss()


def model_maximum_likelihood_objective(model: BayesianModel, data: Data) -> tf.Tensor:
    if isinstance(model, ExternalDataTrainingLossMixin):
        return model.maximum_likelihood_objective(data)
    else:
        _assert_equal_data(model.data, data)
        return model.maximum_likelihood_objective()
