from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In-memory storage for chatrooms
chatrooms = []

@app.route('/')
def lobby():
    # Serve the lobby.html file
    return render_template('lobby.html')

@app.route('/chatrooms', methods=['GET', 'POST', 'DELETE'])
def manage_chatrooms():
    global chatrooms
    if request.method == 'GET':
        # Return the list of chatrooms
        return jsonify(chatrooms)
    elif request.method == 'POST':
        # Add a new chatroom
        data = request.json
        if len(chatrooms) >= 3:
            return jsonify({'error': 'Maximum of 3 chatrooms allowed'}), 400
        if data['name'] in chatrooms:
            return jsonify({'error': 'Chatroom name must be unique'}), 400
        chatrooms.append(data['name'])
        return jsonify({'message': 'Chatroom created'}), 201
    elif request.method == 'DELETE':
        # Delete a chatroom
        data = request.json
        chatrooms = [room for room in chatrooms if room != data['name']]
        return jsonify({'message': 'Chatroom deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)