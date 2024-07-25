import json
from flask import Flask, request, jsonify

app = Flask(__name__)

def read_employees():
    with open('./flask_app/employee.json', 'r') as file:
        data = json.load(file)
    return data

employees = read_employees()

def write_employees(employees):
    with open('./flask_app/employee.json', 'w') as file:
        data = json.dump(employees, file)
    return data

@app.route('/employees', methods=['GET'])
def get_employees():
    return employees

@app.route('/employees/fetch/<int:id>', methods=['GET'])
def get_employee_by_id(id):
    for employee in employees:
        if employee['id'] == id:
            return employee
    return 'error : Employee not found', 404

@app.post('/employees/post')
def add_employee():
    data = request.json
    if data:
        employees.append(data)
        write_employees(employees)
        return data, 201
    else:
        return 'error : No data provided', 404
    
@app.route('/employees/delete/<int:id>', methods=['DELETE'])
def delete_employee(id):
    for employee in employees:
        if employee['id'] == id:
            employees.remove(employee)
            write_employees(employees)
            return 'message: Employee deleted', 200
    return 'error : Employee not found', 404

@app.route('/employees/patch/<int:id>', methods=['PATCH'])
def patch_employee(id):
    data = request.json

    for employee in employees:
        if employee['id'] == id:
            for key, value in data.items():
                employee[key] = value
            write_employees(employees)
            return employee, 200
    return 'error : Employee not found', 404

@app.route('/employees/put', methods=['PUT'])
def put_employee():
    data = request.json
    employees = data
    write_employees(employees)
    return employees

if __name__ == '__main__':
    app.run(debug=True)

