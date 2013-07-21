"""
The twistless package provides a simple to use bridge for starting a twisted reactor 
using stackless tasklets.
"""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from .utils import deferred, blocking
from .executor import Twistless
