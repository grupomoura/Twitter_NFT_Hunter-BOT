import sqlite3
con = sqlite3.connect('db/data.db')
cur = con.cursor()


def commit_db_now():
    con.commit()


def insert_db(twitters, following, twitterId):
    cur.execute("INSERT into posts_twitter (twitters, following, twitterId) values (?,?,?)", (twitters, following, twitterId))
    con.commit()


def insert_db_freemint(twitters, freemint_link, followers_count):
    cur.execute("INSERT into freemint (twitters, freemint_link, followers_count) values (?,?,?)", (twitters, freemint_link, followers_count))
    con.commit()


def insert_db_follow(value):
    cur.execute("INSERT into posts_twitter (following) values (?)", (value,))


def insert_db_twitterId(value):
    cur.execute("INSERT into posts_twitter (twitterId) values (?)", (value,))


"""def insert_db_recusadas(value):
    cur.execute("INSERT into posts_reddit_recusadas (postagem_recusada) values (?)", (value,))
    con.commit()"""


def consult_db():
    data = list(cur.execute("SELECT * from posts_twitter"))
    return data


def del_dbdata_7antes():
    # Para excluir registros anteriores a 7 dias atrás
    print('\nBanco de dados atualizado!\n')
    cur.execute("DELETE FROM posts_twitter WHERE created_at < datetime('now' , '-7 days')")


def consult_db_twitter_id(id):
    data_ids = list(cur.execute("SELECT * from posts_twitter where twitterId"))
    data_ids.reverse()
    for data in data_ids:
        if id in data:
            return True
    return False


def removeColumn(table, column):
    columns = []
    for row in cur.execute('PRAGMA table_info(' + table + ')'):
        columns.append(row[1])
    columns.remove(column)
    columns = str(columns)
    columns = columns.replace("[", "(")
    columns = columns.replace("]", ")")
    for i in ["\'", "(", ")"]:
        columns = columns.replace(i, "")
    cur.execute('CREATE TABLE temptable AS SELECT ' + columns + ' FROM ' + table)
    cur.execute('DROP TABLE ' + table)
    cur.execute('ALTER TABLE temptable RENAME TO ' + table)
    con.commit()


"""
(.*\n)\1
$1

CREATE TABLE post_registry (
	id BIGINT PRIMARY KEY AUTOINCREMENT,
	criado_em TIMESTAMP,
	postagem VARCHAR,
	CONSTRAINT post_registry_PK PRIMARY KEY (id)
);"""

"""
SELECT *
  FROM post_registry;

SELECT *
  FROM post_registry
 WHERE id = 1;

DELETE 
  FROM nft_db
 WHERE id = 1;

 UPDATE nft_db
   SET postagem = 'novo valor'
 WHERE ID = 1; 

"""

"""
CREATE TABLE posts_twitter(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    twitters TEXT UNIQUE,
    "following" TEXT,
    twitterId TEXT UNIQUE, 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""