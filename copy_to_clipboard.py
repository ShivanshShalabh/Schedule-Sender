import pyperclip
def copy_to_clipboard():
    f = open('schedule.txt','r')
    pyperclip.copy(f.read())
    f.close()
if __name__ == '__main__':
    copy_to_clipboard()
