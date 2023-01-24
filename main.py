import DataBase
from dotenv import load_dotenv


load_dotenv()


def main():
    DataBase.init().init_database()


if __name__ == '__main__':
    main()
