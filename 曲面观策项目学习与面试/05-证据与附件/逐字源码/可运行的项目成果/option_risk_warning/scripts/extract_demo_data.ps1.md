---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/scripts/extract_demo_data.ps1](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/extract_demo_data.ps1>)

SHA-256：`70fe27e23e70e03e807abf1875ff8208ffd2cd7292d448400e9419028c71dc8e`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````powershell
param(
    [Parameter(Mandatory = $true)]
    [string]$ArchivePath,

    [string]$OutputDir = (Join-Path $PSScriptRoot "..\data\demo")
)

$resolvedArchive = [IO.Path]::GetFullPath($ArchivePath)
$resolvedOutput = [IO.Path]::GetFullPath($OutputDir)
if (-not (Test-Path -LiteralPath $resolvedArchive -PathType Leaf)) {
    throw "Archive not found: $resolvedArchive"
}
New-Item -ItemType Directory -Force -Path $resolvedOutput | Out-Null

$patterns = @(
    '*extreme_event.csv',
    '*archive/SF/ag*/options/2024/08/options_202408.parquet',
    '*archive/SF/ag*/options/2024/09/options_202409.parquet',
    '*archive/SF/ag*/options/2024/10/options_202410.parquet',
    '*archive/SF/ag*/options/2024/11/options_202411.parquet',
    '*archive/SF/ag*/options/2024/12/options_202412.parquet',
    '*archive/SF/ag*/options/2025/01/options_202501.parquet',
    '*archive/SF/ag*/options/2025/02/options_202502.parquet',
    '*archive/SF/ag*/options/2025/03/options_202503.parquet',
    '*archive/SF/ag*/options/2025/04/options_202504.parquet'
)

& tar -xf $resolvedArchive -C $resolvedOutput @patterns
if ($LASTEXITCODE -ne 0) {
    throw "tar extraction failed with exit code $LASTEXITCODE"
}

$files = Get-ChildItem -LiteralPath $resolvedOutput -Recurse -File -Filter *.parquet
Write-Host "Extracted $($files.Count) Parquet files to $resolvedOutput"
````

</details>
