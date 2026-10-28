
# Lab 5: Static Code Analysis — Reflection

## 1. What is static code analysis, and why is it useful?

Static code analysis examines source code without executing it. It helps identify potential bugs, security vulnerabilities, unused code, and style violations early in development. This improves code quality and maintainability.

## 2. What did Pylint, Bandit, and Flake8 identify?

Pylint identified code-quality issues such as mutable default arguments, missing docstrings, unused variables, and poor naming conventions. Bandit identified security concerns involving `eval()`, MD5 hashing, shell execution, and insecure random-number generation. Flake8 identified formatting and style violations.

## 3. What changes did you make to improve the program?

I replaced `eval()` with validated numeric input, changed MD5 to SHA-256, used the `secrets` module for PIN generation, removed shell command execution, corrected the mutable default argument, improved exception handling, and fixed code style and documentation.

## 4. How did static analysis improve your understanding of software quality?

The lab showed that a program can run successfully and still contain security vulnerabilities and maintainability problems. Using multiple tools helped identify different categories of issues. Rerunning the tools after making changes provided evidence that the reported problems had been addressed.
