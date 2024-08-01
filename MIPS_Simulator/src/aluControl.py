import unittest
from cpuElement import CPUElement
from testElement import TestElement

class AluControl(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        '''
        Connect Alu controlunit to input sources and controller
        '''
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        # Check if the amount of input and output is correct
        assert(len(inputSources) == 1), 'aluControl has only one input'
        assert(len(outputValueNames) == 0), 'aluControl has no output'
        assert(len(control) == 1), 'aluControl has only one control signal input'
        assert(len(outputSignalNames) == 1), 'aluControl has only one control signal output'

        # Store the keys for the output values
        self.inputA = inputSources[0][1]
        self.controlName = control[0][1]
        self.signalName = outputSignalNames[0]

    def writeOutput(self):
        pass # The alu controlunit has no output

    # Set control signal outputs
    def setControlSignals(self):
        input = self.inputValues[self.inputA]
        signal = self.controlSignals[self.controlName]

        # Instruction is I-type
        # Make the Alu perform ADD-operation
        if signal == 0:
            self.outputControlSignals[self.signalName] = 2

        # Instruction is BEQ/BNE
        # Make the Alu perform SUB-operation
        elif signal == 1:
            self.outputControlSignals[self.signalName] = 6

        # Instruction is R-type
        elif signal == 2:
            # Make the Alu perform ADD-operation
            if input == 32:
                self.outputControlSignals[self.signalName] = 2

            # Make the Alu perform ADDU-operation
            elif input == 33:
                self.outputControlSignals[self.signalName] = 3

            # Make the Alu perform SUB-operation
            elif input == 34:
                self.outputControlSignals[self.signalName] = 6

            # Make the Alu perform SUBU-operation
            elif input == 35:
                self.outputControlSignals[self.signalName] = 5

            # Make the Alu perform AND-operation
            elif input == 36:
                self.outputControlSignals[self.signalName] = 0

            # Make the Alu perform OR-operation
            elif input == 37:
                self.outputControlSignals[self.signalName] = 1

            # Make the Alu perform NOR-operation
            elif input == 39:
                self.outputControlSignals[self.signalName] = 12

            # Make the Alu perform SLT-operation
            elif input == 42:
                self.outputControlSignals[self.signalName] = 7

        elif signal == 3:
            self.outputControlSignals[self.signalName] = 3

# Class testing the alu control unit
class TestAluControl(unittest.TestCase):
    def setUp(self):
        self.ac = AluControl()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['dataA'],
        [],
        ['aluop']
        )

        self.ac.connect(
        [(self.testInput, 'dataA')],
        [],
        [(self.testInput, 'aluop')],
        ['signal']
        )

        self.testOutput.connect(
        [],
        [],
        [(self.ac, 'signal')],
        []
        )

    # Testing the output-signal for lw/sw-instruction
    def test_lw_sw(self):
        self.testInput.setOutputValue('dataA', 0)
        self.testInput.setOutputControl('aluop', 0)

        self.ac.readInput()
        self.ac.readControlSignals()
        self.ac.setControlSignals()
        self.testOutput.readControlSignals()

        sigout = self.testOutput.controlSignals['signal']

        self.assertEqual(sigout, 2)

    # Testing the output-signal for beq-instruction
    def test_beq(self):
        self.testInput.setOutputValue('dataA', 16)
        self.testInput.setOutputControl('aluop', 1)

        self.ac.readInput()
        self.ac.readControlSignals()
        self.ac.setControlSignals()
        self.testOutput.readControlSignals()

        sigout = self.testOutput.controlSignals['signal']

        self.assertEqual(sigout, 6)

    # Testing output-signal for r-format instruction
    def test_r_format(self):
        # Send in funct field value, resulting in add-signal output
        self.testInput.setOutputValue('dataA', 32)
        self.testInput.setOutputControl('aluop', 2)

        self.ac.readInput()
        self.ac.readControlSignals()
        self.ac.setControlSignals()
        self.testOutput.readControlSignals()

        # Check if output signal is as expected
        sigout = self.testOutput.controlSignals['signal']
        self.assertEqual(sigout, 2)


        # # Send in funct field value, resulting in sub-signal output
        self.testInput.setOutputValue('dataA', 34)
        self.testInput.setOutputControl('aluop', 2)

        self.ac.readInput()
        self.ac.readControlSignals()
        self.ac.setControlSignals()
        self.testOutput.readControlSignals()

        # Check if output signal is as expected
        sigout = self.testOutput.controlSignals['signal']
        self.assertEqual(sigout, 6)


        # Send in funct field value, resulting in and-signal output
        self.testInput.setOutputValue('dataA', 36)
        self.testInput.setOutputControl('aluop', 2)

        self.ac.readInput()
        self.ac.readControlSignals()
        self.ac.setControlSignals()
        self.testOutput.readControlSignals()

        # Check if output signal is as expected
        sigout = self.testOutput.controlSignals['signal']
        self.assertEqual(sigout, 0)


        # Send in funct field value, resulting in or-signal output
        self.testInput.setOutputValue('dataA', 37)
        self.testInput.setOutputControl('aluop', 2)

        self.ac.readInput()
        self.ac.readControlSignals()
        self.ac.setControlSignals()
        self.testOutput.readControlSignals()

        # Check if output signal is as expected
        sigout = self.testOutput.controlSignals['signal']
        self.assertEqual(sigout, 1)


        # Send in funct field value, resulting in slt-signal output
        self.testInput.setOutputValue('dataA', 42)
        self.testInput.setOutputControl('aluop', 2)

        self.ac.readInput()
        self.ac.readControlSignals()
        self.ac.setControlSignals()
        self.testOutput.readControlSignals()

        # Check if output signal is as expected
        sigout = self.testOutput.controlSignals['signal']
        self.assertEqual(sigout, 7)


if __name__ == '__main__':
    unittest.main()
