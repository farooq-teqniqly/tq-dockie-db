"""
An error handling module for the DockieDb API.
"""
from flask import abort


def respond_with_error(status_code, message):
    """
       Raise an HTTPException with the given status code and error message.

       Args:
           status_code (int): The HTTP status code to be raised.
           message (str): The error message to be included in the HTTP response.

       Returns:
           None

       Raises:
           HTTPException: An HTTPException is raised with the given status code and message.
   """
    abort(status_code, message)
