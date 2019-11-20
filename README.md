# #32-Improved-Hamiltonian-Simulation
For group #32 Improved Hamiltonian Simulation

The problem of Hamiltonian simulation can be described as, given a hermitian matrix H and a real number t, find a circuit for exp(iHt).

A widely used approach is to find a decomposition H = H_1 + H_2 +... + H_m such that we can find circuits for each exp(iH_j t), and then approximate exp(iHt) by a product of the exp(iH_j t) (i.e. by putting the smaller circuits in sequence) according to the e.g. Lie-Trotter and Suzuki formulae.

An example of such formula is
![](https://user-images.githubusercontent.com/5624856/69020846-37051800-09b6-11ea-8398-f6124168d4d6.png)

Here, the larger the M, the better is the approximation to exp(iHt) but also the longer the circuit gets. A solution is to run the algorithm m times, each time with a small M, e.g. for m = 3, M = 2, 3, 4. In each case we get a worse approximation that we would get with, say, M=10. However, the circuits are a lot shorter and the overall running time is shortened. Then, the results obtained in each run can be classically combined so that the lower error terms cancel and we get an approximation with the same accuracy that could be reached with the longer M=10 circuit.

The goal of the project would be to implement a circuit in-place version of the above with Qiskit. The idea itself and a description of the implementation is given in https://arxiv.org/pdf/1907.11679.pdf .

* Paper 1 (for description of V): https://arxiv.org/pdf/1202.5822.pdf
* Paper 2 (for description of a_j): https://arxiv.org/pdf/1907.11679.pdf
# Members
Qiskit Coach: @anedumla  
@hoshitaro  
@haoyudoingthings  
@itsuka021  
@masamuch  


# Code
The main code for our project is Five_circuit.ipynb

# Result
![](https://github.com/hoshitaro/32-Improved-Hamiltonian-Simulation/blob/master/%2332_result.png)
