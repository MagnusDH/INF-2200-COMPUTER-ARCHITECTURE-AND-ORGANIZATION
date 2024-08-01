import unittest
from cpuElement import CPUElement
from testElement import TestElement


class OrGate(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        '''
        Connecting or-gate to controllers
        '''
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 0), 'Or-gate should not recieve inputs'
        assert(len(outputValueNames) == 0), 'Or-gate should not have any output'
        assert(len(control) == 2), 'Or-gate should recieve two control signal'
        assert(len(outputSignalNames) == 1), 'Or-gate should send out a control signal'

        # Store the keys for the output signals
        self.controlA = control[0][1]
        self.controlB = control[1][1]
        self.signalName = outputSignalNames[0]

    def writeOutput(self):
        pass # Or-gate has no output

    # Perform AND-operation on control signals
    def setControlSignals(self):
        input1 = self.controlSignals[self.controlA]
        input2 = self.controlSignals[self.controlB]

        # Check if control signal is valid
        assert(input1 == 1 or input1 == 0), "Input 1 must be either 1 or 0"
        assert(input2 == 1 or input2 == 0), "Input 2 must be either 1 or 0"

        # Perform OR-operation on control input
        result = input1 | input2
        self.outputControlSignals[self.signalName] = result


# Class for testing the Or-gate
class TestOr(unittest.TestCase):
    def setUp(self):
        self.orGate = OrGate()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            [],
            [],
            ['signalA', 'signalB']
        )

        self.orGate.connect(
            [],
            [],
            [(self.testInput, 'signalA'), (self.testInput, 'signalB')],
            ['signalOut']
        )

        self.testOutput.connect(
            [],
            [],
            [(self.orGate, 'signalOut')],
            []
        )

    # Checking for correct output
    def test_correct_behavior(self):
        # Set output values which will be input for the Or-gate
        self.testInput.setOutputControl('signalA', 1)
        self.testInput.setOutputControl('signalB', 0)

        self.orGate.readControlSignals()
        self.orGate.setControlSignals()
        self.testOutput.readControlSignals()

        # Check if output is as expected
        output = self.testOutput.controlSignals['signalOut']
        self.assertEqual(output, 1)

        # Set output values which will be input for the Or-gate
        self.testInput.setOutputControl('signalA', 1)
        self.testInput.setOutputControl('signalB', 1)

        self.orGate.readControlSignals()
        self.orGate.setControlSignals()
        self.testOutput.readControlSignals()

        # Check if output is as expected
        output = self.testOutput.controlSignals['signalOut']
        self.assertEqual(output, 1)

        # Set output values which will be input for the Or-gate
        self.testInput.setOutputControl('signalA', 0)
        self.testInput.setOutputControl('signalB', 0)

        self.orGate.readControlSignals()
        self.orGate.setControlSignals()
        self.testOutput.readControlSignals()

        # Check if output is as expected
        output = self.testOutput.controlSignals['signalOut']
        self.assertEqual(output, 0)


if __name__ == '__main__':
    unittest.main()
