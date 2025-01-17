from flask import Flask, jsonify, request   #adding request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError #adding ValidationError
import mysql.connector
from mysql.connector import Error


app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):  
    name = fields.String(required=True)  
    age = fields.String(required=True) 
    id = fields.String(required=True)


    class Meta:
        fields = ("name", "age", "id")

class MemberUpdateSchema(ma.Schema):  
    name = fields.String(required=True)  
    age = fields.Integer(required=True) 

    class Meta:
        fields = ("name", "age")

member_schema = MemberSchema() 
members_schema = MemberSchema(many=True)  
member_update_schema = MemberUpdateSchema() 

class WorkoutSession(ma.Schema):
    member_id = fields.String(required=True)
    session_date = fields.String(required=True)
    session_time = fields.String(required=True)
    activity = fields.String(required=True)

    class Meta:
        fields = ("session_id", "member_id", "session_date", "session_time", "activity")

workout_schema = WorkoutSession()
workouts_schema = WorkoutSession(many=True)

def get_db_connection():
    """ Connect to the database and return the connection object"""
    db_name = "FITNESS_CENTER_MANAGER"
    user = "root"
    password = "amrit101!"
    host = "localhost"

    try: 
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password,
            host = host
        )

        print("Connected to MySQL database successfully")
        return conn

    except Error as e:
        print(f"Error: {e}")
        return None



@app.route('/')
def home():
    return 'Welcome to the Flask FITNESS CENTER MANAGER'  #whatever if on return statement will print on server

@app.route("/Members", methods=["GET"])
def get_members():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"Error": "Database connection failed"}), 500  #500 is internal server error, must be outside parenthesis
        cursor = conn.cursor(dictionary=True) #if connection is there,

        query = "SELECT * FROM Members"  #then here is our query

        cursor.execute(query) #executing the query

        members = cursor.fetchall() #fetching all of that data

        return members_schema.jsonify(members) #JSONifying the result

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Interal Server Errror"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/Members", methods=["POST"])   
def add_member():         
    try:
        member_data = member_schema.load(request.json) 
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400  
    
    try:
        conn = get_db_connection()
        if conn is None:  
                return jsonify({"Error": "Database connection failed"}), 500  
        cursor = conn.cursor()

        new_member = (member_data['name'], member_data['age'], member_data['id'])
        
        query = "INSERT INTO Members (name, age, id) VALUES (%s, %s, %s)"
        cursor.execute(query, new_member)
        conn.commit()

        return jsonify({"message": "New member added successfully"}), 201

    except Error as e:
        print(f"Error: {e}")

        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/Members/<int:id>", methods=["PUT"])   
def update_member(id):          
    try:
        member_data = member_update_schema.load(request.json) 
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400  
    
    try:
        conn = get_db_connection()
        if conn is None:  
                return jsonify({"Error": "Database connection failed"}), 500  
        cursor = conn.cursor()  

        updated_member = (member_data['name'], member_data['age'], id)


        query = 'UPDATE Members SET name = %s, age = %s WHERE id = %s'
        #original info pulled from customer data + new variable ID, passed in thru function

        cursor.execute(query, updated_member)
        conn.commit()

        return jsonify({"message": "Member information updated successfully"}), 201

    except Error as e:
        print(f"Error: {e}")

        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/Members/<int:id>", methods=["DELETE"])  


def delete_member(id):          
    try:
        conn = get_db_connection()
        if conn is None:  
                return jsonify({"Error": "Database connection failed"}), 500  
        cursor = conn.cursor()  

        member_to_remove = (id,)  

        cursor.execute("SELECT * FROM Members where id = %", member_to_remove)
        member = cursor.fetchone()  
        if not member:
            return jsonify({"error": "Member not found"}), 404
           
        
        query = "DELETE FROM Members WHERE id = %s"
        cursor.execute(query, member_to_remove)
        conn.commit()
        #deleting the customer

        return jsonify({"message": "Member deleted from the database successfully"}), 201

    except Error as e:
        print(f"Error: {e}")

        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

#task 3

@app.route('/WorkoutSessions', methods=['GET'])
def get_workout_sessions():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"Error": "Database connection failed."}), 500
        cursor = conn.cursor(dictionary=True)

        query = 'SELECT * FROM WorkoutSessions'
        cursor.execute(query)

        workout_sessions = cursor.fetchall()
        return workout_schema.jsonify(workout_sessions)

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/WorkoutSessions', methods=['POST'])
def add_session():
    try:
        workout_session_data = workout_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"Error": "Database connection failed."}), 500
        cursor = conn.cursor()

        new_session = (workout_session_data['member_id'], workout_session_data['session_date'], workout_session_data['session_time'], workout_session_data['activity'])

        query = 'INSERT INTO WorkoutSessions (member_id, session_date, session_time, activity) VALUES(%s,%s,%s,%s)'
        cursor.execute(query,new_session)
        conn.commit()
        return jsonify({"Message": "Workout session has successfully added to database"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/WorkoutSessions/<int:member_id>', methods=['PUT'])
def update_workout_session(member_id):
    try:
        workout_session_data = workout_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"Error": "Database connection failed."}), 500
        cursor = conn.cursor()

        updated_workout_session = (workout_session_data['session_date'], workout_session_data['session_time'], workout_session_data['activity'], member_id)

        query = 'UPDATE workoutsessions SET session_date = %s, session_time = %s, activity = %s WHERE member_id = %s'
        cursor.execute(query,updated_workout_session)
        conn.commit()
        return jsonify({"Message": "Workout session has been updated in database successfully."}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/WorkoutSessions/<int:member_id>', methods=['GET'])
def view_sessions_for_members(member_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"Error": "Database connection failed."}), 500
        cursor = conn.cursor(dictionary=True)

        member_to_display = (member_id,)

        cursor.execute('SELECT * FROM Members WHERE id = %s', member_to_display)
        member = cursor.fetchone()

        if not member:
            return jsonify({"Error": "Member ID does not exist"}), 404
        
        query = 'SELECT * FROM WorkoutSessions WHERE member_id = %s'
        cursor.execute(query, member_to_display)
        sessions = cursor.fetchall()
        return workout_schema.jsonify(sessions)
        
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__=='__main__':
    app.run(debug=True)
