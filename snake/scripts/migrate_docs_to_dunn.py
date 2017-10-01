import os

from aws import connect_s3
from tqdm import tqdm

s3_dir = 'welddocs'


def ensure_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_key_list(switch):
    bucket = connect_s3(switch)
    keys = [key.name for key in bucket.list(s3_dir) if key.name.endswith('.pdf')]
    return keys


def get_work_list():
    dunn = set(get_key_list('DUNN'))
    seb = set(get_key_list('SEB'))
    to_do = seb.difference(dunn)
    return sorted(to_do)


def work():
    to_do = get_work_list()
    seb = connect_s3('SEB')
    dunn = connect_s3('DUNN')
    for key_name in tqdm(to_do):
        key = seb.get_key(key_name)
        dst = os.path.join('tmp', os.path.basename(key))
        key.get_contents_to_filename(dst)
        break


def main():
    ensure_exists('tmp')
    work()


if __name__ == '__main__':
    main()
