import numpy as np


###############################################################################
# Auxiliary Methods
###############################################################################

def cry(theta, q_control, q_target, qc):
    qc.u3(theta / 2, 0, 0, q_target)
    qc.cx(q_control, q_target)
    qc.u3(-theta / 2, 0, 0, q_target)
    qc.cx(q_control, q_target)
    return qc


def ccry(theta, q_control_1, q_control_2, q_target, qc):
    qc.u3(theta / 2, 0, 0, q_target)
    qc.ccx(q_control_1, q_control_2, q_target)
    qc.u3(-theta / 2, 0, 0, q_target)
    qc.ccx(q_control_1, q_control_2, q_target)
    return qc


def multi_cry(theta, controls, target, ancillas, qc, q):
    qc.u3(theta / 2, 0, 0, q[target])
    multi_toffoli(qc, q, controls, target, ancillas)
    qc.u3(-theta / 2, 0, 0, q[target])
    multi_toffoli(qc, q, controls, target, ancillas)
    return qc


def multi_cry_q(theta, q_controls, q_target, q_ancillas, qc):
    qc.u3(theta / 2, 0, 0, q_target)
    multi_toffoli_q(qc, q_controls, q_target, q_ancillas)
    qc.u3(-theta / 2, 0, 0, q_target)
    multi_toffoli_q(qc, q_controls, q_target, q_ancillas)
    return qc

def multi_crx(theta, controls, target, ancillas, qc, q):
    qc.u3(theta / 2, -np.pi/2, np.pi/2, q[target])
    multi_toffoli(qc, q, controls, target, ancillas)
    qc.u3(-theta / 2, -np.pi/2, np.pi/2, q[target])
    multi_toffoli(qc, q, controls, target, ancillas)
    return qc


def multi_crx_q(theta, q_controls, q_target, q_ancillas, qc):
    qc.u3(theta / 2, -np.pi/2, np.pi/2, q_target)
    multi_toffoli_q(qc, q_controls, q_target, q_ancillas)
    qc.u3(-theta / 2, -np.pi/2, np.pi/2, q_target)
    multi_toffoli_q(qc, q_controls, q_target, q_ancillas)
    return qc

def ccrx(theta, q_control_1, q_control_2, q_target, qc):
    qc.u3(theta / 2, -np.pi/2, np.pi/2, q_target)
    qc.ccx(q_control_1, q_control_2, q_target)
    qc.u3(-theta / 2, -np.pi/2, np.pi/2, q_target)
    qc.ccx(q_control_1, q_control_2, q_target)
    return qc
    
"""Apply an n-controlled gate. Inputs:
controls - list of controlling qubits
qc - quantum circuit
a - ancilla register
cu - 1-controlled gate, assumed that the last argument is the control bit"""
#def cn_gate(controls, qc, a, cu, *args):
def cn_gate(controls, qc, a, phi, ulambda, theta, tgt):
    # The first Toffoli
    qc.ccx(controls[0], controls[1], a[0])
    for i in range(2,len(controls)):
        qc.ccx(controls[i], a[i-2], a[i-1])
    # Now apply the 1-controlled version of the gate with control the last ancilla bit
    qc.cu3(theta,phi,ulambda,a[len(controls)-2],tgt)

    # Uncompute ancillae
    for i in range(len(controls)-1,1,-1):
        qc.ccx(controls[i], a[i-2], a[i-1])
    qc.ccx(controls[0], controls[1], a[0])
    return qc

def controlled_hadamard(qc, q_control, q_target):
    qc.ry(-7 / 4 * np.pi, q_target)
    qc.cx(q_control, q_target)
    qc.ry(7 / 4 * np.pi, q_target)


def multi_toffoli(qc, q, controls, target, ancillas=None):
    """
    N = number of qubits
    controls = control qubits
    target = target qubit
    ancillas = ancilla qubits, len(ancillas) = len(controls) - 2
    """
    if len(controls) == 1:
        qc.cx(q[controls[0]], q[target])
    if len(controls) == 2:
        qc.ccx(q[controls[0]], q[controls[1]], q[target])
    elif len(controls) > 2 and (ancillas is None or len(ancillas) < len(controls) - 2):
        raise Exception('ERROR: need more ancillas for multi_toffoli!')
    else:
        multi_toffoli(qc, q, controls[:-1], ancillas[-1], ancillas[:-1])
        qc.ccx(q[controls[-1]], q[ancillas[-1]], q[target])
        multi_toffoli(qc, q, controls[:-1], ancillas[-1], ancillas[:-1])


def multi_toffoli_q(qc, q_controls, q_target, q_ancillas=None):
    """
    N = number of qubits
    controls = control qubits
    target = target qubit
    ancillas = ancilla qubits, len(ancillas) = len(controls) - 2
    """

    q_controls = register_to_list(q_controls)
    q_ancillas = register_to_list(q_ancillas)

    if len(q_controls) == 1:
        qc.cx(q_controls[0], q_target)
    elif len(q_controls) == 2:
        qc.ccx(q_controls[0], q_controls[1], q_target)
    elif len(q_controls) > 2 and (q_ancillas is None or len(q_ancillas) < len(q_controls) - 2):
        raise Exception('ERROR: need more ancillas for multi_toffoli!')
    else:
        multi_toffoli_q(qc, q_controls[:-1], q_ancillas[-1], q_ancillas[:-1])
        qc.ccx(q_controls[-1], q_ancillas[-1], q_target)
        multi_toffoli_q(qc, q_controls[:-1], q_ancillas[-1], q_ancillas[:-1])


def reverse_qubits(qc, q, targets):
    for i in range(int(np.floor(len(targets) / 2))):
        qc.swap(q[targets[i]], q[targets[-(1 + i)]])


def qft(circ, q):
    """n-qubit QFT on q in circ."""
    for j in range(q.size):
        for k in range(j):
            circ.cu1(np.pi/float(2**(j-k)), q[j], q[k])
        circ.h(q[j])
    return circ

# Adjustable qft. Scale is the power of the scale (e.g. if want N/2 scale =1, N/4 scale =2)
def qft_scale(circ, q, scale=1):
    """n-qubit QFT on q in circ."""
    for j in range(q.size):
        for k in range(j):
            circ.cu1(np.pi*scale/float(2**(j-k)), q[j], q[k])
        circ.h(q[j])
    #swap
#     for j in range(int(q.size/2)):
#         circ.swap(q[j],q[q.size-j-1])
    return circ

def iqft(circ, q):
    """n-qubit QFT on q in circ."""
    for j in reversed(range(q.size)):
        circ.h(q[j])
        for k in reversed(range(j)):
            circ.cu1(-np.pi/float(2**(j-k)), q[j], q[k])
        
    return circ

def iqft_scale(circ, q, scale=1):
    """n-qubit QFT on q in circ."""
    #swap
#     for j in reversed(range(int(q.size/2))):
#         circ.swap(q[j],q[q.size-j-1])
    for j in reversed(range(q.size)):
        circ.h(q[j])
        for k in reversed(range(j)):
            circ.cu1(-np.pi*scale/float(2**(j-k)), q[j], q[k])
        
    return circ

def logical_or(qc, q, i_a, i_b, i_c):
    qc.x(q[i_a])
    qc.x(q[i_b])
    qc.x(q[i_c])

    qc.ccx(q[i_a], q[i_b], q[i_c])

    qc.x(q[i_a])
    qc.x(q[i_b])


def logical_multi_or(qc, q_in, q_out, q_ancillas):
    for q in q_in:
        qc.x(q)
    multi_toffoli_q(qc, q_in, q_out, q_ancillas)
    for q in q_in:
        qc.x(q)
    qc.x(q_out)


def logical_or_inverse(qc, q, i_a, i_b, i_c):
    qc.x(q[i_b])
    qc.x(q[i_a])

    qc.ccx(q[i_a], q[i_b], q[i_c])

    qc.x(q[i_c])
    qc.x(q[i_b])
    qc.x(q[i_a])


def register_to_list(q, start=0, end=None):
    if q is None:
        return None
    if type(q) is tuple:
        return [q]
    if end is None:
        end = len(q)
    return [q[i] for i in range(start, end)]
