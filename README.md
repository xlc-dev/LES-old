# LES

# README

## Netherlands
[Switch to nl](#nederlands)


## Requirements

- Any moderately modern version of Node and NPM
- Python 3.11+

On windows, in order to get all the packages for the backend to compile, you also have to install
[Microsoft build tools](https://visualstudio.microsoft.com/downloads/?q=build+tools) and select the build tools option in the Visual Studio installer.

## Installation

### Backend

First create a virtual environment and activate it. Make sure you're in the root of the repository.

On Linux/Mac:
```sh
python -m venv venv
source venv/bin/activate
```

On Windows in Git Bash:
```sh
py -m venv venv
source venv/Scripts/activate
```

Or on Powershell/Command Prompt:
```sh
py -m venv venv
.\venv\Scripts\activate
```

Then, install the dependencies:
```sh
pip install pip-tools && pip install -r requirements.txt && pip install -r requirements.dev.txt
```

### Frontend

`cd` to the frontend folder, and run `npm i --legacy-peer-deps`.

The `--legacy-peer-deps` is a workaround to get `svelte-chartjs` working with the latest version of `svelte`.

## Development

### Backend

To run the backend server, make sure you have the virtual environment activated (see installation).
Then `cd` into the backend folder, and run `python run.py` for a dev server, and navigate to `http://localhost:8000/`.

### Frontend

`cd` to the frontend folder, and run `npm run dev` for a dev server, and navigate to `http://localhost:5173/`. The application will automatically reload if you change any of the source files.
