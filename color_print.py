class ansi_color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[32m'
    WARNING = '\033[33m'
    FAIL = '\033[31m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def cprint(theme=None):
    start_seq = ansi_color.ENDC
    if theme == 'ok':
        start_seq = ansi_color.OKGREEN
    elif theme == 'warning':
        start_seq = (ansi_color.WARNING 
                + ansi_color.UNDERLINE
                + "WARNING: "
                + ansi_color.ENDC
                + ansi_color.WARNING)
    elif theme == 'fail':
        start_seq = (ansi_color.FAIL
                + ansi_color.BOLD
                + "FAIL: ")
    elif theme == 'header':
        start_seq = ansi_color.BOLD + ansi_color.HEADER

    end_seq = ansi_color.ENDC
    return lambda text, **kw : print(f"{start_seq}{text}{end_seq}", **kw)

def main():
    cprint(theme='warning')("Checking if life is fine: ", end='')
    cprint(theme='ok')('Great it is!', flush=True)

if __name__ == "__main__":
    main()
