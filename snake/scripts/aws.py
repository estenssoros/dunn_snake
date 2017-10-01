import os

import boto

router = {
    'SEB': {
        'bucket_name': 'sebsbucket',
        'AWS_ACCESS_KEY_ID': 'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY': 'AWS_SECRET_ACCESS_KEY'
    },
    'DUNN': {
        'bucket_name': 'morninggun',
        'AWS_ACCESS_KEY_ID': 'DUNN_AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY': 'DUNN_AWS_SECRET_ACCESS_KEY'
    }
}


def connect_s3(switch):
    env = os.environ
    AWS_ACCESS_KEY_ID = router[switch]['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = router[switch]['AWS_SECRET_ACCESS_KEY']
    bucket_name = router[switch]['bucket_name']
    conn = boto.connect_s3(env[AWS_ACCESS_KEY_ID], env[AWS_SECRET_ACCESS_KEY])
    for bucket in conn.get_all_buckets():
        if bucket.name == bucket_name:
            return bucket
    # if conn.lookup(bucket_name) is None:
    #     msg = 'Bucket {} does not exist\n Options are:\n'.format(bucket_name)
    #     for name in conn.get_all_buckets():
    #         msg += '    - {}\n'.format(name)
    #     raise ValueError(msg)
    # else:
    #     bucket = conn.get_bucket(bucket_name)
    # return bucket


def main():
    pass


if __name__ == '__main__':
    main()
