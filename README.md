#Split-Expenses-Backend-API-Development-Flask

![Alt text](https://github.com/kk8873/Split-Expenses-Backend-API-Development-Flask/blob/0ee280cbd68d50ce0f9f3a4b42dd80a5c3a5e156/Split%20Expenses(Backend%20Development%20)/Demo.png)
# Split Expenses - Backend API Development (Flask)

![Split Expenses Overview](https://github.com/kk8873/Split-Expenses-Backend-API-Development-Flask/blob/84e8904e7d1b821c4b696abb117dc3881c338850/Split%20Expenses(Backend%20Development%20)/Adding%20Expenses%20in%20Group.png)

This is a Flask-based backend API for managing group expenses, tracking balances, and recording payments among group members.

## Features
- Add expenses within a group
- Track group member balances
- Fetch due payments
- Record payments
- Retrieve group member information

---

## API Endpoints

### 1. Get Group Members
**Endpoint:** `GET /group/<group_id>/members`  
**Description:** Retrieves the list of members in a group.  
**Example Response:**
```json
[
    {"id": 1, "name": "Aliya"},
    {"id": 2, "name": "Buhan"},
    {"id": 3, "name": "Cheeti"}
]
```

### 2. Get Group Balances
**Endpoint:** `GET /group/<group_id>/balances`  
**Description:** Fetches the balances of all members in a group.

![Balance](https://github.com/kk8873/Split-Expenses-Backend-API-Development-Flask/blob/84e8904e7d1b821c4b696abb117dc3881c338850/Split%20Expenses(Backend%20Development%20)/Balance.png)

**Example Response:**
```json
[
    {"member_id": 1, "member_name": "Aliya", "balance": -75.0},
    {"member_id": 2, "member_name": "Buhan", "balance": 50.0},
    {"member_id": 3, "member_name": "Cheeti", "balance": 25.0}
]
```

### 3. Get Due Payments
**Endpoint:** `GET /group/<group_id>/due_payments`  
**Description:** Fetches the pending payments that members owe to each other.
**Example Response:**
```json
[
    {"from": "Aliya", "from_id": 1, "to": "Buhan", "to_id": 2, "amount": 50.0},
    {"from": "Aliya", "from_id": 1, "to": "Cheeti", "to_id": 3, "amount": 25.0}
]
```

### 4. Record a Payment
**Endpoint:** `POST /payment`  
**Description:** Records a payment between two members.
**Example Request:**
```json
{
    "from_member": 1,
    "to_member": 2,
    "amount": 50.0,
    "group_id": 1
}
```

### 5. Create an Expense
**Endpoint:** `POST /expense`  
**Description:** Adds an expense to a group.
**Example Request:**
```json
{
    "group_id": 1,
    "paid_by": 1,
    "amount": 150.0
}
```

### 6. Update Group Balances
**Endpoint:** `POST /group/<group_id>/balances`  
**Description:** Manually updates group balances.
**Example Request:**
```json
{
    "balances": [
        {"member_id": 1, "balance": -75.0},
        {"member_id": 2, "balance": 50.0},
        {"member_id": 3, "balance": 25.0}
    ]
}
```

### 7. Update Due Payments
**Endpoint:** `POST /group/<group_id>/due_payments`  
**Description:** Updates pending payments manually.
**Example Request:**
```json
{
    "payments": [
        {"from": "Aliya", "from_id": 1, "to": "Buhan", "to_id": 2, "amount": 50.0},
        {"from": "Aliya", "from_id": 1, "to": "Cheeti", "to_id": 3, "amount": 25.0}
    ]
}
```

---

## API Demonstration
Below are some additional screenshots demonstrating the API in action:

### Retrieving Group Members Info
![Group Members Info](https://github.com/kk8873/Split-Expenses-Backend-API-Development-Flask/blob/84e8904e7d1b821c4b696abb117dc3881c338850/Split%20Expenses(Backend%20Development%20)/Get%20-%20Group%20members%20info.png)

### Payment Record
![Payment Record](https://github.com/kk8873/Split-Expenses-Backend-API-Development-Flask/blob/84e8904e7d1b821c4b696abb117dc3881c338850/Split%20Expenses(Backend%20Development%20)/Payment.png)

---

## Running the Project

### Prerequisites
Ensure you have Python and Flask installed.
```bash
pip install flask
```

### Running the Server
```bash
python app.py
```

---

## Contributing
Feel free to contribute by creating a pull request or opening an issue.

---

## License
This project is licensed under the MIT License.



