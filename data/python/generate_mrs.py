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
    # 过滤白名单
    if line.startswith('@@'):
        return None
    # hosts格式
    m = re.match(r'^(0\.0\.0\.0|127\.0\.0\.1)\s+([a-zA-Z0-9\-._]+)$', line)
    if m:
        domain = m.group(2).lower()
        return f"HOST,{domain},REJECT"
    # AdGuard/Adblock域名
    m = re.match(r'^\|\|([a-zA-Z0-9\-\.]+)\^$', line)
    if m:
        domain = m.group(1).lower()
        return f"HOST,{domain},REJECT"
    # 通配符：如*ads.example.com
    m = re.match(r'^\*([a-zA-Z0-9\-\.]+)$', line)
    if m:
        suffix = m.group(1).lower()
        return f"HOST-SUFFIX,{suffix},REJECT"
    # 正则表达式：/ads\.js$/
    m = re.match(r'^/(.+)/$', line)
    if m:
        return f"URL-REGEX,{m.group(1)},REJECT"
    # 单纯域名
    m = re.match(r'^([a-zA-Z0-9\-]+\.[a-zA-Z0-9\-.]+)$', line)
    if m:
        return f"HOST,{m.group(1).lower()},REJECT"
    return None

def download_and_merge(urls):
    mrs_rules = set()
    for url in urls:
        print(f"[*] Downloading: {url}")
        text = robust_get(url)
        if not text:
            continue
        for line in text.splitlines():
            line = line.strip()
            rule = adg_to_mrs(line)
            if rule:
                mrs_rules.add(rule)
    return sorted(mrs_rules)

def write_mrs(rules, outfile="data/rules/adblock.mrs"):
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    with open(outfile, "w", encoding="utf-8") as f:
        f.write("[Rule]\n")
        for r in rules:
            f.write(f"{r}\n")
    print(f"[+] Wrote {len(rules)} rules to {outfile}")

def main():
    print("[*] Generating mihomo mrs rules...")
    rules = download_and_merge(adblock_urls)
    write_mrs(rules)
    print("[*] Done.")

if __name__ == "__main__":
    main()