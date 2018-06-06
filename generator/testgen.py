# this needs to be reworked, but for the moment, it is working
import json


a = json.load(open('api.json'))
for tag in a['tags']:
    file = open('output/nexpose_' + str(tag['name'].lower()).replace(' ', '_') + '.py', 'w+')
    file.write("from nexpose_rest.nexpose import _GET\n")
    for b in a['paths']:
        tmp = a['paths'][b]
        if 'get' in tmp:
            tmp = tmp['get']
            if tag['name'] in tmp['tags']:
                parameter_names = []
                parameter_names_path = []
                parameter_names_get = []

                for x in tmp['parameters']:
                    if x['name'] == 'page' or x['name'] == 'size' or x['name'] == 'sort':
                        continue

                    parameter_names.append(x['name'])
                    if x['in'] == 'path':
                        parameter_names_path.append(x['name'])
                    elif x['in'] == 'query':
                        parameter_names_get.append(x['name'])
                    else:
                        raise Exception()
                file.write('\n\n')
                file.write("def " + tmp['operationId']+ '(' + ', '.join(['config'] + parameter_names) + '):' + '\n')
                path = b
                for x in parameter_names_path:
                    path = path.replace('{' + x + '}', "' + str(" +  x + ") + '")

                file.write("    getParameters=[]" + '\n')
                for x in parameter_names_get:
                    file.write("    getParameters.append('" + x + "=' + " + x + ")" + '\n')
                file.write("    code, data = _GET('" + path + "', config, getParameters=getParameters)" + '\n')
                file.write("    return data" + '\n')