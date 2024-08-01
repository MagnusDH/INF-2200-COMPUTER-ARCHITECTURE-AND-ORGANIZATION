import unittest
from cpuElement import CPUElement
from testElement import TestElement
from dataMemory import DataMemory


class Alu(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        '''
        Connect Alu to input sources and controller

        '''
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        # Checking if the amount of input and output is correct
        assert(len(inputSources) == 2)
        assert(len(outputValueNames) == 1)
        assert(len(control) == 1)
        assert(len(outputSignalNames) == 1)

        # Store the keys for the output values
        self.inputA = inputSources[0][1]
        self.inputB = inputSources[1][1]
        self.outputName = outputValueNames[0]
        self.controlName = control[0][1]
        self.signalName = outputSignalNames[0]

    def writeOutput(self):
        # Store control signal
        aluControl = self.controlSignals[self.controlName]

        assert(isinstance(aluControl, int)), 'Control signal is not an int'
        calc = self.inputValues[self.inputA] - self.inputValues[self.inputB]

        # Perform an AND-operation
        if aluControl == 0:
            self.outputValues[self.outputName] = self.inputValues[self.inputA] & self.inputValues[self.inputB]

        # Perform an OR-operation
        elif aluControl == 1:
            self.outputValues[self.outputName] = self.inputValues[self.inputA] | self.inputValues[self.inputB]

        # Perform an ADD-operation,
        # and raise exception if overflow
        elif aluControl == 2:
            res = self.inputValues[self.inputA] + self.inputValues[self.inputB]
            self.outputValues[self.outputName] = res
            if res > ((2**32)-1):
                return 'overflow'

        # Perform an ADDU-operation
        elif aluControl == 3:
            result = self.inputValues[self.inputA] + self.inputValues[self.inputB]
            result = result & ((2**32)-1)
            self.outputValues[self.outputName] = result

        # Perform a SUBU-operation
        elif aluControl == 5:
            result = self.inputValues[self.inputA] - self.inputValues[self.inputB]
            result = result & (-(2**32) + 1)
            self.outputValues[self.outputName] = result

        # Perform a SUB-operation
        elif aluControl == 6:
            result = self.inputValues[self.inputA] - self.inputValues[self.inputB]
            self.outputValues[self.outputName] = result
            if result < (-(2**32)+1):
                return 'overflow'

        # Perform a SLT-operation
        elif aluControl == 7:
            # Output 1 if input 1 is less than input 2
            if calc < 0:
                self.outputValues[self.outputName] = 1
            # Output 0 is input 2 is greater or equal to 1
            else:
                self.outputValues[self.outputName] = 0
        # Perform a NOR-operation
        elif aluControl == 12:
            self.outputValues[self.outputName] = ~(self.inputValues[self.inputA] | self.inputValues[self.inputB])

    # Set output-control signals
    def setControlSignals(self):
        calc = self.inputValues[self.inputA] - self.inputValues[self.inputB]
        # Set Zero-signal to high if inputs are equal
        if calc == 0:
            self.outputControlSignals[self.signalName] = 1

        # Set Zero-signal to low if inputs are different
        else:
            self.outputControlSignals[self.signalName] = 0

# Test class for the Alu
class TestAlu(unittest.TestCase):
    def setUp(self):
        self.alu = Alu()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['dataA', 'dataB'],
        [],
        ['aluControl']
        )

        self.alu.connect(
        [(self.testInput, 'dataA'), (self.testInput, 'dataB')],
        ['aluData'],
        [(self.testInput, 'aluControl')],
        ['signal']
        )

        self.testOutput.connect(
        [(self.alu, 'aluData')],
        [],
        [(self.alu, 'signal')],
        []
        )

    # Test AND-operation
    def test_AND(self):
        # Set input values and control signals
        # for the alu
        self.testInput.setOutputValue('dataA', 5)
        self.testInput.setOutputValue('dataB', 13)
        self.testInput.setOutputControl('aluControl', 0)

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.alu.setControlSignals()
        self.testOutput.readInput()

        # Check if output is as expected
        output = self.testOutput.inputValues['aluData']
        self.assertEqual(output, 5)

    # Test OR-operation
    def test_OR(self):
        # Set inputvalues and control signals
        # for the Alu
        self.testInput.setOutputValue('dataA', 5)
        self.testInput.setOutputValue('dataB', 13)
        self.testInput.setOutputControl('aluControl', 1)

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.alu.setControlSignals()
        self.testOutput.readInput()

        # Check if output is as expected
        output = self.testOutput.inputValues['aluData']
        self.assertEqual(output, 13)

    # Test ADD-operation
    def test_ADD(self):
        # Set inputvalues and control signals
        # for the Alu
        self.testInput.setOutputValue('dataA', 5)
        self.testInput.setOutputValue('dataB', 13)

        self.testInput.setOutputControl('aluControl', 2)

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.alu.setControlSignals()
        self.testOutput.readInput()

        # Check if output is as expected
        output = self.testOutput.inputValues['aluData']
        self.assertEqual(output, 18)

    # Test SUB-operation
    def test_SUB(self):
        # Set inputvalues and control signals
        # for the Alu
        self.testInput.setOutputValue('dataA', 5)
        self.testInput.setOutputValue('dataB', 13)
        self.testInput.setOutputControl('aluControl', 6)

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.alu.setControlSignals()
        self.testOutput.readInput()

        # Check if output is as expected
        output = self.testOutput.inputValues['aluData']
        self.assertEqual(output, -8)

    # Test if Zero-signal is correct
    def test_ZERO_signal(self):
        # Set inputvalues and control signals
        # for the Alu
        self.testInput.setOutputValue('dataA', 7)
        self.testInput.setOutputValue('dataB', 7)
        self.testInput.setOutputControl('aluControl', 0)

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.setControlSignals()
        self.testOutput.readControlSignals()

        # Check if output is as expected
        sigout = self.testOutput.controlSignals['signal']
        self.assertEqual(sigout, 1)

        # Set inputvalues and control signals
        # for the Alu
        self.testInput.setOutputValue('dataA', 8)
        self.testInput.setOutputValue('dataB', 7)
        self.testInput.setOutputControl('aluControl', 0)

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.setControlSignals()
        self.testOutput.readControlSignals()

        # Check if output is as expected
        sigout = self.testOutput.controlSignals['signal']
        self.assertEqual(sigout, 0)

    # Test NOR-operation
    def test_NOR(self):
        # Set inputvalues and control signals
        # for the Alu
        self.testInput.setOutputValue('dataA', 5)
        self.testInput.setOutputValue('dataB', 13)
        self.testInput.setOutputControl('aluControl', 12)

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.alu.setControlSignals()
        self.testOutput.readInput()

        # Check if output is as expected
        output = self.testOutput.inputValues['aluData']
        self.assertEqual(output, -14)


if __name__ == '__main__':
    unittest.main()
