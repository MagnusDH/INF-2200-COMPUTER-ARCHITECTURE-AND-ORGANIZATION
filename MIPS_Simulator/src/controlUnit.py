import unittest
from cpuElement import CPUElement
from testElement import TestElement


class ControlUnit(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        '''
        Connect control-unit to input source
        '''
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        # Check if the amoun tof input and output is correct
        assert(len(inputSources) == 1), 'Controlunit has only one input'
        assert(len(outputValueNames) == 0), 'Controlunit has no output'
        assert(len(control) == 0), "Controlunit has no control signal input"
        assert(len(outputSignalNames) == 11), 'Controlunit has eleven ouput control signals'

        # Store the keys for the input and output values
        self.inputA = inputSources[0][1]
        self.regDst = outputSignalNames[0]
        self.aluSrc = outputSignalNames[1]
        self.memtoReg = outputSignalNames[2]
        self.regWrite = outputSignalNames[3]
        self.memRead = outputSignalNames[4]
        self.memWrite = outputSignalNames[5]
        self.branch = outputSignalNames[6]
        self.aluOp = outputSignalNames[7]
        self.jump = outputSignalNames[8]
        self.lui = outputSignalNames[9]
        self.bne = outputSignalNames[10]

    def writeOutput(self):
        pass # Controlunit has no output


    def setControlSignals(self):
        input = self.inputValues[self.inputA]

        # Set control signals for R-format instruction
        if input == 0:
            self.outputControlSignals[self.regDst] = 1
            self.outputControlSignals[self.aluSrc] = 0
            self.outputControlSignals[self.memtoReg] = 0
            self.outputControlSignals[self.regWrite] = 1
            self.outputControlSignals[self.memRead] = 0
            self.outputControlSignals[self.memWrite] = 0
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.aluOp] = 2
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.lui] = 0
            self.outputControlSignals[self.bne] = 0

        # Set control signals for jump instruction
        elif input == 2:
            self.outputControlSignals[self.regDst] = 0
            self.outputControlSignals[self.aluSrc] = 0
            self.outputControlSignals[self.memtoReg] = 0
            self.outputControlSignals[self.regWrite] = 0
            self.outputControlSignals[self.memRead] = 0
            self.outputControlSignals[self.memWrite] = 0
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.aluOp] = 0
            self.outputControlSignals[self.jump] = 1
            self.outputControlSignals[self.lui] = 0
            self.outputControlSignals[self.bne] = 0

        # Set control signals for branch-equal instruction
        elif input == 4:
            self.outputControlSignals[self.regDst] = 0
            self.outputControlSignals[self.aluSrc] = 0
            self.outputControlSignals[self.memtoReg] = 0
            self.outputControlSignals[self.regWrite] = 0
            self.outputControlSignals[self.memRead] = 0
            self.outputControlSignals[self.memWrite] = 0
            self.outputControlSignals[self.branch] = 1
            self.outputControlSignals[self.aluOp] = 1
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.lui] = 0
            self.outputControlSignals[self.bne] = 0

        # Set control signals for branch-not-equal instruction
        elif input == 5:
            self.outputControlSignals[self.regDst] = 0
            self.outputControlSignals[self.aluSrc] = 0
            self.outputControlSignals[self.memtoReg] = 0
            self.outputControlSignals[self.regWrite] = 0
            self.outputControlSignals[self.memRead] = 0
            self.outputControlSignals[self.memWrite] = 0
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.aluOp] = 1
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.lui] = 0
            self.outputControlSignals[self.bne] = 1

        # Set control signals for addi-instruction
        elif input == 8:
            self.outputControlSignals[self.regDst] = 0
            self.outputControlSignals[self.aluSrc] = 1
            self.outputControlSignals[self.memtoReg] = 0
            self.outputControlSignals[self.regWrite] = 1
            self.outputControlSignals[self.memRead] = 0
            self.outputControlSignals[self.memWrite] = 0
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.aluOp] = 0
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.lui] = 0
            self.outputControlSignals[self.bne] = 0

        # Set control signals for addiu-instruction
        elif input == 9:
            self.outputControlSignals[self.regDst] = 0
            self.outputControlSignals[self.aluSrc] = 1
            self.outputControlSignals[self.memtoReg] = 0
            self.outputControlSignals[self.regWrite] = 1
            self.outputControlSignals[self.memRead] = 0
            self.outputControlSignals[self.memWrite] = 0
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.aluOp] = 3
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.lui] = 0
            self.outputControlSignals[self.bne] = 0

        # Set control signals for lui-instruction
        elif input == 15:
            self.outputControlSignals[self.regDst] = 0
            self.outputControlSignals[self.aluSrc] = 0
            self.outputControlSignals[self.memtoReg] = 0
            self.outputControlSignals[self.regWrite] = 1
            self.outputControlSignals[self.memRead] = 0
            self.outputControlSignals[self.memWrite] = 0
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.aluOp] = 0
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.lui] = 1
            self.outputControlSignals[self.bne] = 0

        # Set control signals for load-word instruction
        elif input == 35:
            self.outputControlSignals[self.regDst] = 0
            self.outputControlSignals[self.aluSrc] = 1
            self.outputControlSignals[self.memtoReg] = 1
            self.outputControlSignals[self.regWrite] = 1
            self.outputControlSignals[self.memRead] = 1
            self.outputControlSignals[self.memWrite] = 0
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.aluOp] = 0
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.lui] = 0
            self.outputControlSignals[self.bne] = 0

        # Set control signals for store-word instruction
        elif input == 43:
            self.outputControlSignals[self.regDst] = 0
            self.outputControlSignals[self.aluSrc] = 1
            self.outputControlSignals[self.memtoReg] = 0
            self.outputControlSignals[self.regWrite] = 0
            self.outputControlSignals[self.memRead] = 0
            self.outputControlSignals[self.memWrite] = 1
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.aluOp] = 0
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.lui] = 0
            self.outputControlSignals[self.bne] = 0


# CLass for testing the control-unit
class TestControlUnit(unittest.TestCase):
    def setUp(self):
        self.cu = ControlUnit()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['dataA'],
        [],
        []
        )

        self.cu.connect(
        [(self.testInput, 'dataA')],
        [],
        [],
        ['regdst', 'alusrc', 'memtoreg', 'regwrite', 'memread', 'memwrite', 'branch', 'aluop', 'jump', 'lui', 'bne']
        )

        self.testOutput.connect(
        [],
        [],
        [(self.cu, 'regdst'), (self.cu, 'alusrc'), (self.cu, 'memtoreg'), (self.cu, 'regwrite'),
         (self.cu, 'memread'), (self.cu, 'memwrite'), (self.cu, 'branch'), (self.cu, 'aluop'),
         (self.cu, 'jump'), (self.cu, 'lui'), (self.cu, 'bne')],
        []
        )

    # Running test for Rformat-instruction
    def test_r_format(self):
        self.testInput.setOutputValue('dataA', 0)

        self.cu.readInput()
        self.cu.setControlSignals()
        self.testOutput.readControlSignals()
        sig1 = self.testOutput.controlSignals['regdst']
        sig2 = self.testOutput.controlSignals['alusrc']
        sig3 = self.testOutput.controlSignals['memtoreg']
        sig4 = self.testOutput.controlSignals['regwrite']
        sig5 = self.testOutput.controlSignals['memread']
        sig6 = self.testOutput.controlSignals['memwrite']
        sig7 = self.testOutput.controlSignals['branch']
        sig8 = self.testOutput.controlSignals['aluop']
        sig9 = self.testOutput.controlSignals['jump']

        # Checking if output is as expected
        self.assertEqual(sig1, 1)
        self.assertEqual(sig2, 0)
        self.assertEqual(sig3, 0)
        self.assertEqual(sig4, 1)
        self.assertEqual(sig5, 0)
        self.assertEqual(sig6, 0)
        self.assertEqual(sig7, 0)
        self.assertEqual(sig8, 2)
        self.assertEqual(sig9, 0)

    # Running test for loadword-instruction
    def test_lw(self):
        self.testInput.setOutputValue('dataA', 35)
        self.cu.readInput()
        self.cu.setControlSignals()
        self.testOutput.readControlSignals()
        sig1 = self.testOutput.controlSignals['regdst']
        sig2 = self.testOutput.controlSignals['alusrc']
        sig3 = self.testOutput.controlSignals['memtoreg']
        sig4 = self.testOutput.controlSignals['regwrite']
        sig5 = self.testOutput.controlSignals['memread']
        sig6 = self.testOutput.controlSignals['memwrite']
        sig7 = self.testOutput.controlSignals['branch']
        sig8 = self.testOutput.controlSignals['aluop']
        sig9 = self.testOutput.controlSignals['jump']

        # Checking if output is as expected
        self.assertEqual(sig1, 0)
        self.assertEqual(sig2, 1)
        self.assertEqual(sig3, 1)
        self.assertEqual(sig4, 1)
        self.assertEqual(sig5, 1)
        self.assertEqual(sig6, 0)
        self.assertEqual(sig7, 0)
        self.assertEqual(sig8, 0)

    # Running test for storeword operation
    def test_sw(self):
        self.testInput.setOutputValue('dataA', 43)
        self.cu.readInput()
        self.cu.setControlSignals()
        self.testOutput.readControlSignals()
        sig1 = self.testOutput.controlSignals['alusrc']
        sig2 = self.testOutput.controlSignals['regwrite']
        sig3 = self.testOutput.controlSignals['memread']
        sig4 = self.testOutput.controlSignals['memwrite']
        sig5 = self.testOutput.controlSignals['branch']
        sig6 = self.testOutput.controlSignals['aluop']

        # Checking if output is as expected
        self.assertEqual(sig1, 1)
        self.assertEqual(sig2, 0)
        self.assertEqual(sig3, 0)
        self.assertEqual(sig4, 1)
        self.assertEqual(sig5, 0)
        self.assertEqual(sig6, 0)

    # Running test for branch-equal instruction
    def test_beq(self):
        self.testInput.setOutputValue('dataA', 4)
        self.cu.readInput()
        self.cu.setControlSignals()
        self.testOutput.readControlSignals()
        sig1 = self.testOutput.controlSignals['alusrc']
        sig2 = self.testOutput.controlSignals['regwrite']
        sig3 = self.testOutput.controlSignals['memread']
        sig4 = self.testOutput.controlSignals['memwrite']
        sig5 = self.testOutput.controlSignals['branch']
        sig6 = self.testOutput.controlSignals['aluop']

        # Checking if output is as expected
        self.assertEqual(sig1, 0)
        self.assertEqual(sig2, 0)
        self.assertEqual(sig3, 0)
        self.assertEqual(sig4, 0)
        self.assertEqual(sig5, 1)
        self.assertEqual(sig6, 1)

    # Running test for bne-instruction
    def test_bne(self):
        # Set input value
        self.testInput.setOutputValue('dataA', 5)

        self.cu.readInput()
        self.cu.setControlSignals()
        self.testOutput.readControlSignals()

        # Check if output is as expected
        sig1 = self.testOutput.controlSignals['aluop']
        sig2 = self.testOutput.controlSignals['bne']
        self.assertEqual(sig1, 1)
        self.assertEqual(sig2, 1)

    # Running test for jump-instruction
    def test_jump(self):
        self.testInput.setOutputValue('dataA', 2)

        self.cu.readInput()
        self.cu.setControlSignals()
        self.testOutput.readControlSignals()
        sig1 = self.testOutput.controlSignals['regdst']
        sig2 = self.testOutput.controlSignals['alusrc']
        sig3 = self.testOutput.controlSignals['memtoreg']
        sig4 = self.testOutput.controlSignals['regwrite']
        sig5 = self.testOutput.controlSignals['memread']
        sig6 = self.testOutput.controlSignals['memwrite']
        sig7 = self.testOutput.controlSignals['branch']
        sig8 = self.testOutput.controlSignals['aluop']
        sig9 = self.testOutput.controlSignals['jump']

        # Checking if output is as expected
        self.assertEqual(sig1, 0)
        self.assertEqual(sig2, 0)
        self.assertEqual(sig3, 0)
        self.assertEqual(sig4, 0)
        self.assertEqual(sig5, 0)
        self.assertEqual(sig6, 0)
        self.assertEqual(sig7, 0)
        self.assertEqual(sig8, 0)
        self.assertEqual(sig9, 1)

    # Running test for lui-instruction
    def test_lui(self):
        # Set input value
        self.testInput.setOutputValue('dataA', 15)

        self.cu.readInput()
        self.cu.setControlSignals()
        self.testOutput.readControlSignals()

        # CHeck if output is as expected
        sig1 = self.testOutput.controlSignals['regwrite']
        sig2 = self.testOutput.controlSignals['lui']
        self.assertEqual(sig1, 1)
        self.assertEqual(sig2, 1)


if __name__ == '__main__':
    unittest.main()
