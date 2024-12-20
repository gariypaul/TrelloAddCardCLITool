import typer
import subprocess
from PyInquirer import prompt, print_json, Separator
from rich import print as rprint
import requests
import json
import dotenv
import os

# Load environment variables
dotenv.load_dotenv()

# Get environment variables for API calls
API_KEY = os.getenv("TRELLO_API_KEY")
API_TOKEN = os.getenv("TRELLO_API_TOKEN")
USERNAME = os.getenv("TRELLO_USERNAME")

# API URLS
BASE_URL = "https://api.trello.com/1/"
CARDS_URL = f"{BASE_URL}cards"
BOARDS_URL = f"{BASE_URL}boards"
LISTS_URL = f"{BASE_URL}lists"
LABELS_URL = f"{BASE_URL}labels"
MEMBERS_URL = f"{BASE_URL}members"

"""
TODO: Delete after implementing all listed functions of the program
(Program Requirements) 
-- Add new card to trello.com board (any board)
-- Add trello card with labels
-- Card to be added to specified column in the board
"""

"""'
Application Process to add a new card: 
1. Board needs to be specified: 
    -Get all boards from organization 
    -List all boards in organization and let user pick board
    -Use board ID returned for board and store
2. Column/List needs to be specified: 
    -Get all columns from board
    -List all columns in board and let user pick column
    -Use column ID returned for column and store
3. Add new card to specified board and column
    - Ask user for card name 
    - Ask user for card description
    - List all board labels and let user pick label/ ask user if they want to add label 
    - Add card to board and column with specified label, name and description
    - If creating new label ask user for label name and color and add label to card and board 
4. Print card details to user and indicate card has been added to board and column
5. Ask user if they want to add another card to the board or exit the program
"""


"""
Function to get all boards available to the user. Program uses user membership as entry point to get all boards
available to the user.

Returns:
    - JSON object of all boards available to the user
    - Error message and status code if unable to get boards 
"""
def get_all_user_boards():
    # Get all boards available in organization
    query = {"key": API_KEY, "token": API_TOKEN}

    headers = {"Accept": "application/json"}

    user_boards_url = f"{MEMBERS_URL}/{USERNAME}/boards"

    response = requests.request("GET", user_boards_url, headers=headers, params=query)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error: Unable to get boards")
        print(response.status_code)


"""
Function to get all board details for a specified board ID

Parameters:
    - board_id: ID of the board to get details for

Returns:
    - JSON object of board details
    - Error message and status code if unable to get board details
"""
def get_board(board_id):
    # Get board details
    query = {"key": API_KEY, "token": API_TOKEN}

    headers = {"Accept": "application/json"}

    board_url = f"{BOARDS_URL}/{board_id}"
    board_lists_url = f"{board_url}/lists"

    response_board = requests.request("GET", board_url, headers=headers, params=query)

"""
Function to get all lists that are in a specified board ID

Parameters:
    - board_id: ID of the board to get lists for

Returns:
    - JSON object of all lists in the board
    - Error message and status code if unable to get board lists
"""
def get_board_lists(board_id):
    # Get all lists in board
    url = f"{BOARDS_URL}/{board_id}/lists"

    headers = {"Accept": "application/json"}

    query = {"key": API_KEY, "token": API_TOKEN}

    response = requests.request("GET", url, headers=headers, params=query)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error: Unable to get board lists")
        print(response.status_code)



app = typer.Typer()

# @app.command("list-boards")
# def list_all_boards():
#     """
#     List all boards available to the user
#     """
#     boards = get_all_user_boards()
#     rprint(boards)

# @app.command("list-board-lists")
# def list_board_lists(board_id: str):
#     """
#     List all lists available in a specified board
#     """
#     print(board_id)

@app.command("add-card")
def add_card():
    """
    Add a new card to a specified board and list
    """
    question_card_name = [
        {
            'type':'input',
            'name':'card_name',
            'message':'Enter Card Name:'
        }
    ]

    question_card_desc = [
        {
            'type':'input',
            'name':'card_desc',
            'message':'Enter Card Description:'
        }
    ]

    card_name = prompt(question_card_name)
    while card_name==" ":
        rprint("[red bold]Card name cannot be empty![red bold]")
        card_name = prompt(question_card_name)
    
    card_desc = prompt(question_card_desc)
    while card_desc=="":
        rprint("[red bold]Card description cannot be empty![red bold]")
        card_desc = prompt(question_card_desc)
    
    rprint(f"Card Name: {card_name['card_name']}")
    rprint(f"Card Description: {card_desc['card_desc']}")

if __name__ == "__main__":
    app()