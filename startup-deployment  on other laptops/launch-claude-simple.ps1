# Simple PowerShell script to launch Claude Code
# Add npm to PATH and launch Claude

# Set location to home directory
Set-Location ~

# Add npm to PATH for this session
$npmPath = "$env:APPDATA\npm"
$env:PATH = "$npmPath;$env:PATH"

# Now just run claude (it's in PATH now)
claude
