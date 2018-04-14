def getch():
    try:
        import msvcrt
        ch = msvcrt.getch()

    except ImportError:
            import sys
            import tty
            import termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def auto_run(self, files, dirs):
    while (True):
        print
        '\nTo show a list of files and dirs to be changed press "l"'
        print
        'To update the destination press "u"'
        print
        'To quit type q\n'

        command = msvcrt.getch()

        if command.lower() == 'l':
            self.run_type(files, dirs, commit_changes=False)

        elif command.lower() == 'u':
            self.update(files, dirs, commit_changes=True)
            break
        elif command.lower() == 'q':
            break
        else:
            pass

if __name__ == "__main__":
    print(getch())