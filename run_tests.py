import subprocess
import sys


def run_test(cmd, name):
    print("\n" + "=" * 50)
    print(f"=== {name} ===")
    print("=" * 50 + "\n")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    if result.returncode != 0:
        raise SystemExit(result.returncode)


if __name__ == "__main__":
    run_test([sys.executable, "-m", "pytest", "tests", "-q"], "pytest")
