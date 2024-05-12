import os


def get_api_key():
    return os.environ.get('API_KEY')


if __name__ == '__main__':
    print(get_api_key())
