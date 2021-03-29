from scripts import ScriptManager


if __name__ == '__main__':
    s = ScriptManager()

    action_dict = {'a': s.addEvent,
                   'l': s.loadScript,
                   'r': s.run,
                   'k': exit}

    while 1:
        command = input()
        if not action_dict[command[0]](command[1:]):
            print("Error processing command", command)

