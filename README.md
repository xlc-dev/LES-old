# LES

## Requirements

- Node 21.0+ and npm
- Python 3.11

## Installation

### Backend

First create a virtual environment and activate it. Make sure you're in the root of the repository.

On Linux/Mac:
```sh
python -m venv venv
source venv/bin/activate
```

On Windows:
```sh
py -m venv venv
.\venv\Scripts\activate
```

Then, install deps:
```sh
pip install pip-tools && pip install -r requirements.txt && pip install -r requirements.dev.txt
pip-sync requirements.txt requirements.dev.txt
```

### Frontend

`cd` to the frontend folder, and run `npm ci`.

## Development

### Backend

To run the backend server, make sure you have the virtual environment activated (see installation).
Then `cd` into the backend folder, and run `python run.py` for a dev server, and navigate to `http://localhost:8000/`. The application will automatically reload if you change any of the source files.

### Frontend

`cd` to the frontend folder, and run `npm run start` for a dev server, and navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.
