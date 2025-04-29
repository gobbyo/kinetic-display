# Define the root path for temp directories (passed as a parameter)
param (
    [string]$TempRootPath = "../../../deploy"
)

# Delete the root temp directory if it already exists
if (Test-Path $TempRootPath) {
    Remove-Item -Recurse -Force $TempRootPath
}

# Define the paths
$conductorTempDir = Join-Path $TempRootPath "conductor"
$digitTempDir = Join-Path $TempRootPath "digit"
$conductorDir = "./conductor"
$commonDir = "./common"
$digitDir = "./digit"

# Step 1: Overwrite or create a new "conductor" temp directory
if (Test-Path $conductorTempDir) {
    Remove-Item -Recurse -Force $conductorTempDir
}
New-Item -ItemType Directory -Path $conductorTempDir

# Step 2: Copy all files from "conductor" directory to "conductor" temp directory
Copy-Item -Path "$conductorDir\*" -Destination $conductorTempDir -Recurse

# Step 3: Rename uart_command.py to main.py in the "conductor" temp directory
$uartCommandPath = Join-Path $conductorTempDir "uart_command.py"
$mainPath = Join-Path $conductorTempDir "main.py"
if (Test-Path $uartCommandPath) {
    Rename-Item -Path $uartCommandPath -NewName "main.py"
}

# Step 4: Copy the "common" directory to the "conductor" temp directory
Copy-Item -Path $commonDir -Destination $conductorTempDir -Recurse

# Step 5: Create a "secrets.py" file in the "conductor" temp directory with the specified contents
$secretsFilePath = Join-Path $conductorTempDir "secrets.py"
$secretsContent = @'
usr="ssid-name"
pwd="wifi-password"
'@
Set-Content -Path $secretsFilePath -Value $secretsContent

# Step 6: Overwrite or create a new "digit" temp directory
if (Test-Path $digitTempDir) {
    Remove-Item -Recurse -Force $digitTempDir
}
New-Item -ItemType Directory -Path $digitTempDir

# Step 7: Copy the "digit" folder and paste it under the "digit" temp directory
Copy-Item -Path "$digitDir\*" -Destination $digitTempDir -Recurse

# Step 8: Rename uart_digit.py to main.py in the new "digit" folder
$uartDigitPath = Join-Path $digitTempDir "uart_digit.py"
$digitMainPath = Join-Path $digitTempDir "main.py"
if (Test-Path $uartDigitPath) {
    Rename-Item -Path $uartDigitPath -NewName "main.py"
}

# Step 9: Copy the "common" directory to the new "digit" folder
Copy-Item -Path $commonDir -Destination $digitTempDir -Recurse