# Experimental gate summary

The generalized inverse now has an explicit experimental Gate 0 before scalar observability and biological identifiability.

```text
Gate 0A: perturbation excites two modes
    det([v,Jv]) != 0

Gate 0B: observable sees two modes
    det([c^T;c^T J]) != 0

        |
        v
Gate 1: scalar Hankel visibility
    R=x0*x2-x1^2 != 0

        |
        v
recover T,D

        |
        v
Gate 2: independent alpha or phi

        |
        v
recover generalized feedback gain G

        |
        v
factor ecological / selection response

        |
        v
compare with exact finite sensing gap Delta_g
```

Because

\[
R
=\det\begin{pmatrix}c^\top\\c^\top J\end{pmatrix}
 \det\begin{pmatrix}v&Jv\end{pmatrix},
\]

Gate 1 is exactly the conjunction of Gate 0A and Gate 0B in the deterministic 2x2 local model.

The practical consequence is that a failed scalar inverse is not automatically a lack-of-data problem. It can be a design failure:

- the intervention never excited the missing eco-evolutionary mode;
- the measured variable is blind to that mode;
- or both.

For symmetric local dynamics with distinct eigenvalues, equal absolute weighting of the two orthogonal modes maximizes each normalized side of the visibility product.
