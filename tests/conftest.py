import pytest

@pytest.fixture
def g2p():
    from yoruba_g2p.core import YorubaG2P
    return YorubaG2P()

@pytest.fixture
def sample_words():
    return {
        "ọ̀mọ́": ["ɔ_L", "m", "ɔ_H"],
        "ọmọ": ["ɔ_M", "m", "ɔ_M"],
        "jẹ́": ["d͡ʒ", "ɛ_H"],
        "ilé": ["i_M", "l", "e_H"],
        "ẹ̀rọ̀": ["ɛ_L", "r", "ɔ_L"],
        "àwọn": ["a_L", "w", "ɔ_M", "n"],
        "ọba": ["ɔ_M", "b", "a_M"],
        "ọ̀pọ̀": ["ɔ_L", "k", "p", "ɔ_L"],
    }
