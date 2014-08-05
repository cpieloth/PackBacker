__author__ = 'Christof Pieloth'

from .cxxtest import CxxTest
from .eigen3 import Eigen3


def installer_prototypes():
    """Returns prototypes of all known installers."""
    prototypes = []
    prototypes.append(CxxTest.prototype())
    prototypes.append(Eigen3.prototype())
    return prototypes
