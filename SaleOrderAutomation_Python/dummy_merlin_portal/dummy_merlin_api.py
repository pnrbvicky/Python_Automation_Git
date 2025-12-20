from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_sales():
    data = request.json

    if not data:
        return jsonify({
            "status": "FAILED",
            "message": "Empty payload"
        }), 400

    if not isinstance(data, list):
        return jsonify({
            "status": "FAILED",
            "message": "Payload must be a list"
        }), 400

    # Simple validation
    required_keys = {
        "merlin_order_no",
        "merlin_sku",
        "merlin_qty",
        "merlin_unit_price",
        "merlin_total_price",
        "merlin_retailer_id",
        "merlin_city"
    }

    for row in data:
        if not required_keys.issubset(row.keys()):
            return jsonify({
                "status": "FAILED",
                "message": "Missing required fields"
            }), 400

    print(f"📥 Received {len(data)} records")

    return jsonify({
        "status": "SUCCESS",
        "records_received": len(data)
    }), 200


if __name__ == "__main__":
    app.run(port=6000, debug=True)
