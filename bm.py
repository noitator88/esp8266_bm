#
# This is an example of a (sub)application, which can be made a part of
# bigger site using "app mount" feature, see example_app_router.py.
#
import picoweb, network, btree, ntptime, utime, os, gc, ujson

# get my ip address
sta_if = network.WLAN(network.STA_IF)
ipaddr, netmask, gateway, dns = sta_if.ifconfig()

# set the correct local time via ntptime
try:
    ntptime.settime()
except:
    print("Error while settime. Try latter.")
    pass
    
# free disk space
def df():
  s = os.statvfs('//')
  return ('{0} MB'.format((s[0]*s[3])/1048576))

# free memory space
def mem():
  s = gc.mem_free()
  return ('{0} KB'.format(s/1024))

# time for the key of the database
def now():
    utc_epoch         =  utime.mktime(utime.localtime())
    return "%d-%02d-%02d-%02d:%02d:%02d" % utime.localtime(utc_epoch + 28800)[:6]

_hextobyte_cache = None

def unquote(string):
    """unquote('abc%20def') -> b'abc def'."""
    global _hextobyte_cache
    
    # Note: strings are encoded as UTF-8. This is only an issue if it contains
    # unescaped non-ASCII characters, which URIs should not.
    if not string:
        return b''
    
    if isinstance(string, str):
        string = string.encode('utf-8')
    
    bits = string.split(b'%')
    if len(bits) == 1:
        return string
    
    res = [bits[0]]
    append = res.append

    # Build cache for hex to char mapping on-the-fly only for codes
    # that are actually used
    if _hextobyte_cache is None:
        _hextobyte_cache = {}
    
    for item in bits[1:]:
        try:
            code = item[:2]
            char = _hextobyte_cache.get(code)
            if char is None:
                char = _hextobyte_cache[code] = bytes([int(code, 16)])
            append(char)
            append(item[2:])
        except KeyError:
            append(b'%')
            append(item)

    return b''.join(res)


# open database file
try:
    f = open("mybm.db", "r+b")
except OSError:
    f = open("mybm.db", "w+b")
# Now open a database itself
db = btree.open(f)

app = picoweb.WebApp(None)

# for parse the string from http get
def qs_parse(qs): 
  parameters = {}
  ampersandSplit = qs.split("&")
  for element in ampersandSplit:
    equalSplit = element.split("=")
    parameters[equalSplit[0]] = equalSplit[1]
  return parameters

# /add?/url=url_to_be_stored
@app.route("/add")
def add_bm(req, resp):
    parameters = {x[0] : x[1] for x in [x.split("=") for x in req.qs[1:].split("&") ]}
    url_db = unquote(parameters["url"])
    now_db = bytes(now(), "utf-8")
    db[now_db] = url_db
    db.flush()
    url_str = str(url_db, "utf-8")    
    yield from picoweb.start_response(resp)
    yield from resp.awrite("URL to be bookmarked: " + url_str + "\n Back to <a href='/'>Home</a>.")

# /note?/note=txt_for_note
@app.route("/note")
def add_note(req, resp):
    parameters = {x[0] : x[1] for x in [x.split("=") for x in req.qs[1:].split("&") ]}
    note_db = parameters["note"]
    now_db = bytes(now(), "utf-8")
    db[now_db] = note_db
    db.flush()
    note_str = str(note_db, "utf-8")    
    yield from picoweb.start_response(resp)
    yield from resp.awrite("Notes has been bookmarked: " + note_str + "\n Back to <a href='/'>Home</a>.")
    
# /del?/key=key_of_url_to_be_del
@app.route("/del")
def del_bm(req, resp):
    parameters = {x[0] : x[1] for x in [x.split("=") for x in req.qs[1:].split("&") ]}
    key_db = bytes(parameters["key"], "utf-8")
    url_str = str(db[key_db], "utf-8")
    del db[key_db]
    db.flush()    
    yield from picoweb.start_response(resp)
    yield from resp.awrite("URL has been deleted: " + url_str + "\n Back to <a href='/'>Home</a>.")

# /query?/key=key_of_url_to_be_del returns bm in json format
@app.route("/query")
def query_json_bm(req, resp):
    parameters = {x[0] : x[1] for x in [x.split("=") for x in req.qs[1:].split("&") ]}
    key_db = bytes(parameters["key"], "utf-8")
    url_db = db[key_db]
    json_db = {key_db:url_db}
    yield from picoweb.jsonify(resp, json_db)

# /list   list all keys in db
@app.route("/list")
def query_json_list(req, resp):
    i = 0
    dict_i = {}
    for key in db:
        i = i + 1
        key_str = str(key, "utf-8")
        i_str = str(i)
        dict_i[i_str] = key_str
    yield from picoweb.jsonify(resp, dict_i)
    
# # test picoweb parser
# @app.route("/test")
# def test_parse(req,resp):
#   parameters = {x[0] : x[1] for x in [x.split("=") for x in req.qs[1:].split("&") ]}
#   for par in parameters:
#       print(par)
#       print(unquote(parameters[par]))
# #  yield from picoweb.jsonify(res,dict)
#   yield from picoweb.start_response(resp)
#   yield from resp.awrite("Tested")
  
@app.route("/")
def index(req, resp):
    gc.collect()
    free_flash_mb = df()
    esp_tim = now()
    free_mem_kb = mem()
    yield from picoweb.start_response(resp)
    yield from app.render_template(resp, "index.tpl", (free_flash_mb, free_mem_kb, esp_tim, db,))

@app.route("/ntp")
def index(req, resp):
    yield from picoweb.start_response(resp)    
    try:
        ntptime.settime()
        yield from resp.awrite("ntp time synced")
    except: 
        yield from resp.awrite("ntp time error")

import ulogging as logging
logging.basicConfig(level=logging.INFO)

#if __name__ == "__main__":
#    app.run(debug=True, host = "192.168.50.217")
app.run(debug=True, host = ipaddr)

