def test_ascii_mapping(g2p, sample_words):
    for word, ipa_list in sample_words.items():
        ascii_list = [g2p.ipa_phone_to_ascii(p) for p in ipa_list]

        assert len(ascii_list) == len(ipa_list)

        # Ensure mapping preserves tones
        for ipa_p, ascii_p in zip(ipa_list, ascii_list):
            if "_" in ipa_p:
                ipa_tone = ipa_p.split("_")[1]
                ascii_tone = ascii_p.split("_")[1]
                assert ipa_tone == ascii_tone
