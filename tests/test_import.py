def test_import_package():
    import yoruba_g2p
    from yoruba_g2p.core import YorubaG2P

    g2p = YorubaG2P()
    assert g2p is not None
