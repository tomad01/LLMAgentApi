
from typing import Tuple

def chat_parser(text:str)->Tuple[str,bool]:
    """
    a parser for chat like data
    returns the parsed data and a flag for the status of data health
    """
    return text,True


def email_parser(text:str)->Tuple[str,bool]:
    """
    a parser for email like data
    returns the parsed data and a flag for the status of data health
    """
    return text,True