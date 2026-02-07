# setup.ps1 - 自动配置工作流脚本
Write-Host "正在设置 dns-filter-optimizer 仓库..." -ForegroundColor Cyan

# 1. 创建工作流目录
$workflowDir = ".github/workflows"
if (-Not (Test-Path $workflowDir)) {
    New-Item -ItemType Directory -Force -Path $workflowDir
    Write-Host "✓ 创建目录：$workflowDir" -ForegroundColor Green
}

# 2. 创建并写入工作流配置文件
$workflowFile = ".github/workflows/clean-hagezi.yml"
@"
name: Optimize Hagezi DNS Lists

on:
  schedule:
    - cron: '0 2 * * 1'
  workflow_dispatch:
  push:
    branches: [ main ]

jobs:
  optimize:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
    - uses: actions/checkout@v4
      with:
        token: `${{ secrets.GITHUB_TOKEN }}

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'

    - name: Install cleaner-adblock
      run: |
        git clone https://github.com/ryanbr/cleaner-adblock.git
        cd cleaner-adblock
        npm install puppeteer

    - name: Download Lists
      run: |
        curl -sSL "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt" -o pro.txt
        curl -sSL "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/tif.txt" -o tif.txt

    - name: Optimize Pro List
      run: |
        cd cleaner-adblock
        node cleaner-adblock.js ../pro.txt --export-list --check-dig-always --ignore-similar --concurrency=6
        find . -name "*pro_cleaned_*.txt" -exec mv {} ../hagezi-pro_final.txt \;

    - name: Optimize TIF List
      run: |
        cd cleaner-adblock
        node cleaner-adblock.js ../tif.txt --export-list --check-dig-always --ignore-similar --concurrency=6
        find . -name "*tif_cleaned_*.txt" -exec mv {} ../hagezi-tif_final.txt \;

    - name: Commit Results
      run: |
        git config --global user.name 'GitHub Actions Bot'
        git config --global user.email 'actions@github.com'
        git add hagezi-*_final.txt
        if git diff --staged --quiet; then
          echo "No changes."
        else
          git commit -m "Optimized: $(date '+%Y-%m-%d')"
          git push
        fi
"@ | Out-File -FilePath $workflowFile -Encoding UTF8

Write-Host "✓ 创建文件：$workflowFile" -ForegroundColor Green

# 3. 推送到GitHub
Write-Host "`n正在推送到GitHub仓库..." -ForegroundColor Cyan
git add .
git commit -m "初始化：添加自动化优化工作流"
git push origin main

Write-Host "`n✅ 完成！" -ForegroundColor Green
Write-Host "请接下来执行以下操作："
Write-Host "1. 访问 https://github.com/Pattern-max/dns-filter-optimizer" -ForegroundColor Yellow
Write-Host "2. 点击 Settings -> Actions -> General" -ForegroundColor Yellow
Write-Host "3. 找到 Workflow permissions，选择 Read and write permissions" -ForegroundColor Yellow
Write-Host "4. 保存后，在 Actions 标签页手动触发工作流运行" -ForegroundColor Yellow