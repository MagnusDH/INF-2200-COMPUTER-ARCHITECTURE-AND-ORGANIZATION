'''
Code written for inf-2200, University of Tromso
'''

import unittest

# Import elements with tests
from mux import *
from registerFile import *
from testCommon import *
from AND import *
from signExtend import *
from leftShift import *
from alu import *
from controlUnit import *
from aluControl import *
from dataMemory import *
from instructionMemory import *
from concatenator import *
from inverter import *
from orGate import *
from leftShift_sixteen import *
from pipeline_ifid import *
from pipeline_idex import *
from pipeline_exmem import *
from pipeline_memwb import *

if __name__ == '__main__':
    unittest.main() # Run all tests
