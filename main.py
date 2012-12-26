
while True:
    choice = raw_input("choose starting program: (e)ditor, (g)ame:\n>")
    if choice == 'e':
        import game_code.main
        game_code.main.editor()
        break
    if choice in ('g',''):
        import game_code.main
        game_code.main.main()
        break