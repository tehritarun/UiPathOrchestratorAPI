$envfilename=".testenv"
$instance = Read-Host -Prompt "Enter instance name: "
$tenant = Read-Host -Prompt "Enter tanent name: "
$client_id = Read-Host -Prompt "Enter client-id: "
$client_secret = Read-Host -Prompt "Enter client secret: "


Add-Content $envfilename INSTANCE_NAME="$instance"
Add-Content $envfilename TANENT="$tenant"
Add-Content $envfilename CLIENT_ID="$client_id"
Add-Content $envfilename USER_KEY="$client_secret"

python -m venv venv
pip install -r .\requirements.txt
.\venv\Scripts\Activate.ps1
