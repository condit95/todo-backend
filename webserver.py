from flask import request, Flask
from resources import EntryManager, Entry

FOLDER = '/test'
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def hello_world_test():
    return "<p>Hello, TEST!</p>"

# list(Entry) from .json
@app.route("/api/entries/")
def get_entries() -> list:
    entry_manager = EntryManager(FOLDER)
    entry_manager.load()
    res = [i.json() for i in entry_manager.entries]
    return res

@app.route("/api/save_entries/", methods=['POST'])
def save_entries():
    # инициализируем экземпляр класса
    entry_manager = EntryManager(FOLDER)
    # получаем json из запроса list(dict)
    res_json = request.get_json()
    for i in res_json:
        # Entry из json
        post_entry = Entry.entry_from_json(i)
        entry_manager.entries.append(post_entry)
    entry_manager.save()
    return {'status': 'success'}

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)