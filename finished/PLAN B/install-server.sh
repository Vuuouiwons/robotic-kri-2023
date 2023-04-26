$env = 'server'

conda create --name $env
conda activate $env
conda install pip
pip install -r '.\server\requirements.txt'

Write-Output 'successfully installed the requirements navigate to the server folder...'