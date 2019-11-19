from qiskit.aqua.utils.circuit_factory import CircuitFactory
from utils.circuit_utils import cn_gate, multi_toffoli_q
from exp_a4 import A4Factory
from exp_a23 import A23Factory
from exp_a1 import A1Factory
import numpy as np

class FTSDFactory(CircuitFactory):
    """
    When no time is provided the simulation runs for t=1. The target qubit is the less significant one.
    """
    def __init__(self, num_target_qubits=1):
        super().__init__(num_target_qubits)

    def required_ancillas(self):
        return 0

    def required_ancillas_controlled(self):
        return 0
    
    def build(self, qc, q, q_ancillas=None, params=1):
        pass
        # qc.u3(params, -np.pi/2, np.pi/2, q[0])

    def build_controlled(self, qc, q, q_control, q_ancillas=None, t=1, kj=1, coefficient = [], matrix_index = []):
        if len(coefficient) != len(matrix_index):
            exit("Error.")
        a1 = A1Factory(n)
        a23 = A23Factory(n)
        a4 = A4Factory(n)
        
        for j in range(kj):
          for i in range(len(matrix_index)):
              if matrix_index[i] == 0:
                  a1.build_controlled(qc, qr, q_control, q_ancillas, coefficient[i]*t/kj/2)
              elif matrix_index[i]==1:
                  a23.build_controlled(qc, qr, q_control, q_ancillas, coefficient[i]*t/kj/2)
              elif matrix_index[i]==2:
                  a4.build_controlled(qc, qr, q_control, q_ancillas, coefficient[i]*t/kj/2)
              else:
                  exit("Wrong matrix index: ", i)

    def build_inverse(self, qc, q, q_ancillas=None, params=1):
        pass
        # self.build(qc, q, q_ancillas, -params)

    def build_controlled_inverse(self, qc, q, q_control, q_ancillas=None, params=1):
        self.build_controlled(qc, q, q_control, q_ancillas, -params)


if __name__ == '__main__':
    from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, BasicAer, execute
    from exp_a4 import A4Factory
    from exp_a23 import A23Factory
    import numpy as np
    from qiskit.tools.visualization import circuit_drawer

    # number of qubits n, where size of the matrix is 2**n
    n = 2
    t = 1

    #quantum register for the matrix
    qr = QuantumRegister(n+1)
    #ancilla qubits
    qra = QuantumRegister(n-1)
    cr = ClassicalRegister(2*n)
    qc = QuantumCircuit(qr, qra, cr)


    FTSDFactory(n).build_controlled(qc, qr, qr[n], qra, t, 3, [1,2,3,4,5,6], [0,0,0,0,0,1])

    qc.draw(output='mpl',reverse_bits=True)


