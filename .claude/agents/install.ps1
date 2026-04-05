[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = $ScriptDir
$AgentsDir = Join-Path $ProjectDir ".claude\agents"
$CommandsDir = Join-Path $ProjectDir ".claude\commands"
$SettingsDir = Join-Path $ProjectDir ".claude"

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  종목분석 에이전트 v2.2 설치" -ForegroundColor Cyan
Write-Host "  (개별종목 + ETF 지원)" -ForegroundColor Gray
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  프로젝트: $ProjectDir" -ForegroundColor Gray
Write-Host ""

Write-Host "[1/4] 폴더 생성..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $AgentsDir | Out-Null
New-Item -ItemType Directory -Force -Path $CommandsDir | Out-Null
Write-Host "       OK" -ForegroundColor Green

Write-Host "[2/4] 에이전트 파일 복사..." -ForegroundColor Yellow
$agents = @("stock-analyst-lead.md","data-collector.md","company-overview.md","financial-analyst.md","business-analyst.md","momentum-analyst.md","risk-analyst.md","scorecard-strategist.md","etf-analyst.md","report-generator.md","stop-loss-rules.md")
$c = 0
foreach ($a in $agents) {
    $s = Join-Path $ProjectDir $a
    if (Test-Path $s) { Copy-Item $s -Destination $AgentsDir -Force; Write-Host "       OK  $a" -ForegroundColor Green; $c++ }
    else { Write-Host "       SKIP  $a" -ForegroundColor Red }
}
Write-Host "       에이전트: ${c}개" -ForegroundColor Gray

Write-Host "[3/4] 슬래시 명령어 복사..." -ForegroundColor Yellow
$cc = 0
Get-ChildItem -Path $ProjectDir -Filter "*.md" | Where-Object {
    $_.Name -match "^(종목분석|비교분석|빠른분석|손절계산|리포트)\.md$"
} | ForEach-Object {
    Copy-Item $_.FullName -Destination $CommandsDir -Force
    Write-Host "       OK  /$($_.BaseName)" -ForegroundColor Green
    $cc++
}
Write-Host "       명령어: ${cc}개" -ForegroundColor Gray

Write-Host "[4/4] settings.json..." -ForegroundColor Yellow
$sp = Join-Path $SettingsDir "settings.json"
$sc = @'
{
  "env": {
    "DART_API_KEY": "baa4729e8499b32f8467814d0742de664a8eb47c"
  }
}
'@
Set-Content -Path $sp -Value $sc -Encoding UTF8
Write-Host "       OK" -ForegroundColor Green

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  설치 완료! (v2.2)" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  사용법:" -ForegroundColor White
Write-Host "    /종목분석 삼성전자       (개별 종목)" -ForegroundColor Yellow
Write-Host "    /종목분석 XLE            (ETF)" -ForegroundColor Yellow
Write-Host "    /종목분석 KODEX 200      (ETF)" -ForegroundColor Yellow
Write-Host "    /비교분석 SPY QQQ        (ETF 비교)" -ForegroundColor Yellow
Write-Host "    /빠른분석 네이버         (빠른 요약)" -ForegroundColor Yellow
Write-Host "    /손절계산 삼성전자 80000 (손절/목표)" -ForegroundColor Yellow
Write-Host ""
