[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = $ScriptDir
$AgentsDir = Join-Path $ProjectDir ".claude\agents"
$SettingsDir = Join-Path $ProjectDir ".claude"

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  종목분석 에이전트 설치" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  프로젝트: $ProjectDir" -ForegroundColor Gray
Write-Host ""

# 1. 폴더 생성
Write-Host "[1/3] .claude\agents 폴더 생성..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $AgentsDir | Out-Null
Write-Host "       OK" -ForegroundColor Green

# 2. 에이전트 파일 복사
Write-Host "[2/3] 에이전트 파일 복사..." -ForegroundColor Yellow
$agents = @(
    "stock-analyst-lead.md",
    "data-collector.md",
    "company-overview.md",
    "financial-analyst.md",
    "business-analyst.md",
    "momentum-analyst.md",
    "risk-analyst.md",
    "scorecard-strategist.md",
    "report-generator.md"
)

$copied = 0
$skipped = 0
foreach ($agent in $agents) {
    $src = Join-Path $ProjectDir $agent
    if (Test-Path $src) {
        Copy-Item $src -Destination $AgentsDir -Force
        Write-Host "       OK  $agent" -ForegroundColor Green
        $copied++
    } else {
        Write-Host "       SKIP  $agent (파일 없음)" -ForegroundColor Red
        $skipped++
    }
}
Write-Host "       복사: ${copied}개 / 스킵: ${skipped}개" -ForegroundColor Gray

# 3. settings.json 생성
Write-Host "[3/3] settings.json 생성..." -ForegroundColor Yellow
$settingsPath = Join-Path $SettingsDir "settings.json"

$settingsContent = @'
{
  "env": {
    "DART_API_KEY": "baa4729e8499b32f8467814d0742de664a8eb47c"
  }
}
'@

Set-Content -Path $settingsPath -Value $settingsContent -Encoding UTF8
Write-Host "       OK  $settingsPath" -ForegroundColor Green

# 완료
Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  설치 완료!" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  다음 단계:" -ForegroundColor White
Write-Host "  1. 이 폴더에서 Claude Code 실행" -ForegroundColor Gray
Write-Host "     cd ""$ProjectDir""" -ForegroundColor Yellow
Write-Host "     claude" -ForegroundColor Yellow
Write-Host ""
Write-Host "  2. 에이전트 확인" -ForegroundColor Gray
Write-Host "     /agents" -ForegroundColor Yellow
Write-Host ""
Write-Host "  3. 테스트" -ForegroundColor Gray
Write-Host "     삼성전자 종목 분석해줘" -ForegroundColor Yellow
Write-Host ""
