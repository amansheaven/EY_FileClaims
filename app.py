from flask import Flask
import app

app = Flask(__name__)` 

if __name__ == "__main__":  
    app.run(port=5000, threaded=True, debug=True, host='0.0.0.0')
