from flask import Flask, jsonify, request
from collections import defaultdict
import unittest

app = Flask(__name__)

class Group:
    """Represents a group of friends and their expenses."""

    def __init__(self, group_id, name, members):
        self.id = group_id
        self.name = name
        self.members = members
        self.expenses = []
        self.settlements = []

    def add_expense(self, expense):
        self.expenses.append(expense)
        self.calculate_balances()

    def add_settlement(self, settlement):
        self.settlements.append(settlement)
        self.calculate_balances()

    def calculate_balances(self):
        """Calculates and updates member balances based on expenses and settlements."""
        balances = defaultdict(float)  # Use float for accurate calculations

        for expense in self.expenses:
            paid_by = expense['paid_by']
            amount = expense['amount']
            split_between = expense.get('split_between', []) #Handle case where split_between is empty
            split_count = len(split_between)
            if split_count > 0:
                amount_per_person = amount / split_count
                balances[paid_by] -= amount
                for member_id in split_between:
                    balances[member_id] += amount_per_person

        for settlement in self.settlements:
            payer_id = settlement['payer_id']
            payee_id = settlement['payee_id']
            amount = settlement['amount']
            balances[payer_id] -= amount
            balances[payee_id] += amount

        for member in self.members:
            member['balance'] = balances[member['id']]

# Sample in-memory data (replace with a database in a real application)
groups = []  # Start with an empty list of groups

def find_group(group_id):
    for group in groups:
        if group.id == group_id:
            return group
    return None

@app.route('/group/<int:group_id>', methods=['GET'])
def get_group_details(group_id):
    group = find_group(group_id)
    if group is None:
        return jsonify({"error": "Group not found"}), 404
    return jsonify(group.__dict__)

@app.route('/group', methods=['POST'])
def create_group():
    new_group_data = request.get_json()
    if not new_group_data or 'name' not in new_group_data or 'members' not in new_group_data:
        return jsonify({"error": "Invalid group data"}), 400
    new_group = Group(len(groups) + 1, new_group_data['name'], new_group_data['members'])
    groups.append(new_group)
    return jsonify(new_group.__dict__), 201

@app.route('/group/<int:group_id>/expense', methods=['POST'])
def add_expense(group_id):
    group = find_group(group_id)
    if group is None:
        return jsonify({"error": "Group not found"}), 404

    expense = request.get_json()
    if not expense or 'amount' not in expense or 'paid_by' not in expense or 'split_between' not in expense:
        return jsonify({"error": "Invalid expense data"}), 400
    group.add_expense(expense)
    return jsonify({"message": "Expense added successfully"}), 201

@app.route('/group/<int:group_id>/settle', methods=['POST'])
def settle_dues(group_id):
    group = find_group(group_id)
    if group is None:
        return jsonify({"error": "Group not found"}), 404

    settlement = request.get_json()
    if not settlement or 'payer_id' not in settlement or 'payee_id' not in settlement or 'amount' not in settlement:
        return jsonify({"error": "Invalid settlement data"}), 400

    payer_id = settlement['payer_id']
    payee_id = settlement['payee_id']

    if not any(member['id'] == payer_id for member in group.members) or \
       not any(member['id'] == payee_id for member in group.members):
        return jsonify({"error": "Invalid payer or payee"}), 400

    group.add_settlement(settlement)
    return jsonify({"message": "Settlement recorded successfully"})

@app.route('/group/<int:group_id>/balance', methods=['GET'])
def get_group_balance(group_id):
    group = find_group(group_id)
    if group is None:
        return jsonify({"error": "Group not found"}), 404

    group.calculate_balances() # Ensure balances are up to date.
    return jsonify([
        {"member_id": member['id'], "name": member['name'], "balance": member['balance']}
        for member in group.members
    ])

class TestExpenseSplittingAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        # Create a test group for all tests
        response = cls.app.post('/group', json={
            "name": "Test Group",
            "members": [
                {"id": 1, "name": "User1"},
                {"id": 2, "name": "User2"},
                {"id": 3, "name": "User3"}
            ]
        })
        cls.group_id = response.get_json()['id']

    def test_add_expense_and_get_balance(self):
        response = self.app.post(f'/group/{self.group_id}/expense', json={
            "amount": 90,
            "paid_by": 1,
            "split_between": [2, 3]
        })
        self.assertEqual(response.status_code, 201)

        response = self.app.get(f'/group/{self.group_id}/balance')
        self.assertEqual(response.status_code, 200)
        balances = response.get_json()
        self.assertEqual(balances[0]['balance'], -90.0)
        self.assertEqual(balances[1]['balance'], 45.0)
        self.assertEqual(balances[2]['balance'], 45.0)

    def test_settle_dues(self):
        response = self.app.post(f'/group/{self.group_id}/settle', json={
            "payer_id": 2,
            "payee_id": 1,
            "amount": 30
        })
        self.assertEqual(response.status_code, 200)

        response = self.app.get(f'/group/{self.group_id}/balance')
        self.assertEqual(response.status_code, 200)
        balances = response.get_json()
        self.assertEqual(balances[0]['balance'], -60.0)
        self.assertEqual(balances[1]['balance'], 15.0)
        self.assertEqual(balances[2]['balance'], 45.0)

if __name__ == '__main__':
    unittest.main()
    app.run(debug=True)