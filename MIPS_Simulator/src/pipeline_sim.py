'''
Code written for inf-2200, University of Tromso
'''


'''
Pipeline implementation (not finished)
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
from pipeline_ifid import Pipeline_IfId
from pipeline_idex import Pipeline_IdEx
from pipeline_exmem import Pipeline_ExMem
from pipeline_memwb import Pipeline_MemWb


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
        self.pipeline_ifid = Pipeline_IfId()
        self.pipeline_idex = Pipeline_IdEx()
        self.pipeline_exmem = Pipeline_ExMem()
        self.pipeline_memwb = Pipeline_MemWb()

        # Lists containing the different stages of pipeline implementation
        self.pipe1 = [self.constant4, self.adder, self.instructionMemory, self.pipeline_ifid]
        self.pipe2 = [self.shiftLeft2, self.concatenator, self.controlUnit, self.mux2, self.registerFile, self.signExtend, self.pipeline_idex]
        self.pipe3 = [self.shift_left_lui, self.shiftLeft1, self.mux3, self.aluControl, self.adder2, self.alu, self.pipeline_exmem]
        self.pipe4 = [self.inverter, self.andGate2, self.andGate, self.orGate, self.mux1, self.dataMemory, self.pipeline_memwb]
        self.pipe5 = [self.mux4, self.mux6, self.registerFile, self.mux5]

        self._connectCPUElements()

    # Instruction fetch stage of pipeline
    def stage1(self):
        for elem in self.pipe1:
            elem.readControlSignals()
            elem.readInput()
            elem.writeOutput()
            elem.setControlSignals()

    # Instruction decode stage of pipeline
    def stage2(self):
        for elem in self.pipe2:
            elem.readControlSignals()
            elem.readInput()
            elem.writeOutput()
            elem.setControlSignals()
        self.stage1()

    # Execute stage of pipeline
    def stage3(self):
        for elem in self.pipe3:
            elem.readControlSignals()
            elem.readInput()
            overflow_detection = elem.writeOutput()
            if overflow_detection == 'overflow':
                self.printRegisterFile()
                self.printDataMemory()
                print("Detected Overflow, Exiting...")
                print("Code Ran Successfully")
                exit()
            elem.setControlSignals()
        self.stage2()

    # Memory stage of pipeline
    def stage4(self):
        for elem in self.pipe4:
            elem.readControlSignals()
            elem.readInput()
            elem.writeOutput()
            elem.setControlSignals()
        self.stage3()

    # Write back stage of pipeline
    def stage5(self):
        for elem in self.pipe5:
            elem.readControlSignals()
            elem.readInput()
            elem.writeOutput()
            elem.setControlSignals()
        self.stage4()

    def _connectCPUElements(self):
        # Connecting fourth pipeline
        self.pipeline_memwb.connect(
        [(self.pipeline_exmem, 'exmemConc'), (self.mux1, 'muxOut'), (self.dataMemory, 'memoryData'),
         (self.pipeline_exmem, 'exmemAlu'), (self.pipeline_exmem, 'exmemLui'), (self.pipeline_exmem, 'mux')],
        ['memwbConc', 'memwbMux1', 'memwbData', 'memwbAlu', 'memwbLui', 'memwbMux2'],
        [(self.pipeline_exmem, 'exmemMR'), (self.pipeline_exmem, 'exmemL'), (self.pipeline_exmem, 'exmemJ')],
        ['memwbMTR', 'memwbLui', 'memwbJump']
        )

        # Connecting thrid pipeline
        self.pipeline_exmem.connect(
        [(self.adder2, 'sum2'), (self.pipeline_idex, 'idexConc'), (self.alu, 'aluRes'), (self.pipeline_idex, 'idexData2'),
         (self.pipelien_idex, 'idexLui'), (self.mux2, 'muxOut2')],
        ['exmemSum2', 'exmemConc', 'exmemAlu', 'exmemData2', 'exmemLui', 'mux'],
        [(self.pipeline_idex, 'pipMemReg'), (self.pipeline_idex, 'pipregW'), (self.pipeline_idex, 'pipMemRead'),
         (self.pipeline_idex, 'pipMemWrite'), (self.pipeline_idex, 'pipBranch'), (self.pipeline_idex, 'pipJump'),
         (self.pipeline_idex, 'pipLui'), (self.pipeline_idex, 'pipbne'), (self.alu, 'zeroSignal'),],
        ['exmemMR', 'exmemRW', 'exmemMRead', 'exmemMW', 'exmemB', 'exmemJ', 'exmemL', 'exmemBne', 'exmemZ']
        )

        # Connecting second pipeline
        self.pipeline_idex.connect(
        [(self.pipeline_ifid, 'pipSum'), (self.concatenator, 'concatenated'), (self.registerFile, 'data1'),
         (self.registerFile, 'data2'), (self.signExtend, 'extended'), (self.pipeline_ifid, 'pipOut7'), (self.shift_left_lui, 'shifted_lui')],
        ['idexOut1', 'idexConc', 'idexData1', 'idexData2', 'idexExt', 'idexOut7', 'idexLui'],
        [(self.controlUnit, 'regDst'), (self.controlUnit, 'aluSrc'), (self.controlUnit, 'memtoReg'), (self.controlUnit, 'regWrite'),
         (self.controlUnit, 'memRead'), (self.controlUnit, 'memWrite'), (self.controlUnit, 'branch'), (self.controlUnit, 'aluOp'),
         (self.controlUnit, 'jump'), (self.controlUnit, 'lui'), (self.controlUnit, 'bne'), ],
        ['pipDst', 'pipSrc', 'pipMemReg' 'pipregW', 'pipMemRead', 'pipMemWrite', 'pipBranch', 'pipAluop', 'pipJump', 'pipLui', 'pipBne']
        )

        # Connecting first pipeline
        self.pipeline_ifid.connect(
        [(self.adder, 'sum'), (self.instructionMemory, 'out1'), (self.instructionMemory, 'out2'), (self.instructionMemory, 'out3'),
         (self.instructionMemory, 'out4'), (self.instructionMemory, 'out5'), (self.instructionMemory, 'out6'),
         (self.instructionMemory, 'out7'), (self.instructionMemory, 'out8')],
        ['pipSum', 'pipOut1', 'pipOut2', 'pipOut3', 'pipOut4', 'pipOut5', 'pipOut6', 'pipOut7', 'pipOut8'],
        [],
        []
        )

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

        # Connect mux to datamemory
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

        self.signExtend.connect(
        [(self.instructionMemory, 'out6')],
        ['extended'],
        [],
        []
        )

        # Mux between IM and RF
        self.mux2.connect(
        [(self.instructionMemory, 'out4'), (self.instructionMemory, 'out5')],
        ['muxOut2'],
        [(self.controlUnit, 'regDst')],
        []
        )

        self.registerFile.connect(
        [(self.instructionMemory, 'out2'), (self.instructionMemory, 'out3'), (self.mux2, 'muxOut2'), (self.mux6, 'muxOut6')],
        ['data1', 'data2'],
        [(self.controlUnit, 'regWrite')],
        []
        )

        self.controlUnit.connect(
        [(self.instructionMemory, 'out1')],
        [],
        [],
        ['regDst', 'aluSrc', 'memtoReg', 'regWrite', 'memRead', 'memWrite', 'branch', 'aluOp', 'jump', 'lui', 'bne']
        )

        self.instructionMemory.connect(
        [(self.pc, 'pcAddress')],
        ['out1', 'out2', 'out3', 'out4', 'out5', 'out6', 'out7', 'out8'],
        [],
        []
        )

        self.constant4.connect(
        [],
        ['constant'],
        [],
        []
        )

        # Second adder, connected to mux and shift left
        self.adder2.connect(
        [(self.adder, 'sum'), (self.shiftLeft1, 'shifted1')],
        ['sum2'],
        [],
        []
        )
        # Adder connected to PC
        self.adder.connect(
        [(self.pc, 'pcAddress'), (self.constant4, 'constant')],
        ['sum'],
        [],
        []
        )
        # Mux connected to and-gate and second adder
        self.mux1.connect(
        [(self.adder, 'sum'), (self.adder2, 'sum2')],
        ['muxOut'],
        [(self.orGate, 'orOut')],
        []
        )

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

    def printRegisterFile(self):
        self.registerFile.printAll()

    def tick(self):
        '''Execute one clock cycle of pipeline.'''

        self.nCycles += 1

        # The following is just a small sample implementation

        self.pc.writeOutput()
        self.stage5()
        self.pc.readInput()
