from qiskit.aqua.utils.circuit_factory import CircuitFactory

class A4Factory(CircuitFactory):
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
        qc.u3(params, -np.pi/2, np.pi/2, q[0])

    def build_controlled(self, qc, q, q_control, q_ancillas=None, params=1):
        qc.cu3(params, -np.pi/2, np.pi/2, q_control, q[0])

    def build_inverse(self, qc, q, q_ancillas=None, params=1):
        self.build(qc, q, q_ancillas, -params)

    def build_controlled_inverse(self, qc, q, q_control, q_ancillas=None, params=1):
        self.build_controlled(qc, q, q_control, q_ancillas, -params)