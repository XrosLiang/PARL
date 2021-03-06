#   Copyright (c) 2018 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import warnings
warnings.simplefilter('default')

from parl.core.algorithm_base import AlgorithmBase
from parl.core.fluid.model import Model
from parl.utils.deprecation import deprecated

__all__ = ['Algorithm']


class Algorithm(AlgorithmBase):
    """
    | `alias`: ``parl.Algorithm``
    | `alias`: ``parl.core.fluid.algorithm.Algorithm``

    | ``Algorithm`` defines the way how to update the parameters of the ``Model``. This is where we define loss functions and the optimizer of the neural network. An ``Algorithm`` has at least a model.

    | PARL has implemented various algorithms(DQN/DDPG/PPO/A3C/IMPALA) that can be reused quickly, which can be accessed with ``parl.algorithms``.

    Example:

    .. code-block:: python

        import parl

        model = Model()
        dqn = parl.algorithms.DQN(model, lr=1e-3)

    Attributes:
        model(``parl.Model``): a neural network that represents a policy or a Q-value function.

    Pulic Functions:
        - ``get_weights``: return a Python dictionary containing parameters of the current model.
        - ``set_weights``: copy parameters from ``get_weights()`` to the model.
        - ``sample``: return a noisy action to perform exploration according to the policy.
        - ``predict``: return an action given current observation.
        - ``learn``: define the loss function and create an optimizer to minized the loss.

    Note:

        ``Algorithm`` defines all its computation inside a ``fluid.Program``, such that the returns of functions(`sample`, `predict`, `learn`) are tensors.
        ``Agent`` also has functions like `sample`, `predict`, and `learn`, but they return numpy array for the agent.
        
    """

    def __init__(self, model=None, hyperparas=None):
        """
        Args:
            model(``parl.Model``): a neural network that represents a policy or a Q-value function.
            hyperparas(dict): a dict storing the hyper-parameters relative to training.
        """
        if model is not None:
            warnings.warn(
                "the `model` argument of `__init__` function in `parl.Algorithm` is deprecated since version 1.2 and will be removed in version 1.3.",
                DeprecationWarning,
                stacklevel=2)

            assert isinstance(model, Model)
            self.model = model
        if hyperparas is not None:
            warnings.warn(
                "the `hyperparas` argument of `__init__` function in `parl.Algorithm` is deprecated since version 1.2 and will be removed in version 1.3.",
                DeprecationWarning,
                stacklevel=2)

            self.hp = hyperparas

    @deprecated(
        deprecated_in='1.2', removed_in='1.3', replace_function='get_weights')
    def get_params(self):
        """ Get parameters of self.model.

        Returns:
            params(dict): a Python List containing the parameters of self.model.
        """
        return self.model.get_params()

    @deprecated(
        deprecated_in='1.2', removed_in='1.3', replace_function='set_weights')
    def set_params(self, params):
        """ Set parameters from ``get_params`` to the model.

        Args:
            params(dict ): a Python List containing the parameters of self.model.
        """
        self.model.set_params(params)

    def learn(self, *args, **kwargs):
        """ Define the loss function and create an optimizer to minize the loss.
        """
        raise NotImplementedError

    def predict(self, *args, **kwargs):
        """ Refine the predicting process, e.g,. use the policy model to predict actions.
        """
        raise NotImplementedError

    def sample(self, *args, **kwargs):
        """ Define the sampling process. This function returns an action with noise to perform exploration.
        """
        raise NotImplementedError
