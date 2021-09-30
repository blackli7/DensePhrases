import re
import json

lines = []
with open('phdefinitions.html', errors='ignore') as fin:
    for line in fin:
        lines.append(line)
temp_lines = "".join(lines)
lines = temp_lines.split("\n\n")
re_line = []
for line in lines[9:-3]:
    if line.startswith("<p>"):
        if "</a>" in line:
            continue
        line = line.replace("\n", " ")
        line = re.sub(r"(<\/?[a-z]>?)", "", line)
        re_line.append(line)

re_json = {}
re_json['data'] = []
for i in re_line:
    content = i.split(":")
    if len(content) == 2:
        if len(content[0]) > 0 and len(content[1]) > 0:
            temp_json = {}
            temp_json['title'] = content[0]
            temp_json['paragraphs'] = []
            context_json = {}
            context_json['context'] = content[0] + " is" + content[1]
            temp_json['paragraphs'].append(context_json)
            re_json['data'].append(temp_json)

re_str = json.dumps(re_json)
print(re_str)
with open('wiki_physics.json', 'w') as fout:
    fout.write(re_str)