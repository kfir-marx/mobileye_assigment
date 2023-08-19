from flask import Flask, request, jsonify
import get_songs

app = Flask(__name__)


@app.route('/get_songs', methods=['GET'])
def get_tracks():
    keyword = request.args.get('keyword')

    if not keyword:
        return jsonify({"error": "Missing 'keyword' parameter"}), 400

    songs = get_songs.get_songs()

    if not songs:
        return jsonify({"message": "No songs found with the given keyword."}), 200

    return jsonify(songs), 200


if __name__ == "__main__":
    app.run(debug=True)
