import os
import sys
os.system("cd /Users/susmitvengurlekar/Flyer/MongoDB/ && git add .")
os.system(f"cd /Users/susmitvengurlekar/Flyer/MongoDB/ && git commit -m {sys.argv[1]}")
os.system("cd /Users/susmitvengurlekar/Flyer/MongoDB/ && git push")
