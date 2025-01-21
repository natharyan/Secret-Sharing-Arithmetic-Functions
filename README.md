# Shamir's Secret Sharing for Arbitrary Arithmetic Functions

This project implements Shamir's Secret Sharing and integrates Beaver's Multiplication to generate and compute shares for an arbitrary arithmetic function defined by the user. It is designed to explore the theoretical foundations of secret sharing and multi-party computation.

> **Note:** This implementation is intended for theoretical exploration and is not fully secure for real-world applications. It does not use client-server architectures, secure communication protocols, or other measures necessary for production-level security.

<img width="1236" alt="output" src="https://github.com/user-attachments/assets/62a022de-2846-4efd-a4f8-8320b6fcfe7f" />

---

## Table of Contents

1. [Introduction](#introduction)
2. [File Descriptions](#file-descriptions)
   - [main.py](#mainpy)
   - [secret_sharing.py](#secret_sharingpy)
   - [utils.py](#utilspy)
3. [Theory](#theory)
   - [Shamir's Secret Sharing](#shamirs-secret-sharing)
   - [Beaver's Multiplication](#beavers-multiplication)
   - [Parse Tree Construction and Evaluation](#parse-tree-construction-and-evaluation)
4. [Usage](#usage)
5. [Limitations](#limitations)
6. [License](#license)

---

## Introduction

Shamir's Secret Sharing is a cryptographic technique that divides a secret into multiple shares, requiring a threshold number of shares to reconstruct the original secret. This project extends Shamir's scheme by incorporating Beaver's Multiplication, enabling the computation of shares for arbitrary arithmetic expressions involving two secret values.

The primary goals of this project are:
- To explore the mathematics behind secret sharing schemes.
- To implement theoretical concepts like Beaver's Multiplication and Lagrange interpolation in Python.

---

## File Descriptions

### main.py

The main file orchestrates the program by:
- Accepting user inputs for two secrets (`x` and `y`), their thresholds, and the number of shares.
- Parsing and evaluating an arithmetic expression involving the secrets.
- Displaying the computed result as shares and recovering the secret using Lagrange interpolation.

Key functions:
- `shunting_yard_postfix(infix)`: Converts an infix arithmetic expression to postfix notation.
- `build_parsetree(expression)`: Constructs a binary parse tree for the arithmetic expression.
- `evaluate_tree(node)`: Recursively evaluates the parse tree using secret sharing operations.

### secret_sharing.py

This file contains:

#### **Shamir Class**

Implements Shamir's Secret Sharing:
- **`split_secret(secret)`**: Splits a secret into multiple shares based on a randomly generated polynomial.
  
  **Mathematics:**
  - A random polynomial \( f(x) = a_0 + a_1x + a_2x^2 + \ldots + a_{t-1}x^{t-1} \mod p \) is generated, where \( a_0 \) is the secret.
  - Shares are points \((x_i, f(x_i))\).

- **`recover_secret(shares, threshold)`**: Recovers the secret using Lagrange interpolation.
  
  **Mathematics:**
  - Lagrange basis polynomial for \( x \):
    \[ L_i(x) = \prod_{j \neq i} \frac{x - x_j}{x_i - x_j} \mod p \]
  - Secret (constant term):
    \[ f(0) = \sum_{i=0}^{t-1} y_i \cdot L_i(0) \mod p \]

#### **Operations Class**

Provides methods for arithmetic operations on shares:
- **Addition**: Adds two shares or a share with a public value.
- **Multiplication**: Implements Beaver's Multiplication for secure multiplication of two secrets without revealing them.

### utils.py

Contains utility functions for mathematical operations:
- **`_lagrange_interpolation_evaluate_at_x(threshold, x_eval, x_s, y_s, prime)`**:
  Efficiently evaluates the Lagrange polynomial at \( x = x_{\text{eval}} \).

- **`_lagrange_interpolation(threshold, x_s, y_s, prime)`**:
  Constructs the Lagrange polynomial as a symbolic expression.

- **`_divmod(num, denom, prime)`**:
  Computes modular division using the extended Euclidean algorithm.

---

## Theory

### Shamir's Secret Sharing

Shamir's Secret Sharing is a \( (t, n) \)-threshold scheme where:
- \( t \): Minimum number of shares required to reconstruct the secret.
- \( n \): Total number of shares distributed.

A polynomial of degree \( t-1 \) is used to encode the secret, ensuring that any \( t \) shares can recover the secret but fewer than \( t \) shares cannot.

### Beaver's Multiplication

Beaver's Multiplication enables the secure multiplication of two secrets \( x \) and \( y \) without revealing them. It uses a precomputed random triple \((a, b, c)\), where \( c = a \cdot b \mod p \). The steps are:
1. Compute \( x' = x + a \) and \( y' = y + b \).
2. Distribute \( x' \) and \( y' \).
3. Combine precomputed shares with \( x' \) and \( y' \) to derive \( x \cdot y \).

### Parse Tree Construction and Evaluation

Arithmetic expressions are parsed into a binary tree:
- Leaf nodes: Operands (public values or shares).
- Internal nodes: Operators (+, -, *, ^).

Evaluation combines operations on shares, preserving the security of secrets.

---

## Usage

1. Clone the repository.
2. Run `python src`.
3. Enter secrets, thresholds, and an arithmetic expression.
4. View the computed result as shares and the recovered secret.

