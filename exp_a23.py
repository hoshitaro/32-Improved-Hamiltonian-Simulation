from qiskit.aqua.utils.circuit_factory import CircuitFactory
from utils.circuit_utils import cn_gate, multi_toffoli_q
import numpy as np


class A23Factory(CircuitFactory):
    """
    When no time is provided the simulation runs for t=1.
    """
    
    def __init__(self, num_target_qubits):
        super().__init__(num_target_qubits)

    def required_ancillas(self):
        if self.num_target_qubits == 1:
            return 0
        else:
            return max(1, self._num_target_qubits - 2)

    def required_ancillas_controlled(self):
        if self.num_target_qubits == 1:
            return 0
        else:
            return max(1, self._num_target_qubits - 1)

    def build(self, qc, q, q_ancillas=None, params=1):
        # Gates for A3
        for i in range(0, self.num_target_qubits-1):
            q_controls = []
            qc.cx(q[i], q[i+1])
            q_controls.append(q[i+1])

            # Now we want controlled by 0
            qc.x(q[i])
            for j in range(i, 0, -1):
                qc.cx(q[i], q[j-1])
                q_controls.append(q[j-1])
            qc.x(q[i])

            # Multicontrolled x rotation
            if(len(q_controls)>1):
                qc = cn_gate(q_controls, qc, q_ancillas, -np.pi/2, np.pi/2, -2*params, q[i])
            else:
                qc.cu3(-2*params, -np.pi/2, np.pi/2, q_controls[0], q[i])
            # Uncompute
            qc.x(q[i])
            for j in range(0, i):
                qc.cx(q[i], q[j])
            qc.x(q[i])
            qc.cx(q[i], q[i+1])


    def build_inverse(self, qc, q, q_ancillas=None, params=1):
        self.build(qc, q, q_ancillas, -params)

    def build_controlled(self, qc, q, q_control, q_ancillas=None, params=1):
        # Gates for A3
        for i in range(0, self.num_target_qubits-1):
            q_controls = []
            q_controls.append(q_control)
            qc.cx(q[i], q[i+1])
            q_controls.append(q[i+1])

            # Now we want controlled by 0
            qc.x(q[i])
            for j in range(i, 0, -1):
                qc.cx(q[i], q[j-1])
                q_controls.append(q[j-1])
            qc.x(q[i])

            # Multicontrolled x rotation
            if(len(q_controls)>1):
                qc = cn_gate(q_controls, qc, q_ancillas, -np.pi/2, np.pi/2, -2*params, q[i])
            else:
                qc.cu3(-2*params, -np.pi/2, np.pi/2, q_controls[0], q[i])

            # Uncompute
            qc.x(q[i])
            for j in range(0, i):
                qc.cx(q[i], q[j])
            qc.x(q[i])
            qc.cx(q[i], q[i+1])

    def build_controlled_inverse(self, qc, q, q_control, q_ancillas=None, params=1):
        self.build_controlled(qc, q, q_control, q_ancillas, -params)