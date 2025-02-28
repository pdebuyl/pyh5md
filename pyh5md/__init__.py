from .h5md_module import (File, element, ParticlesGroup, FixedElement,
                          TimeElement, LinearElement)
import os.path

with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as f:
    __version__ = f.read().strip()
