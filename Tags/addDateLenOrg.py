from Base import tools


def addTag(tags, json_data, tag_name):
    new_org = json_data[tag_name]
    tools.saveTags(tag_name, new_org, tags)


def start(tags, json_data):
    addTag(tags, json_data, 'organization')
    addTag(tags, json_data, 'length')
    addTag(tags, json_data, 'date')
