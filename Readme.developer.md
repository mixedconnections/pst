# pst Developer Readme

## Incremental

Change the version:

`python -m incremental.update <projectname> --newversion=<version>`

## Using Pyinstaller

I've worked on a problem with PyInstaller and the fix for my issue was to remove the `__init__.py` file from my tree, 
so I don't have that file anymore and everything works as expected. However, now I had to modify sys.path in pst.py inorder to access
_version.py from incremental.

Therefore, PyInstaller required the --paths argument while building the application. (The manual states that specifying the -p argument 
is equivalent.)

`pyinstaller --paths=/path/to/pst --onefile pst.py --name pst`

## PyPi

`python setup.py sdist`

`twine check dist/*`

`twine upload dist/*`
