import argparse
from .core import YorubaG2P


def main():
    parser = argparse.ArgumentParser(
        description="Yoruba G2P: build IPA + ASCII + phoneset from .lab transcripts."
    )
    parser.add_argument(
        "--lab-root",
        required=True,
        help="Root folder containing train/valid/test subfolders with .lab transcripts.",
    )
    parser.add_argument(
        "--splits",
        nargs="+",
        default=["train", "valid", "test"],
        help="List of subfolders under lab-root to scan (default: train valid test).",
    )
    parser.add_argument(
        "--out-dir",
        default="yoruba_g2p_out",
        help="Output directory for dictionaries, phoneset, and stats.json",
    )

    args = parser.parse_args()

    g2p = YorubaG2P()
    result = g2p.build_all_from_labs(args.lab_root, splits=args.splits, out_dir=args.out_dir)

    print("\n Yoruba G2P export complete.")
    print(f"  IPA dict:     {result['ipa_dict']}")
    print(f"  ASCII dict:   {result['ascii_dict']}")
    print(f"  phoneset.txt: {result['phoneset']}")
    print(f"  stats.json:   {result['stats']}")
    print(f"  vocab size:   {result['num_vocab']}")
    print(f"  problem words:{result['num_problem_words']}")
