import os
import re

import MySQLdb
from tqdm import tqdm

from aws import connect_s3

s3_dir = 'welddocs'
re_doc = re.compile('\w+C([\w]+)_\w+.pdf')

DB_CONN = {'host': '52.15.123.63',
           'user': 'jdunn',
           'passwd': 'seb132435',
           'db': 'dunn_snake'}


def analyze_s3():
    bucket = connect_s3('SEB')
    files = [os.path.basename(x.name) for x in bucket.list(s3_dir) if x.name.endswith('.pdf')]
    key_mapping = {f: re_doc.findall(f)[0] for f in files}
    doc_mapping = {}
    for key_name, doc in key_mapping.iteritems():
        if doc in doc_mapping:
            doc_mapping[doc].append(key_name)
        else:
            doc_mapping[doc] = [key_name]
    doc_mapping = {k: '|'.join(v) for k, v in doc_mapping.iteritems()}
    return doc_mapping


def write_to_mysql(doc_mapping):
    conn = MySQLdb.connect(**DB_CONN)
    curs = conn.cursor()
    curs.execute('TRUNCATE TABLE weld_docs')
    sql = '''INSERT INTO weld_docs (doc_number, s3_key) VALUES '''
    values = []
    for k, v in tqdm(doc_mapping.iteritems(), total=len(doc_mapping)):
        values.append("('{}','{}')".format(k, v))
        if len(values) == 200:
            curs.execute(sql + ','.join(values))
            conn.commit()
            values = []
    if values:
        curs.execute(sql + ','.join(values))
        conn.commit()
    curs.close()
    conn.close()


def sync_documents_with_s3():
    doc_mapping = analyze_s3()
    write_to_mysql(doc_mapping)


def main():
    sync_documents_with_s3()

if __name__ == '__main__':
    main()
