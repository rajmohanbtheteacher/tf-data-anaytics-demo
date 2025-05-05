from flask import Flask, request, jsonify
import boto3
import os

app = Flask(__name__)
s3 = boto3.client('s3')
BUCKET_NAME = os.getenv("BUCKET_NAME", "my-data-pipeline-bucket")

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    key = file.filename

    try:
        s3.upload_fileobj(file, BUCKET_NAME, key)
        return jsonify({
            "message": "Upload successful",
            "bucket": BUCKET_NAME,
            "path": f"s3://{BUCKET_NAME}/{key}"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
