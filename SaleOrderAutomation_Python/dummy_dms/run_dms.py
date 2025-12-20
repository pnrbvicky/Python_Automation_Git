from flask import Flask, render_template, request, redirect, send_file
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin":
            return redirect("/sales-order")

    return render_template("login.html")


@app.route("/sales-order")
def sales_order():
    return render_template("sales_order.html")


@app.route("/download/sales")
def download_sales():
    file_path = os.path.join(REPORTS_DIR, "sales_order.xlsx")
    return send_file(file_path, as_attachment=True)

@app.route("/download/customer")
def download_customer():
    file_path = os.path.join(REPORTS_DIR, "customer_master.xlsx")
    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    print("Starting Dummy DMS server...")
    app.run(host="0.0.0.0", port=5000, debug=True)
