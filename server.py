from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import datetime
import time

app = Flask(__name__)

mysql = MySQLConnector(app,'friends')

@app.route('/')
def index():
    one_friend = {}
    one_friend['id'] = ''
    one_friend['first_name'] = ''
    one_friend['last_name'] = ''
    one_friend['occupation'] = ''
    query = "SELECT id, first_name, last_name, concat(first_name, ' ', last_name) as full_name, age, occupation FROM friends"
    friends = mysql.query_db(query)
    return render_template('index.html', all_friends=friends, one_friend=one_friend)

@app.route('/friends', methods=['POST'])
def addModifyDelete():

    if request.form['submit'] == 'Delete':
        query = "DELETE FROM friends WHERE id = :id"
        data = {'id': request.form['friend_id']}
        mysql.query_db(query, data)
    elif request.form['submit'] == 'Update':
        query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, age = :age, occupation = :occupation, updated_at = :updated_at WHERE id = :id"
        data = {
                'first_name': request.form['first_name'],
                'last_name':  request.form['last_name'],
                'age':  request.form['age'],
                'occupation': request.form['occupation'],
                'updated_at': datetime.datetime.now(),
                'id': request.form['friend_id']
            }
        mysql.query_db(query, data)
    elif request.form['submit'] == 'Add':
        # Write query as a string. Notice how we have multiple values
        # we want to insert into our query.copy
        query = "INSERT INTO friends (first_name, last_name, age, occupation, created_at, updated_at) VALUES (:first_name, :last_name, :age, :occupation, NOW(), NOW())"
        # We'll then create a dictionary of data from the POST data received.
        data = {
                'first_name': request.form['first_name'],
                'last_name':  request.form['last_name'],
                'age':  request.form['age'],
                'occupation': request.form['occupation']
            }
        # Run query, with dictionary values injected into the query.
        mysql.query_db(query, data)

    return redirect('/')

@app.route('/friends/<friend_id>')
def show(friend_id):
    # Write query to select specific user by id. At every point where
    # we want to insert data, we write ":" and variable name.
    query = "SELECT id, first_name, last_name, concat(first_name, ' ', last_name) as full_name, age, occupation FROM friends WHERE id = :specific_id"
    # Then define a dictionary with key that matches :variable_name in query.
    data = {'specific_id': friend_id}
    # Run query with inserted data.
    friends = mysql.query_db(query, data)
    # Friends should be a list with a single object,
    # so we pass the value at [0] to our template under alias one_friend.

    if not friends:
        friends = [{'id': '0', 'first_name': 'Not Found', 'last_name': 'Not Found', 'full_name': 'None', 'occupation': 'Not Assigned'}]

    print friends[0]

    return render_template('index.html', all_friends=friends, one_friend=friends[0])

@app.route('/remove_friend/<friend_id>', methods=['POST'])
def delete(friend_id):
    query = "DELETE FROM friends WHERE id = :id"
    data = {'id': friend_id}
    mysql.query_db(query, data)
    return redirect('/')

app.run(debug=True)