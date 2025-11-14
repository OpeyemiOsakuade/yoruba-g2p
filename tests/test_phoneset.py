def test_phoneset_extraction(g2p, sample_words):
    lexicon = {w: ph for w, ph in sample_words.items()}
    phoneset = g2p.extract_phoneset(lexicon)

    assert isinstance(phoneset, list)
    assert len(phoneset) > 0

    # Every phone in lexicon must appear in phoneset
    for seq in sample_words.values():
        for p in seq:
            assert p in phoneset
