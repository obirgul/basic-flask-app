from flask import Flask, request
import pandas as pd

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/test')
def test():
    df = pd.DataFrame({'id': [1], 'Name': ['Orcun']})
    return df.to_json(orient='records')


@app.route('/query-example')
def query_example():
    # if key doesn't exist, returns a 400, bad request error
    description = request.args['description']
    # if key doesn't exist, returns None
    username = request.args.get('username')
    # http://127.0.0.1:5000/query-example?description=Flask&username=Python
    return '''<h1>The description value is: {}</h1>
              <h1>The username value is: {}'''.format(description, username)


# allow both GET and POST requests
@app.route('/form-example', methods=['GET', 'POST'])
def form_example():
    # handle the POST request
    if request.method == 'POST':
        username = request.form.get('username')
        description = request.form.get('description')
        return '''
                  <h1>The username value is: {}</h1>
                  <h1>The description value is: {}</h1>'''.format(username, description)

    # otherwise handle the GET request
    return '''<form method="POST">
               <div><label>Language: <input type="text" name="username"></label></div>
               <div><label>description: <input type="text" name="description"></label></div>
               <input type="submit" value="Submit"></form>'''


# GET requests will be blocked
@app.route('/json-example', methods=['POST'])
def json_example():
    request_data = request.get_json()

    username = None
    description = None
    python_version = None
    example = None
    boolean_test = None

    if request_data:
        if 'username' in request_data:
            username = request_data['username']

        if 'description' in request_data:
            description = request_data['description']

        if 'version_info' in request_data:
            if 'python' in request_data['version_info']:
                python_version = request_data['version_info']['python']

        if 'examples' in request_data:
            if (type(request_data['examples']) == list) and (len(request_data['examples']) > 0):
                example = request_data['examples'][0]

        if 'boolean_test' in request_data:
            boolean_test = request_data['boolean_test']

    return '''
           The username value is: {}
           The description value is: {}
           The Python version is: {}
           The item at index 0 in the example list is: {}
           The boolean value is: {}'''.format(username, description, python_version, example, boolean_test)


@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files['file'])
        f = request.files['file']
        data_xls = pd.read_excel(f)
        return data_xls.to_html()
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (csv, tsv, only)</h1>
    <form action="" method=post enctype=multipart/form-data>
    <p><input type=file name=file><input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run(host="localhost", debug=True)
