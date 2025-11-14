import os
import sys
import tempfile
import subprocess
from pathlib import Path


def test_cli_end_to_end():
    """
    Full integration test:
    - create temporary lab folder
    - write one .lab file
    - run CLI
    - verify dictionary outputs exist
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        lab_root = Path(tmpdir)
        train_dir = lab_root / "train"
        train_dir.mkdir(parents=True, exist_ok=True)

        # Create a minimal lab file
        lab_file = train_dir / "sample.lab"
        lab_file.write_text("ọ̀mọ́ jẹ́ ọba\n", encoding="utf-8")

        # Output directory
        out_dir = Path(tmpdir) / "out"

        # Ensure subprocess can import the package
        repo_root = Path(__file__).resolve().parents[1]
        env = os.environ.copy()
        env["PYTHONPATH"] = str(repo_root)

        # Run CLI via python -m yoruba_g2p.cli
        cmd = [
            sys.executable,
            "-m",
            "yoruba_g2p.cli",
            "--lab-root", str(lab_root),
            "--splits", "train",
            "--out-dir", str(out_dir),
        ]

        proc = subprocess.run(cmd, text=True, capture_output=True, env=env)

        # Debug if CLI fails
        # if proc.returncode != 0:
        #     print("CLI STDOUT:\n", proc.stdout)
        #     print("CLI STDERR:\n", proc.stderr)
        #     print("Return code:", proc.returncode)
        print("\n=== CLI STDOUT ===")
        print(proc.stdout)
        print("=== CLI STDERR ===")
        print(proc.stderr)
        print("=== RETURN CODE ===")
        print(proc.returncode)

        # Ensure CLI executed without errors
        assert proc.returncode == 0, f"CLI failed: {proc.stderr}"

        # Validate expected output files exist
        assert (out_dir / "yoruba_ipa.dict").exists()
        assert (out_dir / "yoruba_ascii.dict").exists()
        assert (out_dir / "phoneset.txt").exists()
        assert (out_dir / "stats.json").exists()

        # Confirm IPA dictionary contains expected phones
        ipa_content = (out_dir / "yoruba_ipa.dict").read_text(encoding="utf-8")
        assert "ọ̀mọ́" in ipa_content or "ọ̀mọ́".lower() in ipa_content
