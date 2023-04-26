$env = 'robot'

conda create --name $env
conda activate $env
conda install pip
pip install -r '.\client\requirements-robot.txt'

Write-Output 'successfully installed the requirements navigate to the client folder...'