import os

_path = os.getcwd() + os.sep

def recur(path, fd=True):
    for fi in os.listdir(path):
        if os.path.isdir(path + fi):
            if fi == '__pycache__' and fd:
                for fi2 in os.listdir(path + fi):
                    os.remove(path + fi + '/'+ fi2)
                    print(path + fi + '/'+ fi2)
                os.rmdir(path + fi)
                print('*********', path)
            else:
                recur(path + fi + '/')
                
recur(_path, None)
print('ok')