import os
import re
import requests
import time

adblock_urls = [
    "https://lingeringsound.github.io/10007_auto/adb.txt",
    "https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt",
    "https://raw.hellogithub.com/hosts",
    "https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Replenish.txt",
    "https://raw.githubusercontent.com/qq5460168/666/master/rules.txt",
    "https://raw.githubusercontent.com/2Gardon/SM-Ad-FuckU-hosts/master/SMAdHosts",
    "https://raw.githubusercontent.com/2771936993/HG/main/hg1.txt",
    "https://raw.githubusercontent.com/afwfv/DD-AD/main/rule/DD-AD.txt",
    "https://raw.githubusercontent.com/damengzhu/banad/main/jiekouAD.txt"
]

OUTPUT_TXT = "data/rules/mihomo.txt"

def robust_get(url, retries=3, timeout=30):
    for i in range(retries):
        try:
            resp = requests.get(url, timeout=timeout)
            if resp.status_code == 200:
                resp.encoding = resp.apparent_encoding
                return resp.text
        except Exception as e:
            print(f"[!] Error downloading {url} (attempt {i+1}): {e}")
            time.sleep(2)
    print(f"[!] Failed to download after {retries} attempts: {url}")
    return ""

def adg_to_mrs(line):
    if not line or line.startswith('!') or line.startswith('#'):
        return None
    if line.startswith('@@'):
        return None
    m = re.match(r'^(0\.0\.0\.0|127\.0\.0\.1)\s+([a-zA-Z0-9\-._]+)$', line)
    if m:
        return m.group(2).lower()
    m = re.match(r'^\|\|([a-zA-Z0-9\-\.]+)\^$', line)
    if m:
        return m.group(1).lower()
    m = re.match(r'^\*([a-zA-Z0-9\-\.]+)$', line)
    if m:
        return m.group(1).lower()
    m = re.match(r'^/(.+)/$', line)
    if m:
        # 返回正则表达式本身，因为 convert-ruleset 可能支持
        return m.group(1)
    m = re.match(r'^([a-zA-Z0-9\-]+\.[a-zA-Z0-9\-.]+)$', line)
    if m:
        return m.group(1).lower()
    return None

def smart_domain_dedup(rules):
    return sorted(list(set(filter(None, rules))))

def download_and_merge(urls):
    raw_rules = []
    for url in urls:
        print(f"[*] Downloading: {url}")
        text = robust_get(url)
        if not text:
            continue
        for line in text.splitlines():
            line = line.strip()
            rule = adg_to_mrs(line)
            if rule:
                raw_rules.append(rule)
    print(f"[*] Raw merged rules count: {len(raw_rules)}")
    deduped = smart_domain_dedup(raw_rules)
    print(f"[*] After smart domain dedup: {len(deduped)}")
    return deduped

def write_mihomo_txt(rules, outfile=OUTPUT_TXT):
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    with open(outfile, "w", encoding="utf-8") as f:
        for r in rules:
            f.write(f"{r}\n")
    if not os.path.exists(outfile) or os.path.getsize(outfile) < 100:
        raise RuntimeError("mihomo.txt 生成失败或文件过小，已中止工作流。")
    print(f"[+] Wrote {len(rules)} rules to {outfile}")

def main():
    print("[*] Generating mihomo.txt rules...")
    rules = download_and_merge(adblock_urls)
    write_mihomo_txt(rules, outfile=OUTPUT_TXT)
    print("[*] Done.")

if __name__ == "__main__":
    main()
