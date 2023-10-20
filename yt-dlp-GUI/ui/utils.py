import socket

def is_connected():
    """
    Checks if the machine has an active internet connection.

    Returns:
    bool: True if the machine is connected to the internet, False otherwise.
    """
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False    