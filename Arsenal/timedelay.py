import sys
import time
if __name__ == '__main__':
    try:
        time.sleep(int(sys.argv[1]))
        print("done")
    except Exception as e:
        print(e)
