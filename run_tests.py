import subprocess

def run_test(cmd, name):
    print("\n" + "="*50)
    print(f"=== {name} ===")
    print("="*50 + "\n")
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = res.stdout.strip()
    err = res.stderr.strip()
    if out:
        print(out)
    if err:
        print("LOGS/ERRORS:\n" + err)

if __name__ == "__main__":
    run_test(["python", "main.py"], "main.py")
    run_test(["python", "-m", "tests.test_evaluators"], "test_evaluators")
    run_test(["python", "-m", "tests.loader_testnodb"], "loader_testnodb")
