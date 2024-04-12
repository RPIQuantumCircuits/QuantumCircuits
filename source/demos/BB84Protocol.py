from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer

def bb84():
    # Create a 2 qubit QuantumRegister - two for Alice and two for Bob
    qr = QuantumRegister(2, name="q")
    # Create a 2 bit ClassicalRegister to hold measurements
    cr = ClassicalRegister(2, name="c")
    # Create a QuantumCircuit from the qr and cr
    circuit = QuantumCircuit(qr, cr)

    ## Step 1
    # Alice prepares qubits in state |+> and |-> and sends them to Bob
    circuit.h(qr[0]) # Put the first qubit in superposition
    circuit.x(qr[1]) # Put the second qubit in state |1>
    circuit.h(qr[1]) # And also in superposition
    circuit.barrier()

    ## Step 2
    # Bob measures the qubits in the {|0>, |1>} and {|+>, |->} bases randomly
    circuit.measure(qr[0], cr[0]) # Measure first qubit in Z basis
    circuit.h(qr[1]) # Change second qubit to Z basis
    circuit.measure(qr[1], cr[1]) # And measure it
    circuit.barrier()

    ## Step 3
    # Alice tells Bob which qubits were encoded in which basis
    # If Bob measured in the same basis, the bit is kept, otherwise it is discarded

    # For this demo, we'll assume that Bob happened to measure in the same basis Alice prepared the qubits in,
    # so no bits are discarded.
    # In a real protocol, this would be done by sending classical information over a public channel

    # The remaining bits form the raw key

    return circuit

# Create and draw the circuit
circuit = bb84()
print(circuit)

# Execute the circuit
backend = Aer.get_backend('qasm_simulator')
job = execute(circuit, backend, shots=1)
result = job.result()

# Get the measurement results
counts = result.get_counts(circuit)
print("Measured bits: ", counts)

# Compare a subset of the keys
# For this demo, we'll just compare the first bit
alice_bit = list(counts.keys())[0][1] # Alice's first bit
bob_bit = list(counts.keys())[0][0] # Bob's first bit

if alice_bit == bob_bit:
    print("No eavesdropping detected.")
else:
    print("Eavesdropping detected!")

# If no eavesdropping was detected, use the remaining bits as the secret key
if alice_bit == bob_bit:
    secret_key = list(counts.keys())[0][1:] # All but the first bit
    print("Secret key: ", secret_key)