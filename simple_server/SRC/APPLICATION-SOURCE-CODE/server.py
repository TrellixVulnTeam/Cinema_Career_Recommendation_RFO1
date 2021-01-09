from flask import Flask, render_template, request
import mysql.connector

# import mySqlQueries


app = Flask(__name__)

"""
using mysql connector we can connect to our mysql server and use queries to fetch data from DB
"""

# when we run server.py locally

mysql = mysql.connector.connect(
    host="localhost",
    user="DbMysql11",
    password="DbMysql11",
    database="DbMysql11",
    port="3305"
)


# when we run server on the nova: delta-tomcat-vm

# mysql = mysql.connector.connect(
#   host="mysqlsrv1.cs.tau.ac.il",
#   user="DbMysql11",
#   password="DbMysql11",
#   database="DbMysql11",
# )

#### PAGES ###
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/Film_queries.html')
def films():
    return render_template('Film_queries.html')


@app.route('/Actor_queries.html')
def actors():
    return render_template('Actor_queries.html')


@app.route('/Directors_queries.html')
def directors():
    return render_template('Directors_queries.html')


@app.route('/Producer_queries.html')
def producer():
    return render_template('Producer_queries.html')


@app.route('/Genre_queries.html')
def genre():
    return render_template('Genre_queries.html')


### Run querys functions ###

def run_query_0(input):
    ## find the number of films by the given input  cointry name
    cur = mysql.cursor()
    # mysql_query = f"DESCRIBE Film"
    # cur.execute(mysql_query)
    input = str(input)
    input = input.lower()
    print(input)
    headers = [f"number of films in {input} is: "]
    result = [headers]
    print(headers)
    mysql_query = f"SELECT  sum(c.count)  as films_in_country FROM" \
                  f"( SELECT Country,COUNT(*) as count FROM Film  WHERE Country LIKE '%{input}%'" \
                  f"GROUP BY Country order by count desc) as c"

    cur.execute(mysql_query)
    ft = cur.fetchall()
    print(ft)
    if ft[0][0] == None:
        ft[0] = (0,)
    result.extend(ft)
    return render_template('searchResults.html', data=result)


def run_query_1(input):
    ## find the 20 biggest  producer/genre, by the amount of films with rank above 7
    cur = mysql.cursor()
    headers = ["amount", input]

    result = [headers]
    print(headers)
    mysql_query = f"SELECT  count(f.id) as film_amount , p.fullName FROM Film as f, {input} as p ," \
                  f" Film_{input} as fp where (f.id=fp.film_id) and  (fp.{input}_id=p.id) and f.rating>=7 " \
                  f"GROUP BY  p.fullName ORDER BY film_amount DESC LIMIT 20 "

    cur.execute(mysql_query)
    result.extend(cur.fetchall())
    return render_template('searchResults.html', data=result)


def run_query_2(input):
    pass


def run_query_3(input):
    cur = mysql.cursor()
    headers = ["Genre", f"number of {input}s"]
    result = [headers]

    mysql_query = f"SELECT   DISTINCT  g.fullName as genre ,count(w.fullName) num \
    FROM {input} as w, Genre as g,Film_{input} as fw, Film_Genre as fg \
    where w.id=fw.{input}_id  AND  g.id=fg.Genre_id  AND fw.Film_id = fg.Film_id \
    group by genre \
    Order By num DESC \
    LIMIT 5"

    cur.execute(mysql_query)
    result.extend(cur.fetchall())

    return render_template('searchResults.html', data=result)


def run_query_4(input):
    cur = mysql.cursor()
    headers = ["amount", "number of genres"]
    result = [headers]

    mysql_query = f"SELECT  DISTINCT a.fullName as name,count(g.fullName) as count \
FROM {input} as a, Genre as g,Film_{input} as fa, Film_Genre as fg \
Where a.id =fa.{input}_id and g.id = fg.Genre_id and fa.Film_id = fg.Film_id \
Group BY a.fullname,g.fullName \
ORDER BY count DESC \
LIMIT 20"

    cur.execute(mysql_query)
    result.extend(cur.fetchall())

    return render_template('searchResults.html', data=result)


def run_query_5(input):
    pass


def run_query_6(input):
    pass


def run_query_7(input):
    pass


def run_query_8(input):
    cur = mysql.cursor()

    mysql_query = f"SELECT f.year,f.Title,f.Rating from \
                    Film as f,(SELECT distinct f.Year  ,MAX(f.Rating) as max_rating\
                    FROM Film as f WHERE f.Year>={input} AND f.Year<=2020 \
                    GROUP BY f.year) as max_per_year \
                    WHERE f.Year =max_per_year.Year and f.Rating = max_per_year.max_rating \
                    Order by f.Year "

    cur.execute(mysql_query)
    result = cur.fetchall()

    return render_template('searchResults.html', data=result)


def run_query_9():
    cur = mysql.cursor()

    mysql_query = f"SELECT  g.fullName as genre_name ,AVG(f.Rating) as Avg_rating \
                FROM Film as f, Genre as g , Film_Genre as fg \
                WHERE (f.id =fg.film_id) and  (fg. film_id=g.id) \
                GROUP BY  genre_name \
                ORDER BY Avg_rating DESC \
                LIMIT 10"

    cur.execute(mysql_query)
    result = cur.fetchall()

    return render_template('searchResults.html', data=result)


def run_query_10():
    cur = mysql.cursor()

    mysql_query = f"SELECT  g.fullName, count(f.id) as film_amount\
                FROM Film as f, Genre as g , Film_Genre as fg \
                where (f.id=fg.film_id) and  (fg.Genre_id=g.id) and f.rating>=8 \
                GROUP BY  g.fullName \
                ORDER BY film_amount DESC"

    cur.execute(mysql_query)
    result = cur.fetchall()

    return render_template('searchResults.html', data=result)


### call querys functions ###

@app.route('/query0')
def search_return_html():
    input = request.args.get('query')

    return run_query_0(input)


@app.route('/query1')
def query_1():
    input = request.args.get('query')
    return run_query_1("Production")


@app.route('/query2')
def query_2():
    input = request.args.get('query')
    return run_query_1("Genre")


@app.route('/query3')
def query_3():
    input = request.args.get('query')
    return run_query_3(input)


@app.route('/query4')
def query_4():
    return run_query_4("Actor")


@app.route('/query4_Dir')
def query_4_dir():
    return run_query_4("Director")


@app.route('/query5')
def query_5():
    input = request.args.get('query')
    return run_query_5(input)


@app.route('/query6')
def query_6():
    input = request.args.get('query')
    return run_query_6(input)


@app.route('/query7')
def query_7():
    input = request.args.get('query')
    return run_query_7(input)


@app.route('/query8')
def query_8():
    input = request.args.get('query')
    return run_query_8(input)


@app.route('/query9')
def query_9():
    return run_query_9()


@app.route('/query10')
def query_10():
    return run_query_10()


if __name__ == '__main__':
    app.run(port="8888", debug=True)
    # app.run(port="40707", debug=True,host='delta-tomcat- - when running on delta tomcat server.
