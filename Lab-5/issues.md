
# Lab 5: Static Code Analysis — Issue Table

**File:** `restaurant_order_system.py`

The line numbers below refer to the original source file before fixes.

| Issue | Type / Severity | Original Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Unsafe `eval()` | Security — Medium | 40–42 | Evaluating a supplied expression can execute arbitrary Python code. | Replaced expression evaluation with a validated numeric discount rate. |
| Weak MD5 hash | Security — High | 46–47 | MD5 is unsuitable when a cryptographically secure hash is required. | Replaced MD5 with SHA-256. |
| Shell command execution | Security — High | 54–58 | `os.system()` executes a shell command using a filename that may be untrusted. | Removed shell execution and used safe application output. |
| Mutable default argument | Code quality — Medium | 15 | `order_log=[]` can share the same list across function calls. | Changed the default to `None` and initialized the list inside the function. |
| Bare exception | Code quality / Security — Low | 23–27 | A bare `except` can hide unexpected errors. | Used `orders.pop(table_id, None)` to handle a missing table without a broad exception. |
| Insecure random PIN | Security — Low | 50–51 | `random.randint()` is not intended for security-sensitive random values. | Used `secrets.randbelow()` to generate the PIN. |
| Hardcoded secret | Security concern | Inside `main()` | A secret embedded in source code can be exposed. | Read the secret from an environment variable and avoid printing its value. |
| Unused import and variables | Code quality | Multiple | Unused names make code harder to maintain and can conceal mistakes. | Removed unused imports and variables. |
| Missing docstrings and inconsistent naming | Code quality / Style | Multiple | Functions lacked documentation and did not follow Python naming conventions. | Added docstrings and adopted `snake_case`. |
| File handling and formatting | Code quality / Style | Multiple | Manual file closing, unspecified encoding, long lines, and a missing final newline reduced maintainability. | Used a context manager, explicit UTF-8 encoding, and consistent formatting. |

## Verification Results

- **Pylint:** 10.00/10
- **Bandit:** No issues identified
- **Flake8:** No style violations reported

The final source was also executed successfully, and four security-focused unit tests passed.
