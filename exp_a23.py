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
        # Gates for A2
        qc.u3(-2*params, -np.pi/2, np.pi/2, q[0])

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

        # Below method linear in nb - too slow for few qubits
        # # Gates for A2
        # qc.u3(-2*params, -np.pi/2, np.pi/2, q[0])

        # # Gates for A3
        # # Shit by +1 all basis states except 0 and nb-1. Last ancilla qubit contains flag for 0 and -1
        # q_controls=[]
        # qa = []
        # for i in range(0, q.size-1):
        #     qa.append(q_ancillas[i])
        # qc.x(q_ancillas[q.size-1])
        # for i in range(0, q.size):
        #     q_controls.append(q[i])
        # multi_toffoli_q(qc, q_controls, q_ancillas[q.size-1], qa)
        # for i in range(0,q.size):
        #     qc.x(q[i])
        # multi_toffoli_q(qc, q_controls, q_ancillas[q.size-1], qa)
        # for i in range(0,q.size):
        #     qc.x(q[i])

        # qc.ccx(q[0], q_ancillas[q.size-1], q_ancillas[0])
        # qc.cx(q_ancillas[q.size-1], q[0])
        # for i in range(1, q.size-1):
        #     qc.ccx(q[i], q_ancillas[i-1],  q_ancillas[i])
        #     qc.cx(q_ancillas[i-1], q[i])
        # qc.cx(q_ancillas[q.size-2],q[q.size-1])
        # # Uncompute ancilla
        # for i in reversed(range(1, q.size-1)):
        #     qc.x(q[i])
        #     qc.ccx(q[i], q_ancillas[i-1], q_ancillas[i])
        #     qc.x(q[i])
        # qc.x(q[0])
        # qc.ccx(q[0], q_ancillas[q.size-1], q_ancillas[0])
        # qc.x(q[0])

        # # Ry
        # qc.cu3(-2*params, -np.pi/2, np.pi/2, q_ancillas[q.size-1], q[0])

        # # Shift by -1 all basis states
        # qc.cx(q_ancillas[q.size-1], q[0])
        # qc.ccx(q[0],q_ancillas[q.size-1], q_ancillas[0])
        # for i in range(1, q.size-1):
        #     qc.x(q[i])
        #     qc.ccx(q[i], q_ancillas[i-1], q_ancillas[i])
        #     qc.x(q[i])
        #     qc.cx(q_ancillas[i-1], q[i])
        # qc.cx(q_ancillas[q.size-2],q[q.size-1])
        # # Uncompute ancilla
        # for i in reversed(range(1, q.size-1)):
        #     qc.ccx(q[i], q_ancillas[i-1], q_ancillas[i])
        # qc.ccx(q[0], q_ancillas[q.size-1], q_ancillas[0])

        # # Uncompute last ancilla
        # multi_toffoli_q(qc, q_controls, q_ancillas[q.size-1], qa)
        # for i in range(0,q.size):
        #     qc.x(q[i])
        # multi_toffoli_q(qc, q_controls, q_ancillas[q.size-1], qa)
        # for i in range(0,q.size):
        #     qc.x(q[i])


    def build_inverse(self, qc, q, q_ancillas=None, params=1):
        self.build(qc, q, q_ancillas, -params)

    def build_controlled(self, qc, q, q_control, q_ancillas=None, params=1):
        # Gates for A2 with t
        qc.cu3(-2*params, -np.pi/2, np.pi/2, q_control, q[0])

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

        # Below method linear in nb - too slow for few qubits
        # # Gates for A2
        # qc.cu3(-2*params, -np.pi/2, np.pi/2, q_control, q[0])

        # # Gates for A3
        # # Shit by +1 all basis states except 0 and nb-1. Last ancilla qubit contains flag for 0 and -1
        # qa = []
        # for i in range(0, q.size-1):
        #     qa.append(q_ancillas[i])
        # q_controls=[q_control]
        # # Only simulate if q_control is 1
        # qc.cx(q_control, q_ancillas[q.size-1])

        # for i in range(0, q.size):
        #     q_controls.append(q[i])
        # multi_toffoli_q(qc, q_controls, q_ancillas[q.size-1], qa)
        # for i in range(0,q.size):
        #     qc.x(q[i])
        # multi_toffoli_q(qc, q_controls, q_ancillas[q.size-1], qa)
        # for i in range(0,q.size):
        #     qc.x(q[i])

        # qc.ccx(q[0], q_ancillas[q.size-1], q_ancillas[0])
        # qc.cx(q_ancillas[q.size-1], q[0])
        # for i in range(1, q.size-1):
        #     qc.ccx(q[i], q_ancillas[i-1],  q_ancillas[i])
        #     qc.cx(q_ancillas[i-1], q[i])
        # qc.cx(q_ancillas[q.size-2],q[q.size-1])
        # # Uncompute ancilla
        # for i in reversed(range(1, q.size-1)):
        #     qc.x(q[i])
        #     qc.ccx(q[i], q_ancillas[i-1], q_ancillas[i])
        #     qc.x(q[i])
        # qc.x(q[0])
        # qc.ccx(q[0], q_ancillas[q.size-1], q_ancillas[0])
        # qc.x(q[0])

        # # Ry
        # qc.cu3(-2*params, -np.pi/2, np.pi/2, q_ancillas[q.size-1], q[0])

        # # Shift by -1 all basis states
        # qc.cx(q_ancillas[q.size-1], q[0])
        # qc.ccx(q[0],q_ancillas[q.size-1], q_ancillas[0])
        # for i in range(1, q.size-1):
        #     qc.x(q[i])
        #     qc.ccx(q[i], q_ancillas[i-1], q_ancillas[i])
        #     qc.x(q[i])
        #     qc.cx(q_ancillas[i-1], q[i])
        # qc.cx(q_ancillas[q.size-2],q[q.size-1])
        # # Uncompute ancilla
        # for i in reversed(range(1, q.size-1)):
        #     qc.ccx(q[i], q_ancillas[i-1], q_ancillas[i])
        # qc.ccx(q[0], q_ancillas[q.size-1], q_ancillas[0])

        # # Uncompute last ancilla
        # multi_toffoli_q(qc, q_controls, q_ancillas[q.size-1], qa)
        # for i in range(0,q.size):
        #     qc.x(q[i])
        # multi_toffoli_q(qc, q_controls, q_ancillas[q.size-1], qa)
        # for i in range(0,q.size):
        #     qc.x(q[i])
        # qc.cx(q_control, q_ancillas[q.size-1])

    def build_controlled_inverse(self, qc, q, q_control, q_ancillas=None, params=1):
        self.build_controlled(qc, q, q_control, q_ancillas, -params)