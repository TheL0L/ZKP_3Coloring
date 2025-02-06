# ZKP-3Coloring

This project demonstrates a Zero-Knowledge Proof (ZKP) protocol for verifying the 3-colorability of a graph without revealing the actual coloring.

## Setup Instructions

### 1. Prerequisites

Ensure you have **Python 3.10 or higher** installed on your system. You can check your Python version by running:

```bash
python --version
```

### 2. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies. Run the following command to create a virtual environment:

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

- **Windows (Command Prompt):**
  ```bash
  venv\Scripts\activate
  ```
- **Windows (PowerShell):**
  ```powershell
  venv\Scripts\Activate.ps1
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 4. Install Required Dependencies

Ensure all dependencies are installed by running:

```bash
pip install -r requirements.txt
```

### 5. Running the Project

To execute the Zero-Knowledge Proof demonstration, run:

```bash
python main.py
```

## Project Structure

```
├── main.py          # Entry point of the application
├── Parties.py       # Defines the roles of the prover and verifier
├── Protocol.py      # Implements the ZKP protocol logic
├── requirements.txt # (Optional) Lists required dependencies
├── README.md        # Documentation
```

## About the Protocol

This project implements an interactive ZKP protocol to verify whether a given graph is 3-colorable without revealing the actual coloring. The protocol consists of a Prover and a Verifier who engage in multiple rounds of challenges to confirm the validity of the claim.

## License

This project is open-source and available for modification and distribution under the applicable license.
