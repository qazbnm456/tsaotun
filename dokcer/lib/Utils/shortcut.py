"""This module provides shortcut functionality (mapping command to another command)"""

mapping = {
    "ps": "container ps",
    "images": "image images",
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
    c = 0
    for i, val in enumerate(argv):
        if val.startswith("-"):
            if val == '-H' or val == '--host':
                c = c - 1
            continue
        else:
            c = c + 1
        if (c == 1) and mapping.get(val):
            argv[i] = mapping.get(val)
            break
    return ' '.join(argv).split()
