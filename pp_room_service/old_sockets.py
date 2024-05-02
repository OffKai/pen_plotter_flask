import logging

from flask import Flask, request
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room

from app import socket


@socket.on("connect")
def on_connect():
    logging.info(f"Client {request.sid} has connected.")


@socket.on("disconnect")
def on_disconnect():
    logging.info(f"Client {request.sid} has disconnected.")


@socket.on("join")
def on_join(data):
    room = data["room"]
    logging.info(f"Client {request.sid} has joined room: '{room}'.")
    join_room(room)


@socket.on("leave")
def on_leave(data):
    room = data["room"]
    logging.info(f"Client {request.sid} left room: '{room}'.")
    leave_room(room)


@socket.on("plot")
def handle_plot_requests(data):
    if current_user.is_authenticated:
        # forward message from guests to plotter
        logging.info(f"Client {request.sid} has requested a plot.")
        emit("plot", data, to="plotter")


@socket.on("notify")
def handle_notifications(data):
    # forward message from plotter to guests
    logging.info(f"Plotter {request.sid} has sent a status update.")
    emit("notify", data, to="guests")
