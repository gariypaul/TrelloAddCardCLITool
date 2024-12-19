import typer
import subprocess
from PyInquirer import prompt, print_json, Separator
from rich import print as rprint
from typing import Optional
from addcardtool import __app_name__, __version__
from .program import (
    create_new_label,
    get_all_user_boards_name,
    get_board_labels,
    get_board_lists,
    create_new_card,
    create_new_board,
    create_new_list,
)


app = typer.Typer()


"""
Version Callback function to show the version of the application

Parameters:
    - value: bool: Value of the version option

Returns:
    - None 
"""


def version_callback(value: bool):
    if value:
        rprint(f"{__app_name__} version: {__version__}")
        raise typer.Exit()


"""
Function to get card name and description from user

Returns:
    - card_name: str: Name of the card
    - card_desc: str: Description of the card
"""


def get_card_name_and_desc():

    # Create question to get card name and description from user
    question_card_name = [
        {"type": "input", "name": "card_name", "message": "Enter Card Name:"}
    ]

    question_card_desc = [
        {"type": "input", "name": "card_desc", "message": "Enter Card Description:"}
    ]

    # Prompt to get Card Name from user
    card_name = prompt(question_card_name)
    card_name = card_name["card_name"].strip()
    # Check if card name is empty and prompt user to enter card name
    while not card_name:
        rprint("[red bold]Card name cannot be empty![/red bold]")
        card_name = prompt(question_card_name)
        card_name = card_name["card_name"].strip()

    # Prompt to get Card Description from user
    card_desc = prompt(question_card_desc)
    card_desc = card_desc["card_desc"].strip()
    # Check if card description is empty and prompt user to enter card description
    while card_desc == "":
        rprint("[red bold]Card description cannot be empty![/red bold]")
        card_desc = prompt(question_card_desc)
        card_desc = card_desc["card_desc"].strip()

    return card_name, card_desc


"""
Function to get board selection from user

Returns:
    - selected_board_id: str: ID of the selected board
    - is_new_board: bool: True if user selected to add a new board, False if user selected an existing board
"""


def get_board_selection():
    # prompt to query user for board name
    boards = get_all_user_boards_name()
    # check if board query was successful
    if boards is None:
        rprint("[red bold]Error: Unable to get boards[/red bold]")
        raise typer.Exit()
    board_choices = []
    for i in range(len(boards)):
        board_name = boards[i][0]
        board_desc = (
            boards[i][2] if not boards[i][2] == "" else "No Description Avaliable"
        )
        board_choices.append(
            {"name": f"Board Name:{board_name}, Description:{board_desc}", "value": i}
        )
    add_new_board_choice = (
        "Choose this to add a new board instead of selecting from existing boards"
    )
    board_choices.append({"name": f"{add_new_board_choice}", "value": -1})
    question_board_name = [
        {
            "type": "list",
            "name": "board_name",
            "message": "Select Board Name or pick last choice to add new board (New list will be required in next step):",
            "choices": board_choices,
        }
    ]

    question_new_board_name = [
        {
            "type": "input",
            "name": "new_board_name",
            "message": "Enter New Board Name:",
        }
    ]

    question_new_board_desc = [
        {
            "type": "input",
            "name": "new_board_desc",
            "message": "Enter New Board Description (Optional):",
        }
    ]

    # Prompt to get board to add card to
    board_idx = prompt(question_board_name)
    board_idx = board_idx["board_name"]
    is_new_board = True if board_idx == -1 else False
    if is_new_board:
        prompt_new_board_name = prompt(question_new_board_name)
        new_board_name = prompt_new_board_name["new_board_name"].strip()
        while not new_board_name:
            rprint("[red bold]Board name cannot be empty![/red bold]")
            prompt_new_board_name = prompt(question_new_board_name)
            new_board_name = prompt_new_board_name["new_board_name"].strip()

        prompt_new_board_desc = prompt(question_new_board_desc)
        new_board_desc = prompt_new_board_desc["new_board_desc"].strip()
        selected_board_id = create_new_board(new_board_name, new_board_desc)

        # Check if new board was created successfully
        if selected_board_id is None:
            rprint("[red bold]Error: Unable to create new board[/red bold]")
            raise typer.Exit()

        board_name = new_board_name
    else:
        selected_board_id = boards[board_idx][1]
        board_name = boards[board_idx][0]

    return selected_board_id, is_new_board, board_name


"""
Function to get list selection from user

Parameters:
    - selected_board_id: str: ID of the selected board
    - is_new_board: bool: True if user selected to add a new board, False if user selected an existing board

Returns:
    - selected_list_id: str: ID of the selected list

"""


def get_list_selection(selected_board_id, is_new_board):
    question_new_list_name = [
        {
            "type": "input",
            "name": "new_list_name",
            "message": "Chosen board is New/Has no lists. Enter New List Name for Card:",
        }
    ]
    lists = get_board_lists(selected_board_id)


    # check if list query was successful
    if lists is None:
        rprint("[red bold]Error: Unable to get board lists[/red bold]")
        raise typer.Exit()

    if is_new_board or len(lists) == 0:
        prompt_new_list_name = prompt(question_new_list_name)
        new_list_name = prompt_new_list_name["new_list_name"].strip()
        while not new_list_name:
            rprint("[red bold]List name cannot be empty![/red bold]")
            prompt_new_list_name = prompt(question_new_list_name)
            new_list_name = prompt_new_list_name["new_list_name"].strip()
        selected_list_id = create_new_list(selected_board_id, new_list_name)
        # check if new list was created successfully
        if selected_list_id is None:
            rprint("[red bold]Error: Unable to create new list[/red bold]")
            raise typer.Exit()
        list_name = new_list_name
    else:
        # prompt to ask user for specified column/list to add card to
        # Get all columns from board
        list_choices = []
        for i in range(len(lists)):
            list_name = lists[i][0]
            list_choices.append({"name": f"List Name:{list_name}", "value": i})

        question_list_name = [
            {
                "type": "list",
                "name": "list_name",
                "message": "Select List Name:",
                "choices": list_choices,
            }
        ]

        # Prompt to get list to add card to
        list_idx = prompt(question_list_name)
        list_idx = list_idx["list_name"]
        selected_list_id = lists[list_idx][1]
        list_name = lists[list_idx][0]
    return selected_list_id, list_name


"""
Function to get label selection from user

Parameters:
    - selected_board_id: str: ID of the selected board

Returns:
    - selected_labels_ids: list: List of selected label IDs

"""


def get_label_selections(selected_board_id):
    # get all labels on board
    labels = get_board_labels(selected_board_id)
    # check if label query was successful
    if labels is None:
        rprint("[red bold]Error: Unable to get board labels[/red bold]")
        raise typer.Exit()
    # Prompt to get label from user
    if len(labels) == 0:
        question_label = [
            {
                "type": "list",
                "name": "is_new_label",
                "message": "This board has no labels. Create new label or have no labels on card (Select actions or no label to exit after selecting all labels or none)",
                "choices": [
                    {"name": "Create New Label", "value": 1},
                    {"name": "No label/Selected all Labels", "value": -1},
                ],
            }
        ]
    else:
        question_label = [
            {
                "type": "list",
                "name": "is_new_label",
                "message": "Do you want to create a new label? Or do you want to select from existing labels? (Select actions or no label to exit after selecting all labels or none)",
                "choices": [
                    {"name": "Create New Label", "value": 1},
                    {"name": "Select from Existing Labels", "value": 0},
                    {"name": "No label/Selected all Labels", "value": -1},
                ],
            }
        ]
    label_choices = []
    for i in range(len(labels)):
        label_name = labels[i][0] if not labels[i][0] == "" else "No Name Provided"
        label_color = labels[i][1]
        label_choices.append(
            {"name": f"Label Name:{label_name}, Label Color:{label_color}", "value": i}
        )

    question_existing_label_name = [
        {
            "type": "list",
            "name": "label_name",
            "message": "Select From existing Labels:",
            "choices": label_choices,
        }
    ]

    selected_labels_ids = []
    # Prompt to get label from user
    is_new_label = 0
    while not is_new_label < 0:

        is_new_label = prompt(question_label)
        is_new_label = is_new_label["is_new_label"]
        # If user wants to create a new label, prompt user to enter label name and color
        if is_new_label == 1:
            question_new_label_name = [
                {
                    "type": "input",
                    "name": "new_label_name",
                    "message": "Enter New Label Name:",
                }
            ]

            question_new_label_color = [
                {
                    "type": "input",
                    "name": "new_label_color",
                    "message": "Enter New Label Color (Valid values: yellow, purple, blue, red, green, orange, black, sky, pink, lime):",
                }
            ]
            valid_colors = [
                "yellow",
                "purple",
                "blue",
                "red",
                "green",
                "orange",
                "black",
                "sky",
                "pink",
                "lime",
            ]
            new_label_name = prompt(question_new_label_name)
            new_label_name = new_label_name["new_label_name"].strip()
            # Check if new label name is empty and prompt user to enter new label name
            while not new_label_name:
                rprint("[red bold]Label name cannot be empty![/red bold]")
                new_label_name = prompt(question_new_label_name)
                new_label_name = new_label_name["new_label_name"].strip()

            new_label_color = prompt(question_new_label_color)
            new_label_color = new_label_color["new_label_color"].strip()
            # Check if new label color is empty and prompt user to enter new label color
            while not new_label_color or new_label_color not in valid_colors:
                rprint(
                    "Error: [red bold]Label color cannot be empty![/red bold] and must be one of the following colors: yellow, purple, blue, red, green, orange, black, sky, pink, lime"
                )
                new_label_color = prompt(question_new_label_color)
                new_label_color = new_label_color["new_label_color"].strip()
            new_label_id = create_new_label(
                selected_board_id, new_label_name, new_label_color
            )
            # check if new label was created successfully
            if new_label_id is None:
                rprint("[red bold]Error: Unable to create new label[/red bold]")
                raise typer.Exit()
            selected_labels_ids.append(new_label_id)
        elif is_new_label == 0:
            selected_label = prompt(question_existing_label_name)
            selected_label = selected_label["label_name"]
            selected_label_id = labels[selected_label][2]
            selected_labels_ids.append(selected_label_id)
        else:
            break
    return selected_labels_ids


@app.callback()
def callback(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the applications version then exit application",
        callback=version_callback,
        is_eager=True,
    )
) -> None:
    pass



@app.command("add-card")
def add_card():
    """
    Add a new card to a specified board and list
    """

    # Get card name and description from user
    card_name, card_desc = get_card_name_and_desc()

    # Get board selection from user
    selected_board_id, is_new_board, board_name = get_board_selection()

    # Get list selection from user
    selected_list_id, list_name = get_list_selection(selected_board_id, is_new_board)

    # Get label selection from user
    selected_labels_ids = get_label_selections(selected_board_id)

    # Add card to board
    rprint(
        f"Adding Card to Board:[blue] {board_name}[/blue], List: [green]{list_name}[/green] with card name: [yellow]{card_name}[/yellow] and card description: [magenta]{card_desc}[/magenta]\n"
    )
    card_response = create_new_card(
        selected_list_id, card_name, card_desc, selected_labels_ids
    )
    if card_response:
        rprint("[green bold]Card Added Successfully[/green bold]\n")
        raise typer.Exit()
    else:
        rprint(
            "[red bold]Error: Unable to add card to board run the program again[/red bold]\n"
        )
        raise typer.Exit()
