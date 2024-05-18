# Aiter Project README

Welcome to the Aiter Project! This README will guide you through the steps to set up and run the project. Please follow the instructions carefully.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:
- [git](https://git-scm.com/)
- [pyenv](https://github.com/pyenv/pyenv)
- [pipenv](https://pipenv.pypa.io/en/latest/)

## Setup Instructions

### 1. Clone the Repository

First, clone the repository to your local machine using the following command:

```sh
git clone https://github.com/yourusername/aiter.git
cd aiter
```

### 2. Install Python Version and Libraries

If the required Python version is not already installed, use `pyenv` to install it. Ensure you have `pyenv` properly set up in your shell.

```sh
pyenv install 3.12
```

Next, install the project dependencies using `pipenv`:

```sh
pipenv install
```

### 3. Activate the Virtual Environment

Activate the virtual environment with:

```sh
pipenv shell
```

### 4. Seed the Database

With the virtual environment activated, navigate to the parent directory and seed the database:

```sh
cd ..
python -m aiter.seed
cd aiter
```

This command will create a `database.db` file outside the `aiter` repository.

### 5. Loading Processed Data

The application requires processed CSV files within `data/<user_id>` for proper functionality. Please contact @jaimescose for detailed instructions on preparing and loading this data. Note that sharing health data involves privacy considerations and must be authorized by @javillarreal.

### 6. Run the Application

Once the data is loaded and processed, you can run the application using:

```sh
uvicorn aiter.main:app --reload
```

## Future Enhancements

- **Database Management:** Consider integrating a more robust database management system to handle user and metric data more efficiently.
- **Data Handling:** Automate the process of loading and processing user data to streamline application setup.
- **Dev Dependencies:** Differentiate development dependencies from production dependencies in the `Pipfile`. This will allow installing dev dependencies with `pipenv install --dev` and excluding them in production environments.
- **User Interface:** Develop a user-friendly interface to manage users, labs, and results more intuitively.

Feel free to contribute to the project by submitting pull requests or opening issues for any bugs or feature requests.

Thank you for using Aiter!