def test_tone_alignment(g2p, sample_words):
    for word, expected in sample_words.items():
        ipa_out, ok = g2p.yoruba_word_to_ipa_phones(word)

        expected_tones = [p.split("_")[1] for p in expected if "_" in p]
        got_tones = [p.split("_")[1] for p in ipa_out if "_" in p]

        assert expected_tones == got_tones
