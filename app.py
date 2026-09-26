from flask import Flask, jsonify, request, send_from_directory
import ast
import operator

app = Flask(name, static_folder="static")

Supported arithmetic operations

OPERATORS = {
ast.Add: operator.add,
ast.Sub: operator.sub,
ast.Mult: operator.mul,
ast.Div: operator.truediv,
ast.Mod: operator.mod,
ast.Pow: operator.pow,
ast.USub: operator.neg,
ast.UAdd: operator.pos,
}

def evaluate(node):
"""Safely evaluate a mathematical expression."""
if isinstance(node, ast.Constant):
if isinstance(node.value, (int, float)):
return node.value
raise ValueError("Invalid value")

if isinstance(node, ast.BinOp):
    left = evaluate(node.left)
    right = evaluate(node.right)

    operation = OPERATORS.get(type(node.op))
    if operation is None:
        raise ValueError("Unsupported operator")

    return operation(left, right)

if isinstance(node, ast.UnaryOp):
    operation = OPERATORS.get(type(node.op))
    if operation is None:
        raise ValueError("Unsupported operator")

    return operation(evaluate(node.operand))

raise ValueError("Invalid expression")


def calculate(expression):
expression = expression.strip()

if not expression:
    raise ValueError("Expression cannot be empty")

if len(expression) > 100:
    raise ValueError("Expression is too long")

tree = ast.parse(expression, mode="eval")
return evaluate(tree.body)


@app.route("/")
def index():
return send_from_directory("static", "index.html")

@app.route("/api/calculate", methods=["POST"])
def api_calculate():
data = request.get_json(silent=True) or {}
expression = data.get("expression", "")

try:
    result = calculate(expression)
    return jsonify({
        "expression": expression,
        "result": result
    })
except ZeroDivisionError:
    return jsonify({"error": "Division by zero"}), 400
except (ValueError, SyntaxError, TypeError):
    return jsonify({"error": "Invalid expression"}), 400


@app.route("/api/health", methods=["GET"])
def health():
return jsonify({"status": "ok"})

if name == "main":
app.run(host="0.0.0.0", port=5000, debug=False)