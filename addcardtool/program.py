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
Function to get all boards available to the user. Program uses user membership as entry point to get all boards
available to the user.

Returns:
    - JSON object of all boards available to the user
    - Error message and status code if unable to get boards 
"""


def get_all_user_boards_name():
    # Get all boards available in organization
    query = {"key": API_KEY, "token": API_TOKEN}

    headers = {"Accept": "application/json"}

    user_boards_url = f"{MEMBERS_URL}/me/boards"

    response = requests.request("GET", user_boards_url, headers=headers, params=query)

    if response.status_code == 200:
        boards = []
        for board in response.json():
            boards.append((board["name"], board["id"], board["desc"]))
        return boards
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
        lists = []
        for list in response.json():
            lists.append((list["name"], list["id"]))
        return lists


"""
Function to get all labels that are in a specified board ID

Parameters:
    - board_id: ID of the board to get labels for

Returns:
    - Labels in the board in the form of a list of tuples with label name, label color and label id
    - None if unable to get board labels
"""


def get_board_labels(board_id):
    # Get all labels in board
    url = f"{BOARDS_URL}/{board_id}/labels"

    headers = {"Accept": "application/json"}

    query = {"key": API_KEY, "token": API_TOKEN}

    response = requests.request("GET", url, headers=headers, params=query)

    if response.status_code == 200:
        labels = []
        for label in response.json():
            labels.append((label["name"], label["color"], label["id"]))
        return labels
    else:
        print("Error: Unable to get board labels")
        print(response.status_code)
        return None


"""
Function to create a new board

Parameters:
    - board_name: Name of the board to create
    - board_description: Description of the board to create (optional)

Returns:
    - ID of the created board if successful
    - None if unable to create board
"""


def create_new_board(board_name, board_description):
    # Create new board
    url = BOARDS_URL

    headers = {"Accept": "application/json"}
    if board_description:
        query = {
            "key": API_KEY,
            "token": API_TOKEN,
            "name": board_name,
            "desc": board_description,
        }
    else:
        query = {"key": API_KEY, "token": API_TOKEN, "name": board_name}

    response = requests.request("POST", url, headers=headers, params=query)

    if response.status_code == 200:
        board_id = response.json()["id"]
        return board_id
    else:
        print("Error: Unable to create new board")
        print(response.status_code)
        return None


"""
Function to create a new list in a specified board

Parameters:
    - board_id: ID of the board to create list in

Returns:   
    - ID of the created list if successful
    - None if unable to create list
"""


def create_new_list(board_id, list_name):
    # Create new list in board
    url = f"{BOARDS_URL}/{board_id}/lists"

    headers = {"Accept": "application/json"}

    query = {"key": API_KEY, "token": API_TOKEN, "name": list_name}

    response = requests.request("POST", url, headers=headers, params=query)

    if response.status_code == 200:
        list_id = response.json()["id"]
        return list_id
    else:
        print("Error: Unable to create new list")
        print(response.status_code)
        return None


"""
Function to create a new label in a specified board

Parameters:
    - board_id: ID of the board to create label in
    - label_name: Name of the label to create
    - label_color: Color of the label to create
Returns:
    - ID of the created label if successful
    - None if unable to create label
"""


def create_new_label(board_id, label_name, label_color):
    # Create new label in board
    url = f"{BOARDS_URL}/{board_id}/labels"

    headers = {"Accept": "application/json"}

    query = {
        "key": API_KEY,
        "token": API_TOKEN,
        "name": label_name,
        "color": label_color,
        "idBoard": board_id,
    }

    response = requests.request("POST", url, headers=headers, params=query)

    if response.status_code == 200:
        label_id = response.json()["id"]
        return label_id
    else:
        print("Error: Unable to create new label")
        print(response.status_code)
        return None


"""
Function to create a new card in a specified board

Parameters:
    - list_id: ID of the list to create card in
    - card_name: Name of the card to create
    - card_description: Description of the card to create
    - label_ids: List of label IDs to attach to the card

Returns:
    - Status code if successful
    - None if unable to create card
"""


def create_new_card(list_id, card_name, card_description, label_ids):
    # Create new card in board

    headers = {"Accept": "application/json"}

    # parse label ids to string
    label_ids_string = ",".join(label_ids)

    query = {
        "key": API_KEY,
        "token": API_TOKEN,
        "idList": list_id,
        "name": card_name,
        "desc": card_description,
        "idLabels": label_ids_string,
    }

    response = requests.request("POST", CARDS_URL, headers=headers, params=query)

    if response.status_code == 200:
        return response.status_code
    else:
        print("Error: Unable to create new card")
        print(response.status_code)
        return None
