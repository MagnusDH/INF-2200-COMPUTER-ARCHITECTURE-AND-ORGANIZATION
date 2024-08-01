'''
Code written for inf-2200, University of Tromso
'''

from pc import PC
from add import Add
from mux import Mux
from registerFile import RegisterFile
from instructionMemory import InstructionMemory
from dataMemory import DataMemory
from constant import Constant
from controlUnit import ControlUnit
from signExtend import SignExtend
from aluControl import AluControl
from alu import Alu
from leftShift import Shift_left
from AND import AndGate
from concatenator import Concatenator
from leftShift_sixteen import Shift_left_Sixteen
from inverter import Inverter
from orGate import OrGate


class MIPSSimulator():
    '''Main class for MIPS pipeline simulator.

    Provides the main method tick(), which runs pipeline
    for one clock cycle.

    '''
    def __init__(self, memoryFile):
        self.nCycles = 0 # Used to hold number of clock cycles spent executing instructions

        self.dataMemory = DataMemory(memoryFile)
        self.instructionMemory = InstructionMemory(memoryFile)
        self.registerFile = RegisterFile()
        self.controlUnit = ControlUnit()
        self.mux2 = Mux()
        self.mux3 = Mux()
        self.mux4 = Mux()
        self.mux5 = Mux()
        self.mux6 = Mux()
        self.signExtend = SignExtend()
        self.shift_left_lui = Shift_left_Sixteen()
        self.aluControl = AluControl()
        self.alu = Alu()
        self.shiftLeft1 = Shift_left()
        self.shiftLeft2 = Shift_left()
        self.adder2 = Add()
        self.andGate = AndGate()
        self.andGate2 = AndGate()
        self.orGate = OrGate()
        self.inverter = Inverter()
        self.concatenator = Concatenator()
        self.constant4 = Constant(4)
        self.mux1 = Mux()
        self.adder = Add()
        self.pc = PC(0xbfc00000)

        # List containing all the components in the datapath
        self.elements = [self.constant4, self.adder, self.instructionMemory, self.shiftLeft2, self.concatenator, self.controlUnit, self.mux2,
                         self.registerFile, self.signExtend, self.shift_left_lui, self.shiftLeft1, self.mux3, self.aluControl, self.adder2,
                         self.alu, self.inverter, self.andGate2, self.andGate, self.orGate, self.mux1,
                         self.dataMemory, self.mux4, self.mux6, self.registerFile, self.mux5]

        self._connectCPUElements()

    def _connectCPUElements(self):
        # Connect or-gate to controllers
        self.orGate.connect(
        [],
        [],
        [(self.andGate, 'andOut'), (self.andGate2, 'andOut2')],
        ['orOut']
        )
        # Connect and-gate to controllers
        self.andGate.connect(
        [],
        [],
        [(self.controlUnit, 'branch'), (self.alu, 'zeroSignal')],
        ['andOut']
        )
        # Connect and-gate to controllers
        self.andGate2.connect(
        [],
        [],
        [(self.controlUnit, 'bne'), (self.inverter, 'inverted')],
        ['andOut2']
        )
        # Connect inverter to controllers
        self.inverter.connect(
        [],
        [],
        [(self.alu, 'zeroSignal')],
        ['inverted']
        )
        # Connect left-shift component to input source
        self.shift_left_lui.connect(
        [(self.instructionMemory, 'out6')],
        ['shifted_lui'],
        [],
        []
        )
        # Connect mux to input sources and controller
        self.mux6.connect(
        [(self.mux4, 'muxOut4'), (self.shift_left_lui, 'shifted_lui')],
        ['muxOut6'],
        [(self.controlUnit, 'lui')],
        []
        )
        # Connect mux to input sources and controller
        self.mux5.connect(
        [(self.mux1, 'muxOut'), (self.concatenator, 'concatenated') ],
        ['muxOut5'],
        [(self.controlUnit, 'jump')],
        []
        )
        # Connect concatenator to input sources
        self.concatenator.connect(
        [(self.shiftLeft2, 'shifted2'), (self.adder, 'sum')],
        ['concatenated'],
        [],
        []
        )

        # Connect left-shift component to instruction memory
        self.shiftLeft2.connect(
        [(self.instructionMemory, 'out8')],
        ['shifted2'],
        [],
        []
        )

        # Connect mux to datamemory, alu, and controlunit
        self.mux4.connect(
        [(self.alu, 'aluRes'), (self.dataMemory, 'memoryData')],
        ['muxOut4'],
        [(self.controlUnit, 'memtoReg')],
        []
        )

        # Connect datamemory to alu, registerfile, and controlunit
        self.dataMemory.connect(
        [(self.alu, 'aluRes'), (self.registerFile, 'data2')],
        ['memoryData'],
        [(self.controlUnit, 'memRead'), (self.controlUnit, 'memWrite')],
        []
        )

        # Connect alu to registerfile, mux, and controlunit
        self.alu.connect(
        [(self.registerFile, 'data1'), (self.mux3, 'muxOut3')],
        ['aluRes'],
        [(self.aluControl, 'aluSignal')],
        ['zeroSignal']
        )

        # Connect mux to registerfile, sign-extend, and controlunit
        self.mux3.connect(
        [(self.registerFile, 'data2'), (self.signExtend, 'extended')],
        ['muxOut3'],
        [(self.controlUnit, 'aluSrc')],
        []
        )

        # Connect alucontrol to instructionemmory and controlunit
        self.aluControl.connect(
        [(self.instructionMemory, 'out7')],
        [],
        [(self.controlUnit, 'aluOp')],
        ['aluSignal'],
        )
        # Shift left connected to second adder and sign extend
        self.shiftLeft1.connect(
        [(self.signExtend, 'extended')],
        ['shifted1'],
        [],
        []
        )

        # Connect sign-extend to instructionmemory
        self.signExtend.connect(
        [(self.instructionMemory, 'out6')],
        ['extended'],
        [],
        []
        )

        # Connect mux to instructionmemory and controlunit
        self.mux2.connect(
        [(self.instructionMemory, 'out4'), (self.instructionMemory, 'out5')],
        ['muxOut2'],
        [(self.controlUnit, 'regDst')],
        []
        )

        # Connect registerfile to muxes, instructionmemory, and controlunit
        self.registerFile.connect(
        [(self.instructionMemory, 'out2'), (self.instructionMemory, 'out3'), (self.mux2, 'muxOut2'), (self.mux6, 'muxOut6')],
        ['data1', 'data2'],
        [(self.controlUnit, 'regWrite')],
        []
        )

        # Connect controlunit to instructionememory
        self.controlUnit.connect(
        [(self.instructionMemory, 'out1')],
        [],
        [],
        ['regDst', 'aluSrc', 'memtoReg', 'regWrite', 'memRead', 'memWrite', 'branch', 'aluOp', 'jump', 'lui', 'bne']
        )

        # Connect instructionmemory to pc
        self.instructionMemory.connect(
        [(self.pc, 'pcAddress')],
        ['out1', 'out2', 'out3', 'out4', 'out5', 'out6', 'out7', 'out8'],
        [],
        []
        )

        # Output value 4
        self.constant4.connect(
        [],
        ['constant'],
        [],
        []
        )

        # Connect adder to other adder and left-shift
        self.adder2.connect(
        [(self.adder, 'sum'), (self.shiftLeft1, 'shifted1')],
        ['sum2'],
        [],
        []
        )
        # Connect adder to pc and constant
        self.adder.connect(
        [(self.pc, 'pcAddress'), (self.constant4, 'constant')],
        ['sum'],
        [],
        []
        )
        # Connect mux to both adders
        self.mux1.connect(
        [(self.adder, 'sum'), (self.adder2, 'sum2')],
        ['muxOut'],
        [(self.orGate, 'orOut')],
        []
        )

        # Connect pc to mux
        self.pc.connect(
        [(self.mux5, 'muxOut5')],
        ['pcAddress'],
        [],
        []
        )


    def clockCycles(self):
        '''Returns the number of clock cycles spent executing instructions.'''

        return self.nCycles

    def dataMemory(self):
        '''Returns dictionary, mapping memory addresses to data, holding
        data memory after instructions have finished executing.'''

        return self.dataMemory.memory

    def registerFile(self):
        '''Returns dictionary, mapping register numbers to data, holding
        register file after instructions have finished executing.'''

        return self.registerFile.register

    def printDataMemory(self):
        self.dataMemory.printAll()
        print()
        print("Number of cycles:")
        print(self.nCycles)

    def printRegisterFile(self):
        self.registerFile.printAll()

    def tick(self):
        '''Execute one clock cycle of pipeline.'''
        self.nCycles += 1

        self.pc.writeOutput()

        # Loop through all components
        for elem in self.elements:
            elem.readControlSignals()
            elem.readInput()
            overflow = elem.writeOutput()
            # Check for overflow
            if overflow == 'overflow':
                self.printRegisterFile()
                self.printDataMemory()
                print("Detected Overflow, Exiting...")
                print("Code Ran Successfully")
                exit()
            elem.setControlSignals()

        self.pc.readInput()
