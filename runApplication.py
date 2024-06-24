from webtool.application import *

if __name__ == '__main__':
    init()  # initializing the database
    app.run(HOST, debug=DEBUG, port=5001)