# 🛡️ AdGuard规则同步仓库

本项目自动同步HaGeZi推荐的优化版AdGuard规则，适用于安卓AdGuard与AdGuard Home。

## 📦 包含规则

| 规则 | 版本 | 推荐用途 | RAW链接 |
|------|------|----------|---------|
| Pro列表 | mini版 | 广告、跟踪器拦截 | [点击复制](https://raw.githubusercontent.com/Pattern-max/adguard-rules-sync/main/rules/pro.mini.txt) |
| TIF列表 | medium版 | 威胁、恶意软件拦截 | [点击复制](https://raw.githubusercontent.com/Pattern-max/adguard-rules-sync/main/rules/tif.medium.txt) |
| Spam TLDs | 完整版 | 滥用顶级域名拦截 | [点击复制](https://raw.githubusercontent.com/Pattern-max/adguard-rules-sync/main/rules/spam-tlds.txt) |

## 🚀 使用方法

在AdGuard Home中：
1. 进入 **过滤器** → **DNS封锁清单**
2. 点击 **添加阻止列表**
3. 粘贴上方RAW链接
4. 设置适当的更新间隔（建议24小时）

## 🔄 同步状态

**最后同步时间:** 2024-01-15 12:30:45 UTC  
**下次同步:** 每小时自动运行  
**仓库活跃状态:** ✅ 正常  

## 📊 规则统计

| 规则 | 最后更新 | 条目数 |
|------|----------|--------|
| pro.mini.txt | 2024-01-15 12:30:45 UTC | 45,678 |
| tif.medium.txt | 2024-01-15 12:30:45 UTC | 28,945 |
| spam-tlds.txt | 2024-01-15 12:30:45 UTC | 1,023 |

## ⚙️ 技术细节

- **同步频率:** 每小时一次
- **失败重试:** 3次
- **监控:** GitHub Actions自动监控

---
*自动同步自 [HaGeZi's DNS Blocklists](https://github.com/hagezi/dns-blocklists)*
