"""This module provides shortcut functionality (mapping command to another command)"""

mapping = {
    "ps": "container ls",
    "images": "image ls",
    "pull": "image pull",
    "build": "image build",
    "save": "image save",
    "rmi": "image rm",
    "run": "container run",
    "exec": "container exec",
    "stop": "container stop",
    "restart": "container restart",
    "rename": "container rename",
    "rm": "container rm",
    "cp": "container cp",
    "logs": "container logs",
    "top": "container top"
}


def shortcut(argv):
    """Return mapping command if there exists one"""
    for i, val in enumerate(argv):
        if mapping.get(val):
            argv[i] = mapping.get(val)
            break
    return ' '.join(argv).split()
