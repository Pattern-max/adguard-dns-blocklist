import re
import requests
import dns.resolver
import time
import os
from typing import List, Set
from datetime import timedelta

# ========== 配置区域 ==========
UPSTREAM_RULES = [
    "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.mini.txt",
    "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/tif.medium.txt"
]
DOMESTIC_DNS = ["114.114.114.114", "180.76.76.76", "223.5.5.5"]
FOREIGN_DNS = ["8.8.8.8", "1.1.1.1", "9.9.9.9"]
OUTPUT_FILE = "final_rules.txt"

def download_rules(urls: List[str]) -> Set[str]:
    domains = set()
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            response.encoding = 'utf-8'
            for line in response.text.splitlines():
                if line.startswith('!') or not line.strip():
                    continue
                if match := re.match(r'\|\|([^/^]+)\^', line):
                    domains.add(match.group(1))
        except Exception as e:
            print(f"⚠️ 下载失败 {url}: {str(e)}")
    return domains

def is_domain_resolvable(domain: str, dns_servers: List[str]) -> bool:
    for dns in dns_servers:
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [dns]
            resolver.resolve(domain, 'A', raise_on_no_answer=False)
            return True
        except:
            continue
    return False

def main():
    print("🚀 [INFO] 开始下载上游规则...")
    all_domains = download_rules(UPSTREAM_RULES)
    total = len(all_domains)
    print(f"✅ [INFO] 成功获取 {total:,} 个域名 | 规则源: pro.mini.txt + tif.medium.txt")
    
    valid_domains = []
    start_time = time.time()
    last_log = start_time
    log_interval = 100  # 每100个域名输出详细进度
    
    for i, domain in enumerate(all_domains, 1):
        # DNS验证
        if is_domain_resolvable(domain, DOMESTIC_DNS) or is_domain_resolvable(domain, FOREIGN_DNS):
            valid_domains.append(domain)
        
        # >>>>> GitHub Actions 友好日志输出（关键！）<<<<<
        if i % log_interval == 0 or i == total:
            elapsed = time.time() - start_time
            speed = i / elapsed if elapsed > 0 else 0
            remaining = (total - i) / speed if speed > 0 else 0
            eta = str(timedelta(seconds=int(remaining)))
            
            # GitHub Actions 专用格式化日志（带时间戳+关键指标）
            print(f"⏳ [PROGRESS] {i:,}/{total:,} | {i/total*100:.1f}% | "
                  f"Speed: {speed:.1f} domains/s | ETA: {eta} | "
                  f"Valid: {len(valid_domains):,} | Invalid: {i - len(valid_domains):,}")
        # <<<<< 日志输出结束 >>>>>
        
        if i % 10 == 0:
            time.sleep(0.1)
    
    # 最终统计
    print(f"\n✅ [SUMMARY] 有效域名: {len(valid_domains):,} / {total:,} "
          f"({len(valid_domains)/total*100:.1f}%)")
    print(f"✅ [SUMMARY] 过滤无效域名: {total - len(valid_domains):,} "
          f"({(total - len(valid_domains))/total*100:.1f}%)")
    
    # 生成规则文件
    new_rules = [f'||{domain}^' for domain in valid_domains]
    with open(OUTPUT_FILE, 'w') as f:
        f.write("\n".join(new_rules))
    
    print(f"📝 [OUTPUT] 规则文件已生成: {OUTPUT_FILE} ({len(new_rules):,} 条)")
    print("✅ [SUCCESS] 任务完成！GitHub Actions 将自动提交结果")

if __name__ == "__main__":
    main()
