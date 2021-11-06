# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 21:16:55 2021

@author: jakes
"""

'''
    From the Qiskit Textbook (Alpha)
    See https://qiskit.org/textbook/ch-algorithms/quantum-fourier-transform.html

    state_number is the (soon-to-be) binary number representing the starting states 
    of the qubits, e.g. 5 -> 101, i.e. qubits in states 1, 0 and 1
'''

import math
from numpy import pi
# importing Qiskit
from qiskit import QuantumCircuit, Aer
from qiskit.visualization import plot_bloch_multivector


## n-qubit solution -----------------------------------------------------------

def initial_z_state(state_number): # Code to set up the intial state automatically
    
    # Calculates the minimum required number of bits
    circuit_depth = math.floor(math.log(state_number, 2)) + 1
    
    # Sets up the circuit
    circuit = QuantumCircuit(circuit_depth)

    bin_string = bin(state_number)
    bin_string = bin_string[2:][::-1] # Reverses string for input into Qiskit
    
    
    for i in range(len(bin_string)):
        character = bin_string[i]
        
        if character == '0':
            pass
        elif character == '1':
            circuit.x(i)
    
    return circuit, circuit_depth


def qft_rotations(circuit, n):
    
    if n == 0: # Exit function if circuit is empty
        return circuit
    
    n -= 1 # Indexes start from 0
    circuit.h(n) # Apply the H-gate to the most significant qubit
    
    for qubit in range(1, n+1):
        # For each less significant qubit, we need to do a
        # smaller-angled controlled rotation: 
        circuit.cp(pi/2**(qubit), n-qubit, n) # Reversed order of rotations from Qiskit textbook example
        # They're scheme is reversed to aid with good printing, functionally the same
        
    qft_rotations(circuit, n) # Recursive function call


def swap_registers(circuit, n):
    for qubit in range(n//2):
        circuit.swap(qubit, n-qubit-1)
        
    return circuit


def qft(circuit, n):
    """QFT on the first n qubits in circuit"""
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    
    return circuit


## An example usage of the code -----------------------------------------------

if __name__ == "__main__":
   
    state_number = 10
    
    qc, qc_depth = initial_z_state(state_number)
    
    sim = Aer.get_backend("aer_simulator")
    qc_init = qc.copy()
    qc_init.save_statevector()
    statevector = sim.run(qc_init).result().get_statevector()
    plot_bloch_multivector(statevector)
    
    qft(qc, qc_depth)

    
    print (qc)