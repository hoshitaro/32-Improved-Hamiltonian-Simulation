from qiskit.aqua.utils.circuit_factory import CircuitFactory
import numpy as np

class A1Factory(CircuitFactory):
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
        qc.x(q)
        qc.u1(params, q)
        qc.x(q)
        qc.u1(params, q)

    def build_controlled(self, qc, q, q_control, q_ancillas=None, params=1):
        # qc.cx(q_control, q)
        # qc.cu1(params, q_control, q)
        # qc.cx(q_control, q)
        # qc.cu1(params, q_control, q)
        qc.u1(params,q_control)

    def build_inverse(self, qc, q, q_ancillas=None, params=1):
        self.build(qc, q, q_ancillas, -params)

    def build_controlled_inverse(self, qc, q, q_control, q_ancillas=None, params=1):
        self.build_controlled(qc, q, q_control, q_ancillas, -params)