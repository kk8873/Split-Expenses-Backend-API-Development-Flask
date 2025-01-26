from flask import Flask, request, jsonify

app = Flask(__name__)

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

expenses = []

@app.route('/group/<int:group_id>', methods=['GET'])
def get_group_details(group_id):
    for group in groups:
        if group["id"] == group_id:
            return jsonify(group)
    return jsonify({"error": "Group not found"}), 404

@app.route('/group/<int:group_id>/expenses', methods=['GET'])
def get_group_expenses(group_id):
    group_expenses = [expense for expense in expenses if expense['group_id'] == group_id]
    return jsonify(group_expenses)

@app.route('/expense', methods=['POST'])
def create_expense():
    data = request.get_json()
    amount = data.get('amount')
    description = data.get('description')
    group_id = data.get('group_id')
    paid_by = data.get('paid_by')

    if not all([amount, description, group_id, paid_by]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        amount = float(amount)
    except ValueError:
        return jsonify({'error': 'Invalid amount provided'}), 400

    group = next((g for g in groups if g['id'] == group_id), None)
    if not group:
        return jsonify({'error': 'Group not found'}), 404

    member = next((m for m in group['members'] if m['id'] == paid_by), None)
    if not member:
        return jsonify({'error': 'Member not found in this group'}), 400

    expense = {
        "id": len(expenses) + 1,
        "amount": amount,
        "description": description,
        "group_id": group_id,
        "paid_by": paid_by
    }
    expenses.append(expense)

    return jsonify({'message': 'Expense added successfully', 'expense_id': expense["id"]}), 201

if __name__ == '__main__':
    app.run(debug=True)