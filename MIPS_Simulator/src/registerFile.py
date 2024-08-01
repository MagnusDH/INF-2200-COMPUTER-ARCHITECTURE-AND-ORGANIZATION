'''
Code written for inf-2200, University of Tromso
'''

import unittest
from cpuElement import CPUElement
from testElement import TestElement
import common

class RegisterFile(CPUElement):
    def __init__(self):
        # Dictionary mapping register number to register value
        self.register = {}

        # All registers default to 0
        for i in range(0, 32):
            self.register[i] = 0

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)
        '''
        Connect registerfile to input sources and controller
        '''
        # Check if the amount of input and output is correct
        assert(len(inputSources) == 4), 'Registerfile should only have four inputs'
        assert(len(outputValueNames) == 2), 'Registerfile should only have two outputs'
        assert(len(control) == 1), 'Registerfile should only have one control signal'
        assert(len(outputSignalNames) == 0), 'Registerfile should not have any control signal output'

        # Store the keys for the input and output values
        self.inputA = inputSources[0][1]
        self.inputB = inputSources[1][1]
        self.inputC = inputSources[2][1]
        self.inputD = inputSources[3][1]
        self.outputNameA = outputValueNames[0]
        self.outputNameB = outputValueNames[1]
        self.controlName = control[0][1]

    def writeOutput(self):
        regControl = self.controlSignals[self.controlName]

        # Check if control signal is valid
        assert(isinstance(regControl, int)), 'Invalid contol signal type'
        assert(regControl == 0 or regControl == 1), 'Invalid control signal value'

        # Store inputvalues
        reg1 = self.inputValues[self.inputA]
        reg2 = self.inputValues[self.inputB]
        write_reg = self.inputValues[self.inputC]
        write_data = self.inputValues[self.inputD]

        # Store values from registers
        regOut1 = self.register[reg1]
        regOut2 = self.register[reg2]

        # Output values from registers
        self.outputValues[self.outputNameA] = regOut1
        self.outputValues[self.outputNameB] = regOut2

        # Write to register if control signal is 1
        if regControl == 1:
            self.register[write_reg] = write_data

    def printAll(self):
        '''
        Print the name and value in each register.
        '''

        # Note that we won't actually use all the registers listed here...
        registerNames = ['$zero', '$at', '$v0', '$v1', '$a0', '$a1', '$a2', '$a3',
                        '$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7',
                        '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7',
                        '$t8', '$t9', '$k0', '$k1', '$gp', '$sp', '$fp', '$ra']

        print()
        print("Register file")
        print("================")
        for i in range(0, 32):
            print("%s \t=> %s (%s)" % (registerNames[i], common.fromUnsignedWordToSignedWord(self.register[i]), hex(int(self.register[i]))[:-1]))
        print("================")
        print()
        print()

# Class for testing the registerfile
class TestRegisterFile(unittest.TestCase):
    def setUp(self):
        self.register = RegisterFile()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ['dataA', 'dataB', 'dataC', 'dataD'],
            [],
            ['regControl']
        )

        self.register.connect(
            [(self.testInput, 'dataA'), (self.testInput, 'dataB'), (self.testInput, 'dataC'), (self.testInput, 'dataD')],
            ['regData1', 'regData2'],
            [(self.testInput, 'regControl')],
            []
        )

        self.testOutput.connect(
            [(self.register, 'regData1'), (self.register, 'regData2')],
            [],
            [],
            []
        )

    # Running tests on the registerfile
    # to assure correct behavior
    def test_correct_behavior(self):
        self.testInput.setOutputValue('dataA', 0)
        self.testInput.setOutputValue('dataB', 1)

        # Write 14 to register 0
        self.testInput.setOutputValue('dataC', 0)
        self.testInput.setOutputValue('dataD', 14)
        # Set write-signal to high
        self.testInput.setOutputControl('regControl', 1)
        self.register.readInput()
        self.register.readControlSignals()
        self.register.writeOutput()
        self.testOutput.readInput()


        # Write the value 8 to register 1
        self.testInput.setOutputValue('dataC', 1)
        self.testInput.setOutputValue('dataD', 8)
        # Set write signal to high
        self.testInput.setOutputControl('regControl', 1)
        self.register.readInput()
        self.register.readControlSignals()
        self.register.writeOutput()
        self.testOutput.readInput()


        # Set control signal to low and check if output is correct
        self.testInput.setOutputControl('regControl', 0)
        self.register.readInput()
        self.register.readControlSignals()
        self.register.writeOutput()
        self.testOutput.readInput()

        output1 = self.testOutput.inputValues['regData1']
        output2 = self.testOutput.inputValues['regData2']
        # Check if the correct registers contain the correct values
        self.assertEqual(output1, 14)
        self.assertEqual(output2, 8)


if __name__ == '__main__':
    unittest.main()
