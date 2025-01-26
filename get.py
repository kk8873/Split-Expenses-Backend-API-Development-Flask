## This is Milestone 1 ):
from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample in-memory data (replace with your actual data structure)
groups = [
    {
        "id": 1,
        "name": "Group 1",
        "members": [
            {"id": 1, "name": "Aliya"},
            {"id": 2, "name": "Buhan"},
            {"id": 3, "name": "Cheeti"}
        ]
    },
    {
        "id": 2,
        "name": "Group 2",
        "members": [
            {"id": 4, "name": "Divesh"},
            {"id": 5, "name": "Ajay"},
            {"id": 6, "name": "Ram"}
        ]
    }
]

@app.route('/group/<int:group_id>', methods=['GET'])
def get_group_details(group_id):
    for group in groups:
        if group["id"] == group_id:
            return jsonify(group)
    return jsonify({"error": "Group not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)