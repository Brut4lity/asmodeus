import fileinput, os

directory = os.listdir('json')
for f in directory:
    with fileinput.FileInput('json' + os.sep + f, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace('Invisiblity', 'Invisibility'), end='')
            print(line.replace('Can See Invisibles', 'Can See Invisible'), end='')
            print(line.replace('Invisibile', 'Invisible'), end='')
            print(line.replace('Villians', 'Villains'), end='')
            print(line.replace('Wizzards', 'Wizards'), end='')