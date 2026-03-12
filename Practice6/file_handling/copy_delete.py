import shutil
import os

shutil.copy("source.txt", "copy_source.txt")

if os.path.exists("copy_source.txt"):
    os.remove("copy_source.txt")
    print("File deleted")
else:
    print("File does not exist")