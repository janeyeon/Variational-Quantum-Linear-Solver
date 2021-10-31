# README.md

Created: October 31, 2021 3:39 PM

# **Variational Quantum Linear Solver (VQLS)**

Contributors: Hayeon Kim Jaehoon Hahm

# Introduction

The Variational Quantum Linear Solver, or the VQLS is a variational quantum algorithm that utilizes VQE in order to solve systems of linear equations more efficiently than classical computational algorithms.

We implemented the variational quantum linear solver (VQLS) code by referring to the link below.

[https://qiskit.org/textbook/ch-paper-implementations/vqls.html](https://qiskit.org/textbook/ch-paper-implementations/vqls.html)

We improved the performances of the exist code which is based on qiskit, by using `Mathematica` and `SymPy`. It is expected that this can be utilized in various ways in the further research. 

The overall procedure is as follows. 

1. Simpilfy the circuit code written by Mathematica using `Simplify` function 
2. Export the code to LaTeX format 
3. Import the code to SymPy with `latex2sympy` 

The detailed process is written in the implementation below 

# Structure

Our code is divided into two main parts.

First is `vqls.py` file which is provided by the existing qiskit, and the `customVQLS.py` file that has been simplified. 

The main different point is the format of a circuit. When `vqls.py` using quantum circuit on the qiskit itself, `customVQLS.py` using `Mathematica` and `SymPy` to implement the circuit. By using this two method, we reduced the computational cost and improved the performance.

# Implementation

## requirements

- python 3
- antlr4
- qiskit
- pandoc

## 1. activate latex2sympy

1. Import antlr4 into the python by using this command 

```bash
pip3 install antlr4-python3-runtime==4.9
```

1. Follow the link and finish the process 
  
    [https://github.com/antlr/antlr4/blob/master/doc/getting-started.md](https://github.com/antlr/antlr4/blob/master/doc/getting-started.md)
    
2. And lastly do this 

```bash
antlr4 PS.g4 -o gen
```

## 2. run [customVQLS.py](http://customVQLS.py)

- If you want to run the code right away, go the the `/latex2sympy-master` folder and proceed as follows.

```bash
py customVQLS.py
```

- If you want to run the custom code made by yourself,
    1. Write the circuit in the mathematica 
    2. export the mml file with the format of .text 
    3. converting the file into the `pandoc` 
    
    ```bash
    pandoc your_exporting_file_here.txt -f html -t latex -o htest_tex_short.tex
    ```
    
    1. Edit the converted file
        1. remove (/, /) the front and front back
        2. remove /left, /right 
    2. Put the created circuit in `latex2sympy-master/result` folder 
    3. run the [customVQLS.py](http://customVQLS.py) code

# Result

