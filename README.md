# LES

A simulation tool for comparing schedulable load algorithms and twinworlds in a local energy system environment.

## Requirements

- Any moderately modern version of Node and NPM
- Python 3.11+

On windows, in order to get all the packages for the backend to compile, you also have to install
[Microsoft build tools](https://visualstudio.microsoft.com/downloads/?q=build+tools) and select the build tools option in the Visual Studio installer.

## Installation

### Backend

First create a virtual environment and activate it. In order to do that, make sure you're in the `backend` directory with your terminal of choice.

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
pip install -r requirements.txt && pip install -r requirements.dev.txt
```

### Frontend

`cd` to the frontend folder, and run `npm i`.

## Development

### Backend

To run the backend server, make sure you have the virtual environment activated (see installation).
Then `cd` into the backend folder, and run `python run.py` for a dev server, and navigate to `http://localhost:8000/`.

When `development mode` is enabled, you can go to `http://localhost:8000/docs` to find the API documentation.

**IMPORTANT:** To have any data to start with, call the `seed` API route to generate intial data for your database.

#### Linters

The linters installed with the project are: `black`, `mypy`, and `flake8`. They are run on each pull request with a CI workflow, but to manually run them on your machine,
be sure to be in the backend directory, have the virtual environment enabled and use the commands below:

- black (for formatting your code):
`black .`

- flake8 (follow PEP8 styling):
`flake8 app/`

- mypy (fix type errors):
`mypy app/`

### Frontend

`cd` to the frontend folder, and run `npm run dev` for a dev server, and navigate to `http://localhost:5173/`. The application will automatically reload if you change any of the source files.

#### Linters

The frontend uses `svelte-check` for checking any errors for svelte, and `prettier` for formatting.

Run `npm run check` to run both to check for issues, or run `npm run format` to format the project with prettier.

## Project structure

### Backend

The backend is found in the `backend` folder. In the backend folder you can find the default setup files and dependency lists, and the `run.py` entrypoint file that you run with Python.

The `app` folder contains the rest of the application. The application is structured in the following way:

- The `core` folder:
  - This is the bulk of the app, also separated in multiple directories:
    - `crud`: This contains all CRUD operations for the specified model/router
    - `models`: Here are the database models with [SQLModel](https://sqlmodel.tiangolo.com/). Here you can also find the Response and Input classes in the same files.
    - `routers`: This folder contains all the entrypoints you can call with this API. The router folder will use the model and CRUD for the specified name.


- Everything else in `app`:
  - This contains global helpers, configuration and utilities that don't belong to a specific router, and contains the FastAPI factory in `app.py`

### Frontend

The frontend is found in the `frontend` folder. It is a [Vite](https://vitejs.dev/) project, so it is structured the same way a Vite project get's generated.

Inside the `frontend` folder are all configurations found for Tailwind, Prettier, etc. It also contains a `src` folder which holds the `Svelte` code, and a `public` folder for images, SVGs, etc.

The `src` folder has 2 subfolders:
  - `lib`: Where imported `.ts` or `.js` files, and where the output of the `openapi-typescript-codegen` library resides.
  - `components`: Where all svelte components can be found.

Inside the `src` folder is `App.svelte` which is the entrypoint that is getting loaded by `main.ts`.


## Future Work

* Online:

For this project to be more accessible, the application needs to be deployed online. Right now, it is required to run everything locally.
For instance, you can deploy the frontend to [GitHub Pages](pages.github.com/), and the backend to [Microsoft Azure](azure.microsoft.com/en-us/).

* Accounts:

If the application has been deployed online, it must be secured. User accounts must exist that secure the application and prevent researchers from removing other researchers' algorithms.

* Stock market:

An alternative cost model that works by buying and selling of energy directly to other users can be added to the application.
Users can provide a price and a quantity for how much energy they want to buy or sell, which will get matched to other offers.

* Improve stepper User Experience (UX):

The User Experience of the stepper can be improved. When a researcher creates a large twin world the user interface can become cluttered and complex.
It will be required to scroll around a lot to navigate through the user interface, which makes it counterintuitive.

* (Optional) i18n:

If desired, the application can be internationalised by translating it to different languages.
