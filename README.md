
This is the python source code of basic business software.
You can do whathever You want with that, modify and changing everything.
To run the app from Python, run the script main.py, while keeping all the others files .py in the same folder

I suggest You to do the following steps (but there are many other ways) from your cmd prompt terminal:
1 - using pyenv set the python version to 3.8.5:  pyenv local 3.8.5
2 - check if the version is the correct one:      python --version
3 - create the virtual environment:               python -m venv myprojectname
4 - activate the venv:                            myprojectname\Scripts\activate

If you're using windows and powershell in vscode (but for me is easier to use cmd prompt), step 4 should be like:
PS C:\Users\path> Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
PS C:\Users\path> myprojectname/Scripts/activate.ps1

5 - now you're in the correct environment, You can install the dependencies: 
pip install -r requirements.txt


Once you have changed the code, to export an .exe file You need to 
1 - install the pyinstaller package
2 - open the cmd prompt, and set the current directory of this folder in your system with cd
3 - in the prompt give the command: 

3.a- If You don't want to set an icon:
pyinstaller main.py --onefile --windowed

3.b- If you want an icon for the executable (you need an image .ico in the same folder):
pyinstaller --onefile --windowed --icon=cuteburger.ico main.py

Then, if everything goes well, after some minutes (can be many) You should find the exe 
in the dist folder (a folder that will be generated automatically) 
:)

Just for your knowledge, if you want to see all the packages and their versions 
you have used in your project, just type inside you terminal: pip freeze
