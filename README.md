# Goftino Python Wrapper

A lightweight, structured Python wrapper for interacting with the **Goftino API**.
This package provides a clean client interface, typed data models, logging support, and optional data fetching utilities.

<p align="center">
  <img src="assets/PayPing_Logo.svg" alt="Logo" width="120">
</p>

---
## Disclaimer

This project is developed by the __Data Team at PayPing__ (Mana Tadbir Avatech).

This repository is __an unofficial Python wrapper for the Goftino Web API__ and is not affiliated with, endorsed by, or maintained by Goftino.  
The official Goftino API documentation is available at: [Goftino API](https://api.goftino.com/).  
  
This project is released under the MIT License, and its use is permitted under the terms of that license.  
  
All feature requests, bug reports, and improvements should be submitted through the GitHub Issues section of this repository.

---

## ✨ Features

* Clean and minimal API client (`wrapper.client`)
* Typed request/response models (`wrapper.data_types`)
* Fetcher utilities for structured retrieval (`fetcher.fetcher`)
* Logging support via `log_config.json`
* Packaged and distributable via `pyproject.toml` / `setup.py`
* Unit and manual tests included

---

## 📦 Installation

### Install from source

```bash
git clone https://github.com/ark1375/GoftinoWrapper.git
cd goftino-wrapper
pip install .
```

> Note that you may need python build tools installed on your system.

### Install in development mode

```bash
pip install -e .
```

---

## 📁 Project Structure

```
goftino-wrapper/
│
├── goftino/
│   ├── wrapper/
│   │   ├── client.py        # Main API client
│   │   ├── data_types.py    # Typed request/response models
│   │   └── __init__.py
│   │
│   ├── fetcher/
│   │   ├── fetcher.py       # Higher-level data retrieval logic
│   │   └── __init__.py
│   │
│   ├── utils.py             # Utility helpers
│   └── __init__.py
│
├── tests/                   # Unit and integration tests
├── logs/                    # Log output directory
├── log_config.json          # Logging configuration
├── pyproject.toml           # Modern packaging configuration
├── setup.py                 # Legacy packaging support
├── README.md
└── LICENSE
```

---

# 🚀 Quick Start

## 1️⃣ Initialize the Client

```python
from goftino.wrapper.client import GoftinoClient

client = GoftinoClient(
    api_key="YOUR_API_KEY"
)
```

The `GoftinoClient` is the main entry point to interact with the API.

---

## 2️⃣ Using Typed Data Models

The wrapper uses structured data classes from:

```python
from goftino.wrapper.data_types import SomeRequestType
```

Example:

```python
request = SomeRequestType(
    field1="value",
    field2=123
)

response = client.some_method(request)
print(response)
```

Typed models ensure:

* Better IDE autocomplete
* Type safety
* Cleaner request validation
* Structured API responses

---

# 🧠 Architecture Overview

## 🧩 Wrapper Layer (`wrapper/`)

This is the core of the library.

### `client.py`

* Handles authentication
* Manages HTTP requests
* Parses responses
* Centralizes error handling

The wrapper abstracts raw API calls and exposes Pythonic methods instead.

### `data_types.py`

* Defines structured request/response schemas
* Encapsulates payload formatting
* Improves clarity and maintainability

---

## 📡 Fetcher Layer (`fetcher/`)

The `fetcher` module builds on top of the client to:

* Retrieve bulk or paginated data
* Handle retries
* Normalize results
* Provide higher-level abstractions

Example usage:

```python
from goftino.fetcher.fetcher import GoftinoFetcher

fetcher = GoftinoFetcher(client)
data = fetcher.retrieve_all()
```

Use the fetcher when:

* You need bulk extraction
* You want automation around pagination
* You need structured retrieval workflows

> :warning: Consider this module as Experimental. Proceed with caution.
> 
---

## 🔧 Utilities (`utils.py`)

Shared helpers used internally by:

* Client
* Fetcher
* Logging system

This keeps the client clean and avoids duplication.

---

# 🔐 Configuration

## Logging

Logging is configured via:

```
log_config.json
```

Logs are written to:

```
logs/goftino.log
```

You can customize:

* Log level
* Format
* Output destination

---

# 🏗️ Packaging

This project supports both:

* `pyproject.toml` (PEP 517/518 modern build system)
* `setup.py` (legacy compatibility)

Build distribution:

```bash
python -m build
```

Artifacts will appear in:

```
dist/
```

Example:

```
goftino_wrapper-0.1.7.*-py3-none-any.whl
```

Install locally from built wheel:

```bash
pip install dist/goftino_wrapper-0.1.7.*-py3-none-any.whl
```

---

# 🛠 Development Workflow

### 1️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

or

```bash
pip install -e .
```

---

# 🎯 When to Use This Wrapper

Use this package if you:

* Want a structured Python interface to Goftino
* Prefer typed request/response handling
* Need clean abstraction over HTTP calls
* Want reusable retrieval workflows

---

# 📌 Example End-to-End Usage

```python
from goftino.wrapper.client import GoftinoClient
from goftino.fetcher.fetcher import GoftinoFetcher

client = GoftinoClient(api_key="YOUR_API_KEY")
fetcher = GoftinoFetcher(client)

conversations = fetcher.retrieve_all()

for conv in conversations:
    print(conv.id, conv.created_at)
```

---

# 📄 License

This project is licensed under the MIT License.

---

# 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests
4. Submit a PR

---