from Base import tools


def start(tags, json_data):

    oldArtist = json_data['artist']
    newArtist = tools.removeGibberish(oldArtist)
    newArtist = tools.divideBySColon(newArtist)

    newArtist = tools.removeTrailingExtras(newArtist)
    newArtist = tools.removeDup(newArtist)

    tools.saveTags('artist', newArtist, tags)