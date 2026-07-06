$inputJson = [Console]::In.ReadToEnd() | ConvertFrom-Json

$model = $inputJson.model.display_name
$cwd = $inputJson.workspace.current_dir
if (-not $cwd) { $cwd = $inputJson.cwd }
$dir = Split-Path $cwd -Leaf

$segments = @($model, $dir)

try {
    $branch = git -C $cwd branch --show-current 2>$null
    if ($LASTEXITCODE -eq 0 -and $branch) {
        $status = git -C $cwd status --porcelain 2>$null
        if ($status) { $segments += "$branch*" } else { $segments += $branch }
    }
} catch {}

$pct = $inputJson.context_window.used_percentage
if ($null -ne $pct) {
    $segments += "ctx $([math]::Round($pct))%"
}

$cost = $inputJson.cost.total_cost_usd
$durationMs = $inputJson.cost.total_duration_ms
if ($null -ne $cost -and $null -ne $durationMs) {
    $totalSec = [math]::Floor($durationMs / 1000)
    $mins = [math]::Floor($totalSec / 60)
    $secs = $totalSec % 60
    $costStr = '$' + $cost.ToString('N2', [System.Globalization.CultureInfo]::InvariantCulture)
    $segments += "$costStr | $($mins)m$($secs.ToString('00'))s"
}

Write-Host ($segments -join "  |  ")
