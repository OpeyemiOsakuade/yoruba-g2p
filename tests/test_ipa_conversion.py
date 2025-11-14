def test_ipa_conversion(g2p, sample_words):
    for word, expected in sample_words.items():
        phones, ok = g2p.yoruba_word_to_ipa_phones(word)
        assert ok
        assert phones == expected
