# **Variational Quantum Linear Solver (VQLS)**

## Introduction

The Variational Quantum Linear Solver, or the VQLS is a variational quantum algorithm that utilizes VQE in order to solve systems of linear equations more efficiently than classical computational algorithms.

We implemented the VQLS code by referring to the page below.

[https://qiskit.org/textbook/ch-paper-implementations/vqls.html](https://qiskit.org/textbook/ch-paper-implementations/vqls.html)

We improved the performance of the existing implementation based on qiskit, by using [Mathematica](https://www.wolfram.com/mathematica/) and [SymPy](https://www.sympy.org/).
It is expected that our codebase can be utilized in various ways in further research.

The overall procedure is as follows:

1. Simplify the circuit code written with Mathematica via [the `Simplify` function](https://reference.wolfram.com/language/ref/Simplify.html).
2. Export the code in LaTeX format.
3. Import the code to SymPy using [latex2sympy](https://github.com/augustt198/latex2sympy).

The detailed process is described below.

## Structure

Our code consists of two main parts:
The first part is the [`vqls.py`](vqls.py) file which is provided by the qiskit notebook, and the latter is the [`customVQLS.py`](latex2sympy-master/customVQLS.py) file written by us.

The main difference is the format of a circuit. When [`vqls.py`](vqls.py) applys a quantum circuit on the qiskit itself, [`customVQLS.py`](latex2sympy-master/customVQLS.py) uses Mathematica and SymPy to implement the circuit. By pipelining these two methods, we could reduce the computational cost and improve the overall performance.

## Implementation

### Dependencies

- [Python 3](https://www.python.org)
- [ANTLR v4](https://github.com/antlr/antlr4)
- [Qiskit](https://qiskit.org)
- [Pandoc](https://pandoc.org)

### Step 1. Activate latex2sympy

1. Install ANTLR 4:

```bash
pip3 install antlr4-python3-runtime==4.9
```

2. Refer to the following link and finish the process:

    [https://github.com/antlr/antlr4/blob/master/doc/getting-started.md](https://github.com/antlr/antlr4/blob/master/doc/getting-started.md)

3. And finally:

```bash
antlr4 PS.g4 -o gen
```

### Step 2. Run [customVQLS.py](latex2sympy-master/customVQLS.py)

- If you want to run the code in default settings, go the [`/latex2sympy-master`](latex2sympy-master) directory and
  execute:

```bash
py customVQLS.py
```

- If you want to run a custom code, proceed as follows:
    1. Write the circuit in Mathematica.
    2. Export the `.mml` file the `.txt` format.
    3. Converting the file via pandoc:

    ```bash
    pandoc your_exporting_file_here.txt -f html -t latex -o htest_tex_short.tex
    ```

    1. Remove the following pairs from the the converted file:
        1. the `\(`, `\)` pairs,
        2. the `\left`, `\right` pairs, and
        3. the `{❘`, `❘}` pairs.
          - **Caveat**: The 'bar's above are not typical `| (U+007C)` but 'light vertical bar's `❘ (U+2758)`.
    2. Put the created circuit in [`latex2sympy-master/result`](latex2sympy-master/result) directory.
    3. Run the [customVQLS.py](latex2sympy-master/customVQLS.py).

## Results

## Contributors
Hayeon Kim and Jaehoon Hahm

