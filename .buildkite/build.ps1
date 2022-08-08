Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
$Env:PATH += ";C:\ProgramData\chocolatey\bin"
choco install -y python3 --version=3.9.6 --allow-downgrade --force
$Env:PATH += ";C:\Python39\bin;C:\Python39\scripts"
pip install -r requirements.txt
pip install --editable .
pytest
