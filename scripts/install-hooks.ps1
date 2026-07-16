<#
Installs the ea-code-validator pre-commit hook into .git/hooks/pre-commit.

Idempotent: if the hook already exists and was written by this installer
(recognised by a marker line), it is overwritten.  If it exists but was
written by someone/something else, the installer refuses and prints the
intended contents so the user can merge manually.
#>

$ErrorActionPreference = 'Stop'

$repoRoot = (git rev-parse --show-toplevel 2>$null)
if (-not $repoRoot) { throw "Not inside a git repository." }

$hookPath = Join-Path $repoRoot '.git/hooks/pre-commit'
$marker   = '# ea-code-validator hook -- managed by scripts/install-hooks'
$body = @"
#!/usr/bin/env sh
$marker
python .opencode/skills/ea-code-validator/cli.py --changed
"@

if (Test-Path $hookPath) {
    $existing = Get-Content $hookPath -Raw
    if ($existing -notmatch [regex]::Escape($marker)) {
        Write-Host "Refusing to overwrite existing $hookPath (not managed by this installer)."
        Write-Host ""
        Write-Host "Intended contents:"
        Write-Host $body
        exit 1
    }
}

# Write with LF line endings so Git for Windows' bundled sh can run it.
[IO.File]::WriteAllText($hookPath, ($body -replace "`r`n", "`n"))
Write-Host "Installed pre-commit hook at $hookPath"
