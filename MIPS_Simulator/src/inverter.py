import unittest
from cpuElement import CPUElement
from testElement import TestElement

class Inverter(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        '''
        Connecting inverter to controller
        '''
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 0), 'Inverter should not recieve inputs'
        assert(len(outputValueNames) == 0), 'Inverter should not have any output'
        assert(len(control) == 1), 'Inverter should recieve one control signal'
        assert(len(outputSignalNames) == 1), 'Inverter should send out a control signal'

        # Store the keys for the output signal
        self.controlA = control[0][1]
        self.signalName = outputSignalNames[0]

    def writeOutput(self):
        pass # Inverter has no output

    # Perform invert-operation on control signal
    def setControlSignals(self):
        controlSig = self.controlSignals[self.controlA]
        assert(isinstance(controlSig, int))
        assert(controlSig == 1 or controlSig == 0), " Control Signal should be 0 or 1"

        # Invert the control signal
        if controlSig == 1:
            invert = 0
        else:
            invert = 1
        self.outputControlSignals[self.signalName] = invert

# Class for testing the inverter
class TestInverter(unittest.TestCase):
    def setUp(self):
        self.inv = Inverter()                  
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            [],
            [],
            ['signal']
        )

        self.inv.connect(
            [],
            [],
            [(self.testInput, 'signal')],
            ['inverted']
        )

        self.testOutput.connect(
            [],
            [],
            [(self.inv, 'inverted')],
            []
        )

    # Test if the inverter works as intended
    def test_correct_behavior(self):
        # Set control input
        self.testInput.setOutputControl('signal', 0)

        self.inv.readControlSignals()
        self.inv.setControlSignals()
        self.testOutput.readControlSignals()

        # Check if output is as expected
        sigout = self.testOutput.controlSignals['inverted']
        self.assertEqual(sigout, 1)

        # Set control input
        self.testInput.setOutputControl('signal', 1)

        self.inv.readControlSignals()
        self.inv.setControlSignals()
        self.testOutput.readControlSignals()

        # Check if output is as expected
        sigout = self.testOutput.controlSignals['inverted']
        self.assertEqual(sigout, 0)

if __name__ == '__main__':
    unittest.main()
