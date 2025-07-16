import os

OUTPUT_TXT = "data/rules/mihomo.txt"

def main():
    output_dir = os.path.dirname(OUTPUT_TXT)
    os.makedirs(output_dir, exist_ok=True)
    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        for line in sys.stdin:
            f.write(line)
    print(f"[+] Wrote rules to {OUTPUT_TXT}")

if __name__ == "__main__":
    import sys
    main()
