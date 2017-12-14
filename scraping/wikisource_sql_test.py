import mysql.connector, re

find_links_from = "SELECT p.page_title AS from_article, pl.pl_title AS to_article FROM (SELECT * FROM page WHERE page_title=%s) AS p INNER JOIN (SELECT * FROM pagelinks) AS pl ON p.page_id = pl.pl_from"
find_links_to = "SELECT p.page_title AS from_article, pl.pl_title AS to_article FROM (SELECT * FROM pagelinks WHERE pl_title=%s) AS pl INNER JOIN (SELECT * FROM page) AS p ON p.page_id = pl.pl_from"

def process_title(title):
    return re.sub(" ", "_", title)

def find_all_links_from(conn, title):
    p_title = process_title(title)
    cursor = conn.cursor()
    cursor.execute(find_links_from, [p_title])
    rows = cursor.fetchall()
    cursor.close()
    return rows

def find_all_links_to(conn, title):
    p_title = process_title(title)
    cursor = conn.cursor()
    cursor.execute(find_links_to, [p_title])
    rows = cursor.fetchall()
    cursor.close()
    return rows

conn = mysql.connector.connect(user='root', database='wikipedia')
print find_all_links_to(conn, "Gettysburg Address")
