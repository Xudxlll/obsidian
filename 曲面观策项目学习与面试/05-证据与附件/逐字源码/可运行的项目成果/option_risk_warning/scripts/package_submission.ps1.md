---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/scripts/package_submission.ps1](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/package_submission.ps1>)

SHA-256：`506593dad72b0d25f08f9f9e553f87c804a7e086abccc81927d0ad0b8c7f3f22`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````powershell
param(
    [string]$OutputPath = (Join-Path $PSScriptRoot "..\option_risk_warning_submission.zip"),
    [switch]$ManifestOnly,
    [string]$AuditDataDir = (Join-Path $PSScriptRoot "..\data\demo"),
    [string]$AuditProduct = "ag",
    [string]$AuditTimestamp = "2025-04-07 10:15:00",
    [string]$PythonExecutable = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)

$ProjectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$ResolvedOutput = [IO.Path]::GetFullPath($OutputPath)
# Explicit allowlist: no directory is copied wholesale.
$AllowedFiles = @(
    ".gitignore",
    "pyproject.toml",
    "README.md",
    "src/option_risk/__init__.py",
    "src/option_risk/__main__.py",
    "src/option_risk/agent.py",
    "src/option_risk/alerts.py",
    "src/option_risk/backtest.py",
    "src/option_risk/catalog.py",
    "src/option_risk/cli.py",
    "src/option_risk/config.py",
    "src/option_risk/contracts.py",
    "src/option_risk/dashboard.py",
    "src/option_risk/decision.py",
    "src/option_risk/errors.py",
    "src/option_risk/features.py",
    "src/option_risk/graph_explanation.py",
    "src/option_risk/graph_queries.py",
    "src/option_risk/graph_reasoner.py",
    "src/option_risk/graph_visualization.py",
    "src/option_risk/interactive.py",
    "src/option_risk/io.py",
    "src/option_risk/knowledge_graph.py",
    "src/option_risk/knowledge_schema.py",
    "src/option_risk/labels.py",
    "src/option_risk/model.py",
    "src/option_risk/official_events.py",
    "src/option_risk/pipeline.py",
    "src/option_risk/provenance.py",
    "src/option_risk/quality.py",
    "src/option_risk/surfaces.py",
    "src/option_risk/surface_fit_diagnostics.py",
    "src/option_risk/total_variance_fit.py",
    "src/option_risk/validation.py",
    "src/option_risk/visualization.py",
    "scripts/build_acceptance_report.py",
    "scripts/build_explanation_review.py",
    "scripts/build_knowledge_graph_notebook.py",
    "scripts/build_knowledge_graph_report.py",
    "scripts/build_notebook.py",
    "scripts/extract_demo_data.ps1",
    "scripts/package_submission.ps1",
    "scripts/query_knowledge_graph.py",
    "scripts/render_acceptance_html.py",
    "scripts/validate_knowledge_graph.py",
    "scripts/validate_outputs.py",
    "docs/问题1-离线报告图表设计.md",
    "docs/问题1-Agent图表设计.md",
    "docs/问题2-知识图谱设计与运行说明.md",
    "notebooks/02_knowledge_graph_demo.ipynb",
    "queries/acceptance_report.sql",
    "queries/backtest_report.sql",
    "outputs/问题1-Agent离线验收报告.artifact.json",
    "outputs/问题1-Agent离线验收报告.html",
    "outputs/agent_acceptance_full.json",
    "outputs/demo/run_summary.json",
    "outputs/demo/validation_report.json",
    "outputs/knowledge_graph_acceptance_full.json",
    "outputs/demo/knowledge_graph_snapshot.json",
    "outputs/人工解释评分模板.csv",
    "outputs/问题2-知识图谱验收报告.html",
    "tests/graph_fixtures.py",
    "tests/test_agent_contracts.py",
    "tests/test_graph_acceptance.py",
    "tests/test_graph_artifacts.py",
    "tests/test_graph_dashboard.py",
    "tests/test_graph_explanation.py",
    "tests/test_graph_queries.py",
    "tests/test_graph_reasoner.py",
    "tests/test_knowledge_graph.py",
    "tests/test_knowledge_schema.py",
    "tests/test_total_variance_fit.py",
    "tests/test_validation.py"
)

function Assert-FormalGates {
    $ProblemOnePath = Join-Path $ProjectRoot "outputs\demo\validation_report.json"
    if (-not (Test-Path -LiteralPath $ProblemOnePath -PathType Leaf)) {
        throw "Missing Problem 1 validation gate: $ProblemOnePath"
    }
    $ProblemOne = Get-Content -LiteralPath $ProblemOnePath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($ProblemOne.all_boolean_checks_pass -ne $true) {
        throw "Problem 1 validation gate is not fully green"
    }

    $AgentPath = Join-Path $ProjectRoot "outputs\agent_acceptance_full.json"
    if (-not (Test-Path -LiteralPath $AgentPath -PathType Leaf)) {
        throw "Missing current combined Agent acceptance: $AgentPath"
    }
    $Agent = Get-Content -LiteralPath $AgentPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $AgentProducts = @($Agent.products)
    $AgentPassed = @($AgentProducts | Where-Object { $_.status -eq "passed" }).Count
    if (
        $AgentProducts.Count -ne 35 -or
        $AgentPassed -ne 35 -or
        $Agent.summary.status -ne "passed" -or
        $Agent.summary.product_count -ne 35 -or
        $Agent.summary.passed_products -ne 35 -or
        $Agent.summary.failed_products -ne 0
    ) {
        throw "Current combined Agent acceptance summary does not reconcile"
    }

    $GraphPath = Join-Path $ProjectRoot "outputs\knowledge_graph_acceptance_full.json"
    if (-not (Test-Path -LiteralPath $GraphPath -PathType Leaf)) {
        throw "Missing Problem 2 formal acceptance: $GraphPath"
    }
    $Graph = Get-Content -LiteralPath $GraphPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $Products = @($Graph.products)
    $Passed = @($Products | Where-Object { $_.status -eq "passed" }).Count
    $Failed = $Products.Count - $Passed
    if (
        $Products.Count -ne 35 -or
        $Passed -ne 35 -or
        $Failed -ne 0 -or
        $Graph.summary.status -ne "passed" -or
        $Graph.summary.product_count -ne $Products.Count -or
        $Graph.summary.passed_products -ne $Passed -or
        $Graph.summary.failed_products -ne $Failed
    ) {
        throw "Problem 2 formal acceptance summary does not reconcile"
    }
    $RequiredChecks = @("deterministic", "no_future", "content_safety")
    $ActualChecks = @($Graph.global_checks.PSObject.Properties.Name | Sort-Object)
    if (@(Compare-Object ($RequiredChecks | Sort-Object) $ActualChecks).Count -ne 0) {
        throw "Problem 2 formal acceptance global checks are incomplete"
    }
    foreach ($Name in $RequiredChecks) {
        $Check = $Graph.global_checks.$Name
        if ($Check.passed -ne $true -or [int]$Check.checked_count -le 0 -or [string]::IsNullOrWhiteSpace([string]$Check.scope)) {
            throw "Problem 2 global check is not executed/passing: $Name"
        }
    }
    foreach ($Row in $Products) {
        if (
            $Row.knowledge_graph.status -ne "ready" -or
            $Row.knowledge_graph.schema_version -ne "kg-schema-v1" -or
            $Row.knowledge_graph.rule_version -ne "kg-rule-v1"
        ) {
            throw "Problem 2 product row is not current/ready: $($Row.product)"
        }
    }
}

function Assert-AllowlistSources {
    $Duplicates = @($AllowedFiles | Group-Object | Where-Object Count -gt 1)
    if ($Duplicates.Count -ne 0) {
        throw "Package allowlist contains duplicate paths"
    }
    foreach ($Relative in $AllowedFiles) {
        if ($Relative.Contains("\") -or $Relative.StartsWith("/") -or $Relative.Contains("../")) {
            throw "Allowlist path is not canonical relative POSIX form: $Relative"
        }
        $Source = Join-Path $ProjectRoot ($Relative.Replace("/", [IO.Path]::DirectorySeparatorChar))
        if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) {
            throw "Missing allowlisted file: $Relative"
        }
        $Item = Get-Item -LiteralPath $Source -Force
        if (($Item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
            throw "Allowlisted file may not be a symlink/reparse point: $Relative"
        }
    }
}

function Assert-PortableFiles {
    param(
        [string]$Root,
        [string[]]$RelativeFiles
    )
    $AbsolutePathPattern = '(?:[A-Z]:[\/]|/Us' + 'ers/[A-Za-z0-9._-]+/|/ho' + 'me/[A-Za-z0-9._-]+/)'
    $ForbiddenParts = @("data", ".venv", "__pycache__", ".pytest_cache", ".superpowers", ".git")
    $ForbiddenExtensions = @(".rar", ".zip", ".parquet", ".pyc", ".pyo")
    $TextExtensions = @("", ".py", ".ps1", ".md", ".toml", ".json", ".html", ".csv", ".sql", ".ipynb")
    foreach ($Relative in $RelativeFiles) {
        $Parts = @($Relative -split "/")
        if (@($Parts | Where-Object { $_ -in $ForbiddenParts }).Count -ne 0) {
            throw "Forbidden directory in package manifest: $Relative"
        }
        if ($Relative.Contains(".egg-info/") -or ([IO.Path]::GetExtension($Relative).ToLowerInvariant() -in $ForbiddenExtensions)) {
            throw "Raw data/cache/archive/bytecode is forbidden: $Relative"
        }
        $Path = Join-Path $Root ($Relative.Replace("/", [IO.Path]::DirectorySeparatorChar))
        $Extension = [IO.Path]::GetExtension($Path).ToLowerInvariant()
        if ($Extension -in $TextExtensions -or [IO.Path]::GetFileName($Path) -eq ".gitignore") {
            $Text = [IO.File]::ReadAllText($Path, [Text.Encoding]::UTF8)
            if ([Text.RegularExpressions.Regex]::IsMatch($Text, $AbsolutePathPattern)) {
                throw "Absolute machine path found in allowlisted content: $Relative"
            }
        }
    }
}

function Assert-StagedManifest {
    param([string]$PackageRoot)
    $Actual = @(
        Get-ChildItem -LiteralPath $PackageRoot -Recurse -File -Force |
            ForEach-Object { [IO.Path]::GetRelativePath($PackageRoot, $_.FullName).Replace("\", "/") } |
            Sort-Object
    )
    $Expected = @($AllowedFiles | Sort-Object)
    $Difference = @(Compare-Object $Expected $Actual)
    if ($Difference.Count -ne 0) {
        throw "Staged package differs from explicit allowlist: $($Difference | Out-String)"
    }
    Assert-PortableFiles -Root $PackageRoot -RelativeFiles $Actual
}

Assert-FormalGates
Assert-AllowlistSources
Assert-PortableFiles -Root $ProjectRoot -RelativeFiles $AllowedFiles

$Manifest = [ordered]@{
    format_version = "submission-manifest-v1"
    root_name = "option_risk_warning"
    file_count = $AllowedFiles.Count
    files = @($AllowedFiles)
    audit = [ordered]@{
        explicit_allowlist = $true
        formal_problem1_gate_passed = $true
        formal_problem2_gate_passed = $true
        absolute_path_scan_passed = $true
        raw_data_scan_passed = $true
        incomplete_rating_summary_included = $false
    }
}

if ($ManifestOnly) {
    $Manifest | ConvertTo-Json -Depth 6 -Compress
    exit 0
}

$OutputParent = Split-Path -Parent $ResolvedOutput
New-Item -ItemType Directory -Path $OutputParent -Force | Out-Null
$TemporaryZip = Join-Path $OutputParent ("." + [IO.Path]::GetFileName($ResolvedOutput) + "." + [guid]::NewGuid().ToString("N") + ".tmp.zip")
$StagingRoot = Join-Path ([IO.Path]::GetTempPath()) ("option-risk-submission-" + [guid]::NewGuid().ToString("N"))
$PackageRoot = Join-Path $StagingRoot "option_risk_warning"
$ExtractRoot = Join-Path $StagingRoot "extracted-audit"
$VenvRoot = Join-Path $StagingRoot "clean-install-venv"
$Succeeded = $false

try {
    New-Item -ItemType Directory -Path $PackageRoot -Force | Out-Null
    foreach ($Relative in $AllowedFiles) {
        $Source = Join-Path $ProjectRoot ($Relative.Replace("/", [IO.Path]::DirectorySeparatorChar))
        $Destination = Join-Path $PackageRoot ($Relative.Replace("/", [IO.Path]::DirectorySeparatorChar))
        New-Item -ItemType Directory -Path (Split-Path -Parent $Destination) -Force | Out-Null
        Copy-Item -LiteralPath $Source -Destination $Destination
    }
    Assert-StagedManifest -PackageRoot $PackageRoot

    Compress-Archive -LiteralPath $PackageRoot -DestinationPath $TemporaryZip -CompressionLevel Optimal
    New-Item -ItemType Directory -Path $ExtractRoot -Force | Out-Null
    Expand-Archive -LiteralPath $TemporaryZip -DestinationPath $ExtractRoot
    $ExtractedPackage = Join-Path $ExtractRoot "option_risk_warning"
    Assert-StagedManifest -PackageRoot $ExtractedPackage

    $ResolvedAuditData = [IO.Path]::GetFullPath($AuditDataDir)
    if (-not (Test-Path -LiteralPath $ResolvedAuditData -PathType Container)) {
        throw "ZIP-external audit data directory does not exist: $ResolvedAuditData"
    }
    if ([string]::IsNullOrWhiteSpace($PythonExecutable)) {
        $LocalPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
        $PythonExecutable = if (Test-Path -LiteralPath $LocalPython -PathType Leaf) { $LocalPython } else { "python" }
    }
    $VenvLog = (& $PythonExecutable -m venv $VenvRoot 2>&1 | Out-String)
    if ($LASTEXITCODE -ne 0) {
        throw "Fresh virtual environment creation failed: $VenvLog"
    }
    $AuditPython = Join-Path $VenvRoot "Scripts\python.exe"
    if (-not (Test-Path -LiteralPath $AuditPython -PathType Leaf)) {
        $AuditPython = Join-Path $VenvRoot "bin\python"
    }
    if (-not (Test-Path -LiteralPath $AuditPython -PathType Leaf)) {
        throw "Fresh virtual environment has no Python executable"
    }
    $InstallLog = (& $AuditPython -m pip install --disable-pip-version-check $ExtractedPackage 2>&1 | Out-String)
    if ($LASTEXITCODE -ne 0) {
        throw "Clean package installation failed: $InstallLog"
    }
    $AuditCache = Join-Path $StagingRoot "query-cache"
    $AuditOutput = Join-Path $StagingRoot "query-output"
    $QueryScript = Join-Path $ExtractedPackage "scripts\query_knowledge_graph.py"
    $QueryText = (& $AuditPython $QueryScript --data-dir $ResolvedAuditData --cache-dir $AuditCache --output-dir $AuditOutput --product $AuditProduct --timestamp $AuditTimestamp --query root-evidence 2>&1 | Out-String)
    if ($LASTEXITCODE -ne 0) {
        throw "Clean-install real graph query failed: $QueryText"
    }
    try {
        $QueryResult = $QueryText | ConvertFrom-Json
    }
    catch {
        throw "Clean-install graph query did not emit strict JSON: $QueryText"
    }
    if ($QueryResult.product -ne $AuditProduct -or $QueryResult.query -ne "root-evidence" -or [int]$QueryResult.record_count -lt 1) {
        throw "Clean-install graph query result does not reconcile"
    }

    $ZipItem = Get-Item -LiteralPath $TemporaryZip
    $ZipSha256 = (Get-FileHash -LiteralPath $TemporaryZip -Algorithm SHA256).Hash
    [IO.File]::Move($TemporaryZip, $ResolvedOutput, $true)
    $Succeeded = $true

    Write-Output "Created: $ResolvedOutput"
    Write-Output "Files: $($AllowedFiles.Count)"
    Write-Output "Bytes: $($ZipItem.Length)"
    Write-Output "SHA256: $ZipSha256"
    Write-Output "Audit: extracted manifest clean; fresh venv install passed; external-data real root-evidence query passed"
    Write-Output "Commands: python -m venv; python -m pip install <extracted-package>; query_knowledge_graph.py --query root-evidence"
}
finally {
    $ResolvedStaging = [IO.Path]::GetFullPath($StagingRoot)
    $ResolvedTemp = [IO.Path]::GetFullPath([IO.Path]::GetTempPath())
    if (
        (Test-Path -LiteralPath $ResolvedStaging) -and
        $ResolvedStaging.StartsWith($ResolvedTemp, [StringComparison]::OrdinalIgnoreCase) -and
        $ResolvedStaging -ne $ResolvedTemp
    ) {
        Remove-Item -LiteralPath $ResolvedStaging -Recurse -Force
    }
    if (-not $Succeeded -and (Test-Path -LiteralPath $TemporaryZip -PathType Leaf)) {
        $ResolvedTemporaryZip = [IO.Path]::GetFullPath($TemporaryZip)
        if (
            [IO.Path]::GetDirectoryName($ResolvedTemporaryZip) -eq [IO.Path]::GetFullPath($OutputParent) -and
            [IO.Path]::GetFileName($ResolvedTemporaryZip).StartsWith("." + [IO.Path]::GetFileName($ResolvedOutput) + ".")
        ) {
            [IO.File]::Delete($ResolvedTemporaryZip)
        }
    }
}
````

</details>
