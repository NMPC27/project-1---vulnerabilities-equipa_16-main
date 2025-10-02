# project-1---vulnerabilities-equipa_16

This project was developed as part of the Segurança Informática e nas Organizações course (Universidade de Aveiro, 2020-2021).
It explores common web application vulnerabilities through the implementation of a demo site (Tech Store) in two versions:

- Insecure Version – containing real security flaws
- Secure Version – hardened against the same vulnerabilities

The project demonstrates how attackers can exploit these vulnerabilities and how developers can prevent them.

## Summary

The app covers four major vulnerabilities, each aligned with the CWE (Common Weakness Enumeration) standard:

### CWE-89 – SQL Injection

- Login form bypass
- Search bar exploitation (DROP TABLE)
- Client Support form data extraction

✅ Mitigation: Prepared statements, parameter validation, and POST requests instead of GET.

### CWE-22 – Path Traversal

- Manipulation of file paths to access user images and internal directories.

✅ Mitigation: Secure path handling, restricted static access, use of functions like safe_join.

### CWE-79 – Cross-Site Scripting (XSS)

- Injection of malicious JavaScript in Client Support form.

✅ Mitigation: Proper input sanitization, avoiding unsafe string concatenation, and using prepared queries.

### CWE-522 – Insufficiently Protected Credentials

- Password change functionality could be abused to alter other users' credentials.

✅ Mitigation: Strong session validation, requiring current password for changes, enforcing password complexity, and password hashing.

### Extra Security Measures

- Strong password policies (uppercase, lowercase, numbers, symbols, ≥11 characters).
- Password hashing for secure storage.
- Encrypted session management.
- Improved error handling to avoid information leakage.


## Getting Started

### Prerequisites

    Python 3.x
    Flask
    SQLite

### Installation
    git clone https://github.com/NMPC27/project-1---vulnerabilities-equipa_16-main.git 
    cd project-1---vulnerabilities-equipa_16-main
    pip install -r requirements.txt

### Running

Run either the secure or insecure version:

    python app_insecure.py
    python app_secure.py


Access the web app at http://127.0.0.1:5000/

## References

- OWASP Top 10 – A03: Injection
- OWASP Top 10 – A07: Identification and Authentication Failures
- How Secure Is My Password

## Authors

Nuno Cunha (98124)

Filipe Silveira (97981)

Nuno Matos (97915)

Ana Rosa (98678)

⚠️ Disclaimer:
This project was created for educational purposes only. The insecure version is intentionally vulnerable and must never be used in production environments.
