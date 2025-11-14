<p align="center">
  <!-- PyPI version -->
  <a href="https://pypi.org/project/yoruba-g2p/">
    <img src="https://img.shields.io/pypi/v/yoruba-g2p.svg?color=blue&label=PyPI%20Version" />
  </a>

  <!-- Python versions -->
  <a href="https://pypi.org/project/yoruba-g2p/">
    <img src="https://img.shields.io/pypi/pyversions/yoruba-g2p.svg" />
  </a>

  <!-- GitHub Actions CI -->
  <a href="https://github.com/OpeyemiOsakuade/yoruba-g2p/actions">
    <img src="https://github.com/OpeyemiOsakuade/yoruba-g2p/workflows/CI/badge.svg" />
  </a>

  <!-- License -->
  <a href="https://github.com/OpeyemiOsakuade/yoruba-g2p/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/OpeyemiOsakuade/yoruba-g2p.svg" />
  </a>

  <!-- Downloads -->
  <a href="https://pepy.tech/project/yoruba-g2p">
    <img src="https://static.pepy.tech/badge/yoruba-g2p" />
  </a>
</p>

<p align="center">

  <img src="https://img.shields.io/badge/Yorùbá%20NLP-Tone%20Aware-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Linguistic%20Accuracy-✓%20Yorùbá%20Verified-blueviolet?style=for-the-badge">
  <img src="https://img.shields.io/badge/Yorùbá%20G2P-🪘%20Tone%20Correct-orange?style=for-the-badge">

</p>



# 🇳🇬 Yoruba-G2P  
### **Tone-Aware Yoruba Grapheme-to-Phoneme Toolkit (IPA + ASCII + MFA-Ready)**

**Yoruba-G2P** is a fully deterministic Python package for converting **Yorùbá text → phoneme sequences**, with correct **tones**, **nasal handling**, **affricates**, and **labial-velars**.

It outputs:

- ✔ **IPA dictionary**
- ✔ **ASCII-safe dictionary** (for MFA, ESPnet, Kaldi)
- ✔ **Phoneset file**
- ✔ **Lexicon statistics**
- ✔ **CLI + Python API**
- ✔ **Works on any Yoruba transcript**
- ✔ No ML training required → fully rule-based + Epitran-backed

---

## Installation

### From PyPI (recommended)

```bash
pip install yoruba-g2p
````

### From GitHub

```bash
pip install git+https://github.com/<your-username>/yoruba-g2p.git
```

---

## Quick Start (Python API)

```python
from yoruba_g2p import YorG2P

g2p = YorG2P()
#edit these
print(g2p.to_ipa("ọ̀yọ́"))
print(g2p.to_ascii("ọ̀mọ́"))
```

Output:

```
['ɔ_L', 'm', 'ɔ_H']
['O_L', 'm', 'O_H']
```

Another example:

```python
g2p.to_ipa("àwọn")
# ['a_L', 'w', 'ɔ_M', 'n']
```

---

## Command-line Interface (CLI)

Convert a sentence:

```bash
yoruba-g2p --ipa "àwọn ọmọ ń lọ"
yoruba-g2p --ascii "àwọn ọmọ ń lọ"
```

Build lexicons from `.lab` transcripts:

```bash
yoruba-g2p build-lexicon \
  --lab-dir data/lab/train \
  --out-dir dict/
```

You will get:

```
dict/ipa.dict
dict/ascii.dict
dict/phoneset.txt
dict/stats.json
```

All **MFA-ready**.

---

## What Yoruba-G2P Produces

### **1. IPA Dictionary**

```
ọ̀mọ́    ɔ_L m ɔ_H
jẹ́      d͡ʒ ɛ_H
àwọn     a_L w ɔ_M n
```

### **2. ASCII Dictionary**

```
ọ̀mọ́    O_L m O_H
jẹ́      dZ e_H
àwọn     a_L w O_M n
```

### **3. Phoneset (phoneset.txt)**

```
a_M
a_H
a_L
e_M
e_H
e_L
ɛ_M
ɛ_H
ɛ_L
i_M
i_H
i_L
o_M
o_H
o_L
ɔ_M
ɔ_H
ɔ_L
kp
gb
s
t
d
m
n
n_H
n_L
...
```

### **4. Stats (stats.json)**

```json
{
  "num_words": 5478,
  "problem_words": 2,
  "phoneset_size": 41
}
```

---

## Theory Behind Yoruba-G2P

Yoruba tone is **lexical**, and vowels carry tone:

| Mark | Tone                     | Examples  |
| ---- | ------------------------ | --------- |
| ´    | H                        | ó, é, á   |
| `    | L                        | ò, è, à   |
| none | M                        | o, e, a   |
| ń, ǹ | syllabic nasal with tone | ńlá, ǹkan |

### The engine performs:

1. **Unicode-normalization (NFC)**
2. **Orthographic vowel + tone extraction**
3. **IPA transliteration via Epitran**
4. **IPA segmentation (phones: vowels, consonants, digraphs)**
5. **Tone reattachment** using your vowel map

   * Guarantees correct H/M/L tones
6. Handling:

   * **nasal vowels** (ɛ̃ → ɛ_M + n)
   * **syllabic nasals** (ń → n_H, ǹ → n_L, decomposed forms)
   * **affricates** (`d͡ʒ`, `t͡ʃ`)
   * **labial-velars** (`kp`, `gb`)

Outputs **IPA** or **ASCII-friendly phones** (e.g., `kp`, `gb`, `dZ`).

---

## Directory Outputs (for MFA)

If you run `build-lexicon`, your output folder will contain:

```
ipa.dict       # MFA-ready IPA lexicon
ascii.dict     # ASCII-safe lexicon
phoneset.txt   # sorted unique phones
stats.json     # statistics 
```

Then feed into MFA:

```bash
mfa train \
  --corpus wavs/ \
  --dictionary dict/ipa.dict \
  --output align_out/
```

---

## Demo Notebook

A worked example is provided:

```
demo_yoruba_g2p.ipynb
```

It includes:

* IPA & ASCII conversion
* Batch lexicon building
* Phoneset extraction
* Tone distribution visualization
* Handling problem words

---

## Project Structure

```
yoruba_g2p/
│
├── core.py     # Main G2P engine
├── utils.py    # helper rules, ASCII mapping
├── cli.py      # command line interface
└── __init__.py
```

---

## Contributing

Pull requests are welcome!

Steps:

1. Fork the repo
2. Create a new branch:
   `git checkout -b feature-name`
3. Commit changes
4. Push and open a PR

Issues, feature requests, and Yoruba orthography corrections are welcome.

---

## 📣 Citation (for research)

```
Osakuade, O. (2025). Yoruba-G2P: A tone-aware grapheme-to-phoneme converter for Yorùbá. 
https://github.com/OpeyemiOsakuade/yoruba-g2p
```

---

## License

MIT License — free for academic and commercial use.

---

## ⭐ Support Yoruba NLP

If this toolkit helps you, please give the repo a **star ⭐**
to promote more open-source resources for African languages.

---
