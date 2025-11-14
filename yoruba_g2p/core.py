import os
import glob
import unicodedata
import re
from collections import Counter

import epitran
import json


class YorubaG2P:
    """
    End-to-end Yoruba G2P tool:

    - Build vocab from .lab files
    - Generate IPA lexicon with tone-marked phones
    - Generate ASCII/MFA lexicon
    - Extract phoneset
    - Export stats
    """

    PUNCT_RE = re.compile(r"[.,!?;:\"'()\[\]{}<>«»“”‘’…]")

    # Orthographic vowel + tone -> (IPA vowel, tone)
    VOWEL_TONE_MAP = {
        "a":  ("a", "M"),
        "á":  ("a", "H"),
        "à":  ("a", "L"),
        "e":  ("e", "M"),
        "é":  ("e", "H"),
        "è":  ("e", "L"),
        "ẹ":  ("ɛ", "M"),
        "ẹ́": ("ɛ", "H"),
        "ẹ̀": ("ɛ", "L"),
        "i":  ("i", "M"),
        "í":  ("i", "H"),
        "ì":  ("i", "L"),
        "o":  ("o", "M"),
        "ó":  ("o", "H"),
        "ò":  ("o", "L"),
        "ọ":  ("ɔ", "M"),
        "ọ́": ("ɔ", "H"),
        "ọ̀": ("ɔ", "L"),
        "u":  ("u", "M"),
        "ú":  ("u", "H"),
        "ù":  ("u", "L"),
        # syllabic nasals
        "ń": ("n", "H"),
        "ǹ": ("n", "L"),
    }

    IPA_VOWELS = {"a", "e", "i", "o", "u", "ɛ", "ɔ"}
    VALID_VOWEL_BASES = {"a", "e", "ɛ", "i", "o", "ɔ", "u"}
    VALID_TONES = {"M", "L", "H"}

    # nasal vowels that epitran might emit
    NASAL_VOWEL_MAP = {
        "ɑ̃": ("a", "n"),
        "ã": ("a", "n"),
        "ẽ": ("e", "n"),
        "ɛ̃": ("ɛ", "n"),
        "ĩ": ("i", "n"),
        "õ": ("o", "n"),
        "ɔ̃": ("ɔ", "n"),
        "ũ": ("u", "n"),
        "ĩ": ("i", "n"),
        "ũ": ("u", "n"),
    }

    # IPA -> ASCII mapping
    IPA_TO_ASCII = {
        # vowels
        "a": "a",
        "e": "e",
        "ɛ": "E",
        "i": "i",
        "o": "o",
        "ɔ": "O",
        "u": "u",

        # consonants
        "b": "b",
        "d": "d",
        "f": "f",
        "ɡ": "g",
        "g": "g",
        "h": "h",
        "j": "j",
        "k": "k",
        "l": "l",
        "m": "m",
        "n": "n",
        "p": "p",
        "r": "r",
        "s": "s",
        "t": "t",
        "w": "w",

        # fricatives
        "ʃ": "S",
        "ʒ": "Z",

        # affricates
        "dʒ":  "dZ",
        "d͡ʒ": "dZ",
        "tʃ":  "tS",
        "t͡ʃ": "tS",

        # labial-velars
        "kp": "kp",
        "gb": "gb",
    }

    AFFRICATES = {"dʒ", "tʃ", "d͡ʒ", "t͡ʃ", "kp", "gb"}

    def __init__(self):
        self.epi = epitran.Epitran("yor-Latn")

    # -------------------
    # Text & vocab
    # -------------------
    @staticmethod
    def normalize_text(text: str) -> str:
        return unicodedata.normalize("NFC", text).lower()

    def build_vocab_from_labs(self, lab_root: str, splits=("train", "valid", "test")):
        vocab_counter = Counter()
        for split in splits:
            lab_dir = os.path.join(lab_root, split)
            lab_files = sorted(glob.glob(os.path.join(lab_dir, "*.lab")))
            for lab_path in lab_files:
                with open(lab_path, "r", encoding="utf-8") as f:
                    line = f.readline().strip()
                line = self.normalize_text(line)
                line = self.PUNCT_RE.sub("", line)
                for token in line.split():
                    if token:
                        vocab_counter[token] += 1
        # remove pure numbers
        vocab_counter = {w: f for w, f in vocab_counter.items() if not w.isdigit()}
        return vocab_counter

    # -------------------
    # Vowel & IPA helpers
    # -------------------
    def get_orthographic_vowels_and_tones(self, word: str):
        """
        From orthographic Yoruba word (NFC), return list of (ipa_vowel, tone)
        in vowel order.
        """
        word = unicodedata.normalize("NFC", word)
        vt = []
        i = 0
        while i < len(word):
            ch = word[i]
            if i + 1 < len(word):
                ch2 = word[i:i+2]
                if ch2 in self.VOWEL_TONE_MAP:
                    vt.append(self.VOWEL_TONE_MAP[ch2])
                    i += 2
                    continue
            if ch in self.VOWEL_TONE_MAP:
                vt.append(self.VOWEL_TONE_MAP[ch])
            i += 1
        return vt

    def ipa_to_phones(self, ipa_str: str):
        """
        Group affricates (dʒ, tʃ, d͡ʒ, kp, gb) and attach combining marks to base.
        """
        ipa_str = unicodedata.normalize("NFC", ipa_str)

        phones = []
        buffer = ""
        i = 0
        L = len(ipa_str)

        while i < L:
            ch = ipa_str[i]

            # combining mark → attach to buffer
            if unicodedata.category(ch).startswith("M"):
                buffer += ch
                i += 1
                continue

            # 2-char affricate/digraph
            if i + 1 < L:
                pair = ipa_str[i:i+2]
                    # labial-velars: kp, gb
                if pair == "kp" or pair == "gb":
                    if buffer:
                        phones.append(buffer)
                        buffer = ""
                    phones.append(pair)
                    i += 2
                    continue

                if pair in self.AFFRICATES:
                    if buffer:
                        phones.append(buffer)
                    buffer = ""
                    phones.append(pair)
                    i += 2
                    continue

            # 3-char with tie-bar (for safety)
            if i + 2 < L:
                triple = ipa_str[i:i+3]
                if triple in self.AFFRICATES:
                    if buffer:
                        phones.append(buffer)
                    buffer = triple
                    i += 3
                    continue

            # flush buffer & start new
            if buffer:
                phones.append(buffer)
            buffer = ch
            i += 1

        if buffer:
            phones.append(buffer)

        return phones

    def is_vowel_phone(self, phone: str) -> bool:
        """
        Vowel-like if base (strip combining marks) is vowel or syllabic nasal.
        """
        phone = unicodedata.normalize("NFC", phone)
        base = ''.join(ch for ch in phone if unicodedata.category(ch)[0] != "M")
        return base in self.IPA_VOWELS or base in {"ń", "ǹ"}

    def clean_phone_token_ipa(self, token: str):
        """
        Clean a single IPA-level token.

        Returns:
          - string, e.g. 'ɔ_L', 'm', 'd͡ʃ'
          - or list of strings, e.g. ['i_M','n'] for nasal vowels
          - or None
        """
        token = unicodedata.normalize("NFC", token)

        # junk
        if token in {"—", "-", "", None}:
            return None
        if token.isdigit():
            return None

        # nasal vowels → vowel_M + 'n'
        if token in self.NASAL_VOWEL_MAP:
            base, nseg = self.NASAL_VOWEL_MAP[token]
            return [f"{base}_M", "n"]

        # syllabic nasals (single-character words or segments)
        if token == "ń":
            return "n_H"
        if token == "ǹ":
            return "n_L"

        # decomposed syllabic nasal (n + combining marks)
        if token.startswith("n") and len(token) > 1:
            combining = token[1:]
            if any(unicodedata.category(c).startswith("M") for c in combining):
                names = [unicodedata.name(c, "") for c in combining]
                if any("ACUTE" in nm for nm in names):
                    return "n_H"
                if any("GRAVE" in nm for nm in names):
                    return "n_L"
                if any("TILDE" in nm for nm in names):
                    return "n_M"
                return "n_M"

        # orthographic vowels leaking through
        if token in self.VOWEL_TONE_MAP:
            base, tone = self.VOWEL_TONE_MAP[token]
            return f"{base}_{tone}"

        # affricates and labial-velars
        if token in {"d͡ʒ", "dʒ", "t͡ʃ", "tʃ", "kp", "gb"}:
            return token

        # already vowel_tone like 'a_H'
        if "_" in token:
            base, tone = token.split("_", 1)
            if base in self.VALID_VOWEL_BASES and tone in self.VALID_TONES:
                return token
            else:
                return None

        # tone-aware bare vowel handling
        base = ''.join(ch for ch in token if unicodedata.category(ch)[0] != "M")
        if base in self.VALID_VOWEL_BASES:
            # preserve tone if acute/grave present
            if "́" in token:
                return f"{base}_H"
            if "̀" in token:
                return f"{base}_L"
            return f"{base}_M"

        # consonant / other
        if base:
            return base

        return None

    def yoruba_word_to_ipa_phones(self, word: str):
        """
        Convert Yoruba orthographic word → list of IPA-level phones with tones.
        Returns (phones, ok_flag)
        """
        word_norm = unicodedata.normalize("NFC", word.lower())

        # special-case standalone syllabic nasals
        if word_norm == "ń":
            return ["n_H"], True
        if word_norm == "ǹ":
            return ["n_L"], True

        # 1) Epitran IPA
        ipa = self.epi.transliterate(word_norm)
        ipa = unicodedata.normalize("NFC", ipa)

        # 2) Segment IPA
        ipa_phones = self.ipa_to_phones(ipa)

        # 3) Vowel sequences (orth vs IPA)
        orth_vowels_tones = self.get_orthographic_vowels_and_tones(word_norm)
        ipa_vowel_seq = [p for p in ipa_phones if self.is_vowel_phone(p)]

        out = []
        vt_idx = 0
        ok = True

        if len(ipa_vowel_seq) != len(orth_vowels_tones):
            # fallback: no exact alignment
            ok = False
            for p in ipa_phones:
                cleaned = self.clean_phone_token_ipa(p)
                if cleaned:
                    if isinstance(cleaned, list):
                        out.extend(cleaned)
                    else:
                        out.append(cleaned)
            final = out
        else:
            # tone-aligned path
            for p in ipa_phones:
                if self.is_vowel_phone(p):
                    base_vowel, tone = orth_vowels_tones[vt_idx]
                    vt_idx += 1
                    out.append(f"{base_vowel}_{tone}")
                else:
                    out.append(p)

            final = []
            for p in out:
                cleaned = self.clean_phone_token_ipa(p)
                if cleaned:
                    if isinstance(cleaned, list):
                        final.extend(cleaned)
                    else:
                        final.append(cleaned)

        # patch: restore final 'n' if orth ends with 'n' and last is a vowel
        if word_norm.endswith("n") and final:
            last = final[-1]
            if any(last.startswith(v) for v in self.VALID_VOWEL_BASES):
                final.append("n")

        # recompute OK based on vowel counts
        final_vowel_count = sum(1 for p in final if "_" in p)
        orth_vowel_count = len(orth_vowels_tones)
        if final_vowel_count == orth_vowel_count:
            ok = True

        return final, ok

    # -------------------
    # Lexicon building
    # -------------------
    def build_ipa_lexicon(self, vocab_counter):
        lexicon_ipa = {}
        problem_words = []

        for word, freq in vocab_counter.items():
            phones, ok = self.yoruba_word_to_ipa_phones(word)
            if not phones:
                problem_words.append(word)
                continue
            lexicon_ipa[word] = phones
            if not ok:
                problem_words.append(word)

        return lexicon_ipa, problem_words

    # -------------------
    # IPA → ASCII
    # -------------------
    def ipa_phone_to_ascii(self, p: str) -> str:
        p = unicodedata.normalize("NFC", p)
        if "_" in p:
            base, tone = p.split("_", 1)
            base_ascii = self.IPA_TO_ASCII.get(base, base)
            return f"{base_ascii}_{tone}"
        return self.IPA_TO_ASCII.get(p, p)

    def build_ascii_lexicon(self, lexicon_ipa):
        lexicon_ascii = {}
        for word, phones in lexicon_ipa.items():
            ascii_phones = [self.ipa_phone_to_ascii(p) for p in phones]
            ascii_phones = [p for p in ascii_phones if p]
            lexicon_ascii[word] = ascii_phones
        return lexicon_ascii

    # -------------------
    # Phoneset, stats, saving
    # -------------------
    @staticmethod
    def extract_phoneset(lexicon):
        phones = set()
        for seq in lexicon.values():
            for p in seq:
                phones.add(p)
        return sorted(phones)

    @staticmethod
    def ensure_parent(path):
        path = str(path)
        dirpath = os.path.dirname(path)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)

    @staticmethod
    def save_dict(path, lexicon):
        YorubaG2P.ensure_parent(path)
        with open(path, "w", encoding="utf-8") as f:
            for word in sorted(lexicon.keys()):
                f.write(f"{word}\t{' '.join(lexicon[word])}\n")

    @staticmethod
    def save_phoneset(path, phones):
        YorubaG2P.ensure_parent(path)
        with open(path, "w", encoding="utf-8") as f:
            for p in phones:
                f.write(p + "\n")

    @staticmethod
    def save_stats(path, vocab_counter, problem_words, ipa_phoneset, ascii_phoneset):
        YorubaG2P.ensure_parent(path)
        stats = {
            "num_vocab_items": len(vocab_counter),
            "num_ipa_entries": len(vocab_counter),
            "num_problem_words": len(problem_words),
            "problem_words_sample": problem_words[:50],
            "ipa_phoneset_size": len(ipa_phoneset),
            "ascii_phoneset_size": len(ascii_phoneset),
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

    # -------------------
    # Full pipeline
    # -------------------
    def build_all_from_labs(self, lab_root: str, splits=("train", "valid", "test"), out_dir: str = "yoruba_g2p_out"):
        # Ensure out_dir is always a string
        out_dir = str(out_dir)
        os.makedirs(out_dir, exist_ok=True)

        vocab_counter = self.build_vocab_from_labs(lab_root, splits)
        lexicon_ipa, problem_words = self.build_ipa_lexicon(vocab_counter)
        lexicon_ascii = self.build_ascii_lexicon(lexicon_ipa)

        ipa_phoneset = self.extract_phoneset(lexicon_ipa)
        ascii_phoneset = self.extract_phoneset(lexicon_ascii)

        ipa_dict_path = os.path.join(out_dir, "yoruba_ipa.dict")
        ascii_dict_path = os.path.join(out_dir, "yoruba_ascii.dict")
        phoneset_path = os.path.join(out_dir, "phoneset.txt")
        stats_path = os.path.join(out_dir, "stats.json")

        self.save_dict(ipa_dict_path, lexicon_ipa)
        self.save_dict(ascii_dict_path, lexicon_ascii)
        self.save_phoneset(phoneset_path, ascii_phoneset)
        self.save_stats(stats_path, vocab_counter, problem_words, ipa_phoneset, ascii_phoneset)

        return {
            "ipa_dict": ipa_dict_path,
            "ascii_dict": ascii_dict_path,
            "phoneset": phoneset_path,
            "stats": stats_path,
            "num_vocab": len(vocab_counter),
            "num_problem_words": len(problem_words),
        }
