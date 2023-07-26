import d20
while True:
    print('input what to roll')
    print('templates: "d20" "1d20" "3d4+3" "1d8+1d6+3"')
    print('input "stop" or send empty message to stop')
    answer = input()
    print(str(d20.roll(answer)))
    if answer == '' or answer == 'stop':
        break