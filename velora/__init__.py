"""
Velora - Simple file sharing and chat over TCP sockets

A lightweight Python library for peer-to-peer file sharing and real-time chat
using TCP sockets. No external dependencies required.
"""

__version__ = "1.1.0"
__author__ = "Pavan Sai Tanguturi"
__email__ = "pavansai.tanguturi@gmail.com"

from .client import VeloraClient
from .server import VeloraServer
from .share import quick_share

__all__ = [
    "VeloraClient",
    "VeloraServer", 
    "quick_share",
]