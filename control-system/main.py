from src import BusinessLogic
from time import sleep


if __name__ == '__main__':
    sleep(10)
    bl = BusinessLogic(10)
    bl.run()