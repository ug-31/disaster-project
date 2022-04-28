import win32clipboard


win32clipboard.OpenClipboard()
data = win32clipboard.GetClipboardData()
win32clipboard.CloseClipboard()
with open('data/clipboard.txt', 'a') as f:
    f.write(data)