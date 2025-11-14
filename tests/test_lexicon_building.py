def test_lexicon_building(g2p, sample_words):

    # Pretend sample_words is the vocab
    vocab = {w: 1 for w in sample_words.keys()}

    lexicon_ipa, problem_words = g2p.build_ipa_lexicon(vocab)
    assert len(problem_words) == 0
    assert len(lexicon_ipa) == len(sample_words)

    for w in sample_words:
        assert lexicon_ipa[w] == sample_words[w]

    # ASCII lexicon
    lexicon_ascii = g2p.build_ascii_lexicon(lexicon_ipa)
    assert len(lexicon_ascii) == len(sample_words)
