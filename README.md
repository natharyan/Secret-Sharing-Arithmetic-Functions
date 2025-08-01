# Shamir's Secret Sharing for Arithmetic Operations

This project implements Shamir's Secret Sharing and integrates Beaver's Multiplication to generate shares for arithmetic operations over two secrets.

<img width="1217" height="424" alt="Screenshot 2025-08-02 at 12 05 49 AM" src="https://github.com/user-attachments/assets/a1a49468-4c7c-4d40-8026-b714f1e7b5c8" />

---

## Introduction

Shamir's Secret Sharing is a cryptographic technique that divides a secret into multiple shares, requiring a threshold number of shares to reconstruct the original secret. This project extends Shamir's scheme by incorporating Beaver's Multiplication, enabling the computation of shares for arbitrary arithmetic expressions involving two secret values.

---

## File Descriptions

### main.py

- Accepting user inputs for two secrets (`x` and `y`), their thresholds, and the number of shares.
- Computes the shares of the evaluation using the shares of `x` and `y`.

### secret_sharing.py

This file contains:

#### **Shamir Class**

Implements Shamir's Secret Sharing:
- **`split_secret(secret)`**: Splits a secret into multiple shares based on a randomly generated polynomial.
  
  **Mathematics:**
  ```math
  f(x) = a_0 + a_1x + a_2x^2 + \ldots + a_{t-1}x^{t-1} \mod p
  
where $a_0$ is the secret. Shares are points $$(x_i, f(x_i))$$.

- **`recover_secret(shares, threshold)`**: Recovers the secret using Lagrange interpolation.
  
  **Mathematics:**
  
  Lagrange basis polynomial for \(x\):
  ```math
  L_i(x) = \prod_{j \neq i} \frac{x - x_j}{x_i - x_j} \mod p
  ```
  Secret (constant term):
  ```math
  f(0) = \sum_{i=0}^{t-1} y_i \cdot L_i(0) \mod p
  ```

#### **Operations Class**

Provides methods for arithmetic operations on shares:
- **Addition**: Adds two shares or a share with a public value.
- **Multiplication**: Implements Beaver's Multiplication for secure multiplication of two secrets without revealing them.

### utils.py

Contains utility functions for mathematical operations:
- **`_lagrange_interpolation_evaluate_at_x(threshold, x_eval, x_s, y_s, prime)`**:
  Efficiently evaluates the Lagrange polynomial at \(x = x_{\text{eval}}\).

- **`_lagrange_interpolation(threshold, x_s, y_s, prime)`**:
  Constructs the Lagrange polynomial as a symbolic expression.

- **`_divmod(num, denom, prime)`**:
  Computes modular division using the extended Euclidean algorithm.

---

## Theory

### Shamir's Secret Sharing

Shamir's Secret Sharing is a \((t, n)\)-threshold scheme where:
- \(t\): Minimum number of shares required to reconstruct the secret.
- \(n\): Total number of shares distributed.

A polynomial of degree \(t-1\) is used to encode the secret, ensuring that any \(t\) shares can recover the secret but fewer than \(t\) shares cannot.

### Beaver's Multiplication

Beaver's Multiplication enables the secure multiplication of two secrets \(x\) and \(y\) without revealing them. It uses a precomputed random triple \(([a], [b], [ab])\), where \([ab] = a \cdot b \mod p\). The multiplication works as follows:

1. Compute masked values:
   ```math
   x' = x + a \quad \text{and} \quad y' = y + b
   ```

2. The masked values \(x'\) and \(y'\) are revealed to all parties. These reveal no information about \(x\) or \(y\), as \(a\) and \(b\) are random and independent.

3. After revealing \(x'\) and \(y'\), the parties compute:
   ```math
   [xy] = (x' \cdot y') - (x' \cdot [b]) - (y' \cdot [a]) + [ab]
   ```

4. Substituting the values:
   ```math
   [xy] = [(x + a) \cdot (y + b)] - [(x + a) \cdot b] - [(y + b) \cdot a] + ab
   ```

   Expanding and simplifying:
   ```math
   [xy] = x \cdot y + a \cdot y + b \cdot x + ab - (x \cdot b + a \cdot b + b \cdot a + ab) + ab
   ```

   ```math
   [xy] = x \cdot y
   ```

Evaluation combines operations on shares, preserving the security of secrets.

---

## Usage

1. Clone the repository.
2. Run `python src/main.py`.
3. Enter secrets, thresholds, and number of shares.

