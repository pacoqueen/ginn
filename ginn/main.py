from .framework.configuracion import parse_params

def main():
    (user, password, modulo, clase, fconfig,
     verbose, debug, obj_puid) = parse_params()  # @UnusedVariable
    if not modulo:
        from .formularios import menu
        menu.main()
    else:
        from .formularios import launcher
        launcher.run(modulo, clase, user, fconfig, obj_puid, debug, verbose)

if __name__ == '__main__':
    main()
