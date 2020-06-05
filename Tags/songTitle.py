from Base import tools


def start(tags, json_data):
    oldTitle = json_data['title']
    # newTitle = tools.removeSiteName(oldTitle)
    newTitle = tools.removeGibberish(oldTitle)
    newTitle = newTitle.strip()

    tools.saveTags('title', newTitle, tags)
