##pyenv con venv

Prima di creare l'ambiente virtuale di python bisogna decidere quale versione di python si vuole utilizzare

Usa pyenv:
pyenv local 3.8.5

Crea un ambiente virtuale:
python -m venv myproject

Usa l'ambiente virtuale creato:
myproject\Scripts\activate

Esci dall'ambiente virtuale:
(myproject) C:\Users\Your Name> deactivate

Verifica se pyenv ha settato la versione corrente:
python -V
Oppure
python --version


Attivare il virtual environment da powershell in vscode:
PS C:\Users\path> Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
PS C:\Users\path> HFpro/Scripts/activate.ps1
(HFpro) PS C:\Users\path> 


Installare i packages richiesti:
pip install -r requirements.txt
