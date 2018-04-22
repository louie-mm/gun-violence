Before:
Install homebrew for Mac
Add line `source ~/Documents/gun-violence/.gun_violence_bashrc` to your .bashrc or .bash_profile

Backend:
Install python3 `brew install python3`
Install most recent pip: `pip install --update pip`
Install virtualenv: `python3 -m pip install virtualenv` for Mac
`python3 -m virtualenv venv` in project root dir
install pip libs based on pip-requirements.txt (this seems to suck sometimes so just install certifi, flask, googlemaps, pymongo, and any others that are missing after that)
Install mangodb using `brew install mongodb` and install dependencies if indicated
Download mongo dump containing document bson files (dump/)
Load data into mongoDB using `mongorestore dump/`

Frontend:
run `brew isntall npm`
go to frontend home dir ($PROJECT_HOME/web-src) and run `npm install` (This will install from package-lock.json)

Maps:
Run `npm install mapshaper`
Example command using mapshaper: `mapshaper USA_adm1.shp -simplify 0.01% -o format=topojson`
