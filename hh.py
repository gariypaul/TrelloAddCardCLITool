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

    user_boards_url = f"{MEMBERS_URL}/me/boards"

    response = requests.request("GET", user_boards_url, headers=headers, params=query)

    if response.status_code == 200:
        boards = []
        for board in response.json():
            boards.append((board["name"],board["id"],board["desc"]))
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
            lists.append((list["name"],list["id"]))
        return lists
            
    else:
        print("Error: Unable to get board lists")
        print(response.status_code)

def get_board_labels(board_id):
    # Get all labels in board
    url = f"{BOARDS_URL}/{board_id}/labels"

    headers = {"Accept": "application/json"}

    query = {"key": API_KEY, "token": API_TOKEN}

    response = requests.request("GET", url, headers=headers, params=query)

    if response.status_code == 200:
        labels = []
        for label in response.json():
            labels.append((label["name"],label["color"],label["id"]))
        return labels
    else:
        print("Error: Unable to get board labels")
        print(response.status_code)
        return None

def create_new_label(board_id,label_name,label_color):
    # Create new label in board
    url = f"{BOARDS_URL}/{board_id}/labels"

    headers = {"Accept": "application/json"}

    query = {"key": API_KEY, "token": API_TOKEN, "name": label_name, "color": label_color, "idBoard": board_id}

    response = requests.request("POST", url, headers=headers, params=query)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error: Unable to create new label")
        print(response.status_code)
        return response.status_code
    
def create_new_card(board_id, list_id, card_name, card_description, label_ids):
    # Create new card in board

    headers = {"Accept": "application/json"}

    #parse label ids to string
    label_ids_string = ",".join(label_ids)

    query = {"key": API_KEY, "token": API_TOKEN, "idList": list_id, "name": card_name, "desc": card_description, "idLabels": label_ids_string}

    response = requests.request("POST", CARDS_URL, headers=headers, params=query)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error: Unable to create new card")
        print(response.status_code)
        return None

def create_new_board(board_name, board_description):
    # Create new board
    url = BOARDS_URL

    headers = {"Accept": "application/json"}
    if(board_description):
        query = {"key": API_KEY , "token": API_TOKEN, "name": board_name, "desc": board_description}
    else:
        query = {"key": API_KEY , "token": API_TOKEN, "name": board_name}
    
    response = requests.request("POST", url, headers=headers, params=query)

    if response.status_code == 200:
        board_id = response.json()["id"]
        return board_id
    else:
        print("Error: Unable to create new board")
        print(response.status_code)
        return None
    
def main():
    # Get all boards available to the user
    board_id = "6764aced1fa15869f3f76df5"
    list_id = "676323ae3aede03aa2f2156c"
    label_name = "Test Label"
    label_ids = ["6764974aa597554c2c3c67f4", "67649234cf987481a0014e55"]
    lists = get_board_lists(board_id)
    print(lists)
    print(len(lists))
   

if __name__ == "__main__":
    main()

