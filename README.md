# Trello Add Card Command Line Tool

## About 
This project is a Command Line Application that interfaces with the Trello API to make addition of cards easy and well abstracted directly from the Command Line
This program is able to add a Trello card with labels and a comment to a specified column of a board.
### Features
This CLI tool has the following features built within it with regard to adding Cards to Trello
1. Can add a card to a preexisting board (Shows user all the boards they can edit and user can select which board to add card to)
2. Can add a card to a preexisiting list (Shows user all available lists in a board of their choice and allows them to make a selection)
3. Can add a card to a new board (User can create a new board to add the card to). This feature then makes the user to create a new list to add the card to since the new board is empty.
4. Can add a card to a new list (User can create a new list on a selected board and add card to new list)
5. Can add different labels to a card (User can either create new labels or add preexisting labels. The user can select multiple labels for one card)

## Running Application 
The following sections outline how to get the CLI tool to work. Before following the steps to run the program. First you have to have the files in your local device (Cloning this repository or downloading the files to local device). The folder structure should be as follows
main_folder/
│
├── addcardtool/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   └── program.py
│
├── tests/
│   ├── __init__.py
│   └── test_addcardtool.py
│
├── README.md
├── .env
└── requirements.txt
A .env file is listed but not provided in this file you must have your Trello API_KEY, API_TOKEN and USERNAME
A sample of what this should look like is as follows: 
```
TRELLO_API_KEY="{YOUR_API_KEY}"
TRELLO_API_TOKEN="{YOUR_API_TOKEN}"
TRELLO_USERNAME="{YOUR_USERNAME}"
```
To get these you can refer to the Trello Developer Website to learn how to access these required values from your account: [Trello Developer Website](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/)

Python should also be installed and added to your PATH. More information on this can be found here: [Python Installation Guide](https://www.python.org/downloads/)
### Installing Dependencies
After setting up the folders and files required. The next step is installing dependencies. 
To install dependencies run 
```console
foo@bar:~$ pip install -r requirements.txt
```

###  Running Applicaition 
To run the main application to add a card run: 
```console
foo@bar:~$ python -m addcardtool add-card
```
The python command might change depending on your environment. It might be python3 or python. 
The program guides on how to use it throught the prompts. Follow the prompts and you will be able to add a card to your Trello Board(s). 

You can also run the version option to check the version of the application you are running: 

```console
foo@bar:~$ python -v
```
or

```console
foo@bar:~$ python --version
```
Using the --help option also gives a help menu with a description of the options and commands

```console
foo@bar:~$ python --help
```

