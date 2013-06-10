from framework.configuracion import parse_params

def main():
    user, password, modulo, clase = parse_params()
    if not modulo:
        from formularios import menu
        menu.main()
    else:
        from formularios import launcher
        launcher.main()

if __name__ == '__main__':
    main()

