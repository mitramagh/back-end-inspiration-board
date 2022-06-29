from flask import Blueprint, request, jsonify, make_response
from flask import abort  # added for validations
from app import db
from os import abort
# import models:

from app.models.board import Board
from app.models.card import Card


# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("board_bp", __name__, url_prefix="/boards")

# Board Model routes:

# 1. POST - Create a new board, by filling out a form. The form includes "title" and "owner" name of the board.
# POST displays ERROR msg if empty/blank/invalid/missing "title" or "owner" input.


@board_bp.route("", methods=["POST"])
def create_one_board():
    request_body = request.get_json()
    request_body = validate_board_input(request_body)

    new_board = Board(
        title=request_body['title'], owner=request_body['owner'])

    db.session.add(new_board)
    db.session.commit()
    return {
        'id': new_board.board_id,
        'msg': f'New board {new_board.title} created'
    }, 201

# helper function:


def validate_board_input(request_body):
    if "title" not in request_body or "title" == "":
        abort(make_response(
            {"details": "Invalid data. Title missing or invalid from board"}, 400))
    if "owner" not in request_body or "owner" == "":
        abort(make_response(
            {"details": "Invalid data. Owner missing or invalid from board"}, 400))
    return request_body

# 2.GET- Read; View a list of all boards
# 3. GET - Read; Select a specific board

# POST: Create a new card for the selected board,
# by filling out a form and filling out a "message."
# See an error message if I try to make the card's "message" more than 40 characters.
# All error messages can look like a new section on the screen, a red outline around the input field, and/or disabling the input, as long as it's visible
# See an error message if I try to make a new card with an empty/blank/invalid/missing "message."

# Helper function to validate board_id:


def validate_board(board_id):
    try:
        board_id = int(board_id)
    except:
        abort(make_response(
            {"message": f"Board: {board_id} is not a valid board id"}, 400))
    board = Board.query.get(board_id)
    if not board:
        abort(make_response(
            {"message": f"Board: #{board_id} not found"}, 404))
    return board


@board_bp.route("/<board_id>/cards", methods=["POST"])
def create_card_for_board(board_id):
    board = validate_board(board_id)
    request_body = request.get_json()

    if len(request_body["message"]) > 0 and len(request_body["message"]) <= 40:
        new_card = Card(
            message=request_body["message"],
            board=board
        )
    else:
        abort(make_response(
            {"message": f"Card message for board #{board_id} too long, please keep it under 40 characters"}, 400))

    db.session.add(new_card)
    db.session.commit()

    return {
        "msg": f" New card created for {board.title}"
    }, 201