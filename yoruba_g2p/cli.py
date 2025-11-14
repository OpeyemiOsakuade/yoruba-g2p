import argparse
from .core import YorubaG2P


def main():
    """
    Command-line entry point for Yoruba G2P.
    Reads .lab files, converts to IPA/ASCII, builds phoneset + stats.
    """
    parser = argparse.ArgumentParser(
        description="Yoruba G2P: build IPA + ASCII dictionaries and phoneset from .lab transcripts."
    )

    parser.add_argument(
        "--lab-root",
        required=True,
        help="Root folder containing subfolders (e.g., train/valid/test) with .lab transcripts.",
    )

    parser.add_argument(
        "--splits",
        nargs="+",
        default=["train", "valid", "test"],
        help="List of subfolders under lab-root to process. Default: train valid test",
    )

    parser.add_argument(
        "--out-dir",
        default="yoruba_g2p_out",
        help="Output directory for IPA dict, ASCII dict, phoneset.txt, and stats.json",
    )

    args = parser.parse_args()

    # Instantiate G2P engine
    g2p = YorubaG2P()

    # Build all dictionaries + phoneset + stats
    result = g2p.build_all_from_labs(
        lab_root=args.lab_root,
        splits=args.splits,
        out_dir=args.out_dir,
    )

    # Print summary
    print("\n Yoruba G2P export complete.")
    print(f"  IPA dict:       {result['ipa_dict']}")
    print(f"  ASCII dict:     {result['ascii_dict']}")
    print(f"  phoneset.txt:   {result['phoneset']}")
    print(f"  stats.json:     {result['stats']}")
    print(f"  vocab size:     {result['num_vocab']}")
    print(f"  problem words:  {result['num_problem_words']}")


if __name__ == "__main__":
    main()
