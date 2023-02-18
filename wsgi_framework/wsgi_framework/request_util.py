def get_get_content(env):
    get_params = get_query_params(env['QUERY_STRING']) 
    return get_params

def get_post_content(env):

        content_bytes = get_post_data(env)
        post_params = get_post_params(content_bytes)
        return post_params 


def get_post_data(env) -> bytes:
    content_len_data = env['CONTENT_LENGTH']
    content_len = int(content_len_data) if content_len_data else 0
    content = env['wsgi.input'].read(content_len) if content_len > 0 else b''
    return content

def get_post_params(data) -> dict:
    result = {}
    if data:
        data_str = data.decode('utf-8')
        result = get_query_params(data_str)
    return result


def get_query_params(query_string: str) -> dict:
    result = {}
    if query_string:
        params = query_string.split('&')
        for param in params:
            key, value = param.split('=')
            result[key] = value
    return result
