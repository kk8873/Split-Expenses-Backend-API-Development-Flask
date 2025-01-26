from flask import Flask, request, jsonify

app = Flask(__name__)

# Manual database for groups and expenses
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
    },
    {
        "id": 3,
        "name": "Group 3",
        "members": [
            {"id": 7, "name": "Harh"},
            {"id": 8, "name": "Karan"},
            {"id": 9, "name": "Raj"}
        ]
    }
]

expenses = []

# API endpoints

@app.route('/group/<int:group_id>/members', methods=['GET'])
def get_group_members(group_id):
    group = next((g for g in groups if g['id'] == group_id), None)
    if group:
        return jsonify(group['members'])  # Return only the members list
    return jsonify({"error": "Group not found"}), 404

@app.route('/group/<int:group_id>/balances', methods=['GET'])
def get_group_balances(group_id):
    group = next((g for g in groups if g['id'] == group_id), None)
    if not group:
        return jsonify({"error": "Group not found"}), 404

    group_members = group['members']
    num_members = len(group_members)
    if num_members == 0:
        return jsonify({"message": "Group has no members"}), 200

    balances = {member['id']: 0 for member in group_members}

    for expense in expenses:
        if expense['group_id'] == group_id:
            amount_per_member = expense['amount'] / num_members
            balances[expense['paid_by']] -= expense['amount']
            for member in group_members:
                if member['id'] != expense['paid_by']:
                    balances[member['id']] += amount_per_member

    balances_list = []
    for member_id, balance in balances.items():
        member_name = next((m['name'] for m in group_members if m['id'] == member_id), None)
        balances_list.append({"member_id": member_id, "member_name": member_name, "balance": balance})
    return jsonify(balances_list)

@app.route('/group/<int:group_id>/due_payments', methods=['GET'])
def get_due_payments(group_id):
    balances_response = get_group_balances(group_id)
    if balances_response.status_code != 200:
        return balances_response

    balances = balances_response.get_json()
    due_payments = []
    for payer in balances:
        if payer['balance'] < 0:
            for receiver in balances:
                if receiver['balance'] > 0:
                    amount_to_transfer = min(abs(payer['balance']), receiver['balance'])
                    due_payments.append({
                        "from": payer['member_name'],
                        "from_id": payer['member_id'],
                        "to": receiver['member_name'],
                        "to_id": receiver['member_id'],
                        "amount": amount_to_transfer
                    })
                    payer['balance'] += amount_to_transfer
                    receiver['balance'] -= amount_to_transfer
    return jsonify(due_payments)

@app.route('/payment', methods=['POST'])
def record_payment():
    data = request.get_json()
    from_member = data.get('from_member')
    to_member = data.get('to_member')
    amount = data.get('amount')
    group_id = data.get('group_id')

    if not from_member or not to_member or not amount or not group_id:
        return jsonify({"error": "Invalid input. Missing required fields."}), 400

    group = next((g for g in groups if g['id'] == group_id), None)
    if not group:
        return jsonify({"error": "Group not found"}), 404

    members = group['members']
    if not any(m['id'] == from_member for m in members) or not any(m['id'] == to_member for m in members):
        return jsonify({"error": "Members not found in the group"}), 400

    expenses.append({
        "group_id": group_id,
        "paid_by": from_member,
        "amount": amount
    })

    return jsonify({"message": "Payment recorded successfully."}), 201



@app.route('/expense', methods=['POST'])
def create_expense():
    data = request.get_json()
    group_id = data.get('group_id')
    paid_by = data.get('paid_by')
    amount = data.get('amount')

    if not group_id or not paid_by or not amount:
        return jsonify({"error": "Invalid input. Missing required fields."}), 400

    group = next((g for g in groups if g['id'] == group_id), None)
    if not group:
        return jsonify({"error": "Group not found"}), 404

    if not any(m['id'] == paid_by for m in group['members']):
        return jsonify({"error": "Member not found in group"}), 400

    expenses.append({
        "group_id": group_id,
        "paid_by": paid_by,
        "amount": amount
    })
    return jsonify({"message": "Expense recorded successfully."}), 201


@app.route('/group/<int:group_id>/balances', methods=['POST'])
def update_balances(group_id):
    data = request.get_json()
    balances = data.get('balances')

    group = next((g for g in groups if g['id'] == group_id), None)
    if not group:
        return jsonify({"error": "Group not found"}), 404

    if not balances:
        return jsonify({"error": "Balances data is required"}), 400

    # Update balances manually (for demonstration; should integrate with logic)
    manual_balances = {b['member_id']: b['balance'] for b in balances}
    return jsonify({"message": "Balances updated successfully.", "balances": manual_balances}), 200


@app.route('/group/<int:group_id>/due_payments', methods=['POST'])
def update_due_payments(group_id):
    data = request.get_json()
    payments = data.get('payments')

    group = next((g for g in groups if g['id'] == group_id), None)
    if not group:
        return jsonify({"error": "Group not found"}), 404

    if not payments:
        return jsonify({"error": "Payments data is required"}), 400

    # Store due payments manually (for demonstration; should integrate with logic)
    return jsonify({"message": "Due payments updated successfully.", "payments": payments}), 200


if __name__ == '__main__':
    app.run(debug=True)


# Get Group Members

# Call: GET /group/<group_id>/members
# Get Group Balances

# Call: GET /group/<group_id>/balances
# Get Due Payments

# Call: GET /group/<group_id>/due_payments
# Record a Payment

# Call: POST /payment
# {
#     "from_member": 1,
#     "to_member": 2,
#     "amount": 50.0,
#     "group_id": 1
# }


# Create an Expense
# Call: POST /expense
# {
#     "group_id": 1,
#     "paid_by": 1,
#     "amount": 150.0
# }


# Update Group Balances
# Call: POST /group/<group_id>/balances
# {
#     "balances": [
#         {"member_id": 1, "balance": -75.0},
#         {"member_id": 2, "balance": 50.0},
#         {"member_id": 3, "balance": 25.0}
#     ]
# }

# Update Due Payments
# Call: POST /group/<group_id>/due_payments
# {
#     "payments": [
#         {
#             "from": "Aliya",
#             "from_id": 1,
#             "to": "Buhan",
#             "to_id": 2,
#             "amount": 50.0
#         },
#         {
#             "from": "Aliya",
#             "from_id": 1,
#             "to": "Cheeti",
#             "to_id": 3,
#             "amount": 25.0
#         }
#     ]
# }