Set-ExecutionPolicy Bypass -Scope Process -Force; iwr https://community.chocolatey.org/install.ps1 -UseBasicParsing | iex
refreshenv
choco install -y python
refreshenv
pip install pytest
pytest
