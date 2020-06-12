from Base import tools


def start(tags, json_data):

    old_composer = json_data['composer']
    new_composer = tools.removeGibberish(old_composer)
    new_composer = tools.divideBySColon(new_composer)

    new_composer = tools.removeTrailingExtras(new_composer)
    new_composer = tools.removeDup(new_composer)

    tools.saveTags('composer', new_composer, tags)
