```
CONTRIBUTING.md
```

---

# Contributing to yoruba-g2p

Thank you for your interest in contributing to **yoruba-g2p**!  
This project aims to provide an open, accurate, and tone-aware grapheme-to-phoneme (G2P) toolkit for Yorùbá, including IPA and ASCII phoneme mapping, MFA-ready dictionaries, and research-grade utilities.

We welcome all contributions — from bug reports to new features, documentation, and Yoruba linguistic corrections.

---

## How to Contribute

There are several ways to help:

### 1. Reporting Issues
If you find a bug, have questions, or want to suggest improvements:

1. Go to:  
   https://github.com/OpeyemiOsakuade/yoruba-g2p/issues

2. Create a **New Issue**.

3. Include:
   - What you expected to happen  
   - What actually happened  
   - Steps to reproduce  
   - Your environment (Python version, OS, MFA version, etc.)

Screenshots or examples are very helpful.

---

### 2. Submitting Pull Requests

1. **Fork** the repo  
2. Create a new branch:

   ```bash
   git checkout -b feature/my-new-feature
````

3. Install in editable mode:

   ```bash
   pip install -e .
   ```

4. Make your changes

5. Run tests (if applicable):

   ```bash
   pytest
   ```

6. Commit with a meaningful message:

   ```bash
   git commit -m "Fix tone alignment for nasal vowels"
   ```

7. Push to your fork:

   ```bash
   git push origin feature/my-new-feature
   ```

8. Open a **Pull Request**:
   [https://github.com/OpeyemiOsakuade/yoruba-g2p/pulls](https://github.com/OpeyemiOsakuade/yoruba-g2p/pulls)

Your PR will be reviewed by maintainers before merging.

---

## Development Setup

Clone the repo:

```bash
git clone https://github.com/OpeyemiOsakuade/yoruba-g2p.git
cd yoruba-g2p
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
# OR
.\.venv\Scripts\activate    # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

---

## Testing

To run the full test suite:

```bash
pytest -q
```

To run a single test:

```bash
pytest tests/test_ascii_mapping.py
```

If you add a new feature, please add at least one test.

---

## Linguistic Contributions

The Yorùbá G2P uses:

* vowel-tone extraction
* nasal handling
* orthography-to-IPA conversion
* ASCII mapping for ASR/MFA

If you are a linguist and want to propose corrections, feel free to open an issue titled:

```
Proposal: Correction to vowel/tone mapping for word X
```

Include examples and citations when possible.

---

## Documentation Updates

Good documentation is essential. You can help by improving:

* README.md
* Jupyter demo
* docstrings
* examples
* website (if added later)

---

## 🤝 Code of Conduct

This project aims to be welcoming and inclusive.
Please be respectful when interacting with others.

---

## ❤️ Thank You

Your contribution — big or small — helps improve Yorùbá NLP accessibility and tooling for the entire community.

**Ẹ ṣé gan! 🙏**
— Maintainers of yoruba-g2p

```

