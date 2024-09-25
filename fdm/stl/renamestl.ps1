# Define the directory path
$directoryPath = "C:\repos\kinetic-display\fdm\stl"

# Get all files in the directory
$files = Get-ChildItem -Path $directoryPath -File

# Loop through each file
foreach ($file in $files) {
    # Check if the file name contains "7-segment-"
    if ($file.Name -like "7-segment-digit3-*") {
        # Remove "7-segment-" from the file name
        $newName = $file.Name -replace "7-segment-digit3-", ""
        
        # Rename the file
        Rename-Item -Path $file.FullName -NewName $newName
    }
}

Write-Host "File names have been updated."
