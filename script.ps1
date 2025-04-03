# Requires elevated privileges (Run as Administrator)

# Admin rights required
try {
	# Install File
	if ($installCommand) {
	$installCommand = "dfdf"
	Start-Process -filePath "$localPath" -argumentList "$installCommand" -wait "True" -verb "RunAs"
	Write-Host "Installation successful."
	if ($LASTEXITCODE -ne 0) {
	Write-Warning "Installation failed. with exit code: $LASTEXITCODE"
	}
	}
	
}
catch {
	Write-Error 'An error occurred: $_'
}
finally {
	Remove-Item $localPath -Force 
}

# Requires elevated privileges (Run as Administrator)

try {
	# Download File
	$url = "dfdf"
	$localPath = "sdf"
	Invoke-WebRequest -uri "$url" -outFile "$localPath"
	Write-Host "File downloaded successfully."
	Write-Error "Error during file download."
	
}
catch {
	Write-Error 'An error occurred: $_'
}
finally {
	Remove-Item $localPath -Force 
}

