from application import create_app
import sys

app = create_app()
# Run Server
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)
   #app.run()