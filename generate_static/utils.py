def updateNestedDictByKey(obj, key, new_val):
    if key in obj: return True
    
    if isinstance(obj, dict):
        for k, v in obj.items():
            _recurseObjByKey(v, key, new_val)
    else:
        for item in obj:
            _recurseObjByKey(item, key, new_val)

def _recurseObjByKey(obj, key, new_val):
    if isinstance(obj, list) or isinstance(obj, dict):
                item = updateNestedDict(obj, key, new_val)
                if item:
                    obj[key] = new_val

def updateNestedDictByVal(obj, val, new_val):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if obj[k] == val:
                return k
            if _recurseObjByVal(v, val, new_val):
                return "FOUND_KEY"
    else:
        for item in obj:
            if _recurseObjByVal(item, val, new_val):
                return "FOUND_KEY"

def _recurseObjByVal(obj, val, new_val):
    if isinstance(obj, list) or isinstance(obj, dict):
                key = updateNestedDictByVal(obj, val, new_val)
                if key and key != "FOUND_KEY":
                    obj[key] = new_val
                    return "FOUND_KEY"
                elif key:
                    return "FOUND_KEY"



