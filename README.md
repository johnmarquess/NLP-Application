# NLP Application #

## Description: ##

This Flask application is designed to provide a user-friendly interface for handling files, processing data, and
integrating machine learning models for natural language processing tasks. It features a robust architecture using Flask
Blueprints, Flask-WTF for form handling, and Pandas for data processing.

## Features: ##

- __File Management__: Upload, view, and delete files.
- __Data Processing__: Select worksheets from uploaded files and process selected columns.
- __Machine Learning Integration__: Load and configure NLP models from libraries like spaCy.
- __Responsive User Interface__: Built with Bootstrap 5 for a modern, responsive design.

### Machine Learning and Reporting are not implemented yet!: ###

## Installation: ##

To set up the project locally, follow these steps:

1. Clone the repository.

```bash
git clone https://github.com/johnmarquess/NLP-Application.git
cd NLP-Application
```

2. __Create a Virtual Environment (Optional):__

```bash 
python -m venv venv
source venv/bin/activate  # For Unix or MacOS
venv\Scripts\activate  # For Windows
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```
Another dependency is that  you need to have the correct spaCy models downloaded and installed. For example ` python -m spacy download en_core_web_sm` to download and install the small English web core model. More information at the [spaCy website](https://spacy.io/usage/models).   

4. Run the Application:

On Unix or MacOS, use the following commands to start the server:

```bash
export FLASK_APP=app:create_app
flask run
```

On Windows Powershell, use the following commands instead:

```powershell
$env:FLASK_APP = "app:create_app"
flask run
```

On Windows Command Prompt, use the following:

```cmd
set FLASK_APP=app:create_app
flask run
```

## Usage ##

After starting the application, navigate to http://localhost:5000 in your web browser to interact with the app.

- __Uploading Files:__ Use the file upload interface to upload .csv, .xls, or .xlsx files.
- __Data Processing:__ Select an uploaded file to view its worksheets and columns. Choose columns for data processing
  and save the selection as a new .csv file.
- __Model Integration:__ In the Data Modeling section, choose and configure NLP models for analysis.

## Configuration ##

__Config File:__ Edit config.py to change configuration settings like secret keys and folder paths.
__Security:__ The application includes measures for secure file handling.

## Testing ##
To run the (meagre amount of) tests, use the following command:

```bash
pytest
```

## Contributing ##

Contributions to this project are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature.
3. Make your changes and commit them.
4. Push to your fork and submit a pull request.

## License ##

This project is licensed under the [MIT Licence](https://chat.openai.com/g/g-sSV5plDob-flask-helper/c/LICENSE).
