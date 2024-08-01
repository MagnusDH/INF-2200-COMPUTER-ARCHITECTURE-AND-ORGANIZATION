import unittest
from cpuElement import CPUElement
from testElement import TestElement


class AndGate(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        '''
        Connect and-gate to input sources
        '''
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        # Check if amount of input and output are correct
        assert(len(inputSources) == 0), 'And-gate should not recieve inputs'
        assert(len(outputValueNames) == 0), 'And-gate should not have any output'
        assert(len(control) == 2), 'And-gate should recieve two control signal'
        assert(len(outputSignalNames) == 1), 'And-gate should send out a control signal'

        # Store the keys for the output signals
        self.controlA = control[0][1]
        self.controlB = control[1][1]
        self.signalName = outputSignalNames[0]

    def writeOutput(self):
        pass # And-gate has no output

    # Perform AND-operation on control signals
    def setControlSignals(self):
        result = self.controlSignals[self.controlA] & self.controlSignals[self.controlB]
        self.outputControlSignals[self.signalName] = result


# Class for testing the AND-gate
class TestAND(unittest.TestCase):
    def setUp(self):
        self.andGate = AndGate()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            [],
            [],
            ['signalA', 'signalB']
        )

        self.andGate.connect(
            [],
            [],
            [(self.testInput, 'signalA'), (self.testInput, 'signalB')],
            ['signalOut']
        )

        self.testOutput.connect(
            [],
            [],
            [(self.andGate, 'signalOut')],
            []
        )

    # Testing the and-gate
    def test_correct_behavior(self):
        # Set output values which will be control
        # input for the AND-gate
        self.testInput.setOutputControl('signalA', 1)
        self.testInput.setOutputControl('signalB', 0)

        self.andGate.readControlSignals()
        self.andGate.setControlSignals()
        self.testOutput.readControlSignals()

        # Check if output is as expected
        output = self.testOutput.controlSignals['signalOut']
        self.assertEqual(output, 0)

        # Set output values which will be control
        # input for the and-gate
        self.testInput.setOutputControl('signalA', 1)
        self.testInput.setOutputControl('signalB', 1)

        self.andGate.readControlSignals()
        self.andGate.setControlSignals()
        self.testOutput.readControlSignals()

        # Check if output is as expected
        output = self.testOutput.controlSignals['signalOut']
        self.assertEqual(output, 1)


if __name__ == '__main__':
    unittest.main()
