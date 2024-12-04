# Define the paths
$tempDir = "../../../deploy/conductor"
$conductorDir = "./conductor"
$commonDir = "./common"

# Step 1: Overwrite or create a new "temp" directory
if (Test-Path $tempDir) {
    Remove-Item -Recurse -Force $tempDir
}
New-Item -ItemType Directory -Path $tempDir

# Step 2: Copy all files from "conductor" directory to "temp" directory
Copy-Item -Path "$conductorDir\*" -Destination $tempDir -Recurse

# Step 3: Rename uart_command.py to main.py in the "temp" directory
$uartCommandPath = Join-Path $tempDir "uart_command.py"
$mainPath = Join-Path $tempDir "main.py"
if (Test-Path $uartCommandPath) {
    Rename-Item -Path $uartCommandPath -NewName "main.py"
}

# Step 4: Copy the "common" directory to the "temp" directory
Copy-Item -Path $commonDir -Destination $tempDir -Recurse

# Step 5: Create a "secrets.py" file in the "tempDir" with the specified contents
$secretsFilePath = Join-Path $tempDir "secrets.py"
$secretsContent = @'
usr="ssid-name"
pwd="wifi-password"
'@
Set-Content -Path $secretsFilePath -Value $secretsContent