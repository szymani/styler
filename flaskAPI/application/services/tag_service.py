from application.schemas.schemas import TagSchema
from application.services import user_service
from sqlalchemy import desc
from application import db
from ..models import Tag


def addTag(name):
    newTag = Tag(name.lower)
    db.session.add(newTag)
    db.session.commit()
    return newTag


def checkAndReturnId(name):
    tagQuery = Tag.query.filter(Tag.name == name)
    if len(tagQuery.all()) > 0:
        return tagQuery.first().id
    return None


def getIdsFromString(tagsString):
    tags = str(tagsString).strip()
    tags = tags.replace(" #", "#")
    tagsArr = tags.split('#')
    tagsArr = [f'#{x.lower}' for x in tagsArr if len(x) > 0 and x[0] != '#']
    tagsIndexes = []

    for tag in tagsArr:
        id = checkAndReturnId(tag)
        if id is not None:
            tagsIndexes.append(id)
        else:
            tagsIndexes.append(addTag(tag).id)
    return tagsIndexes


def getTagsFromString(tagsString):
    tagsIds = getIdsFromString(tagsString)
    return [Tag.query.get(x) for x in tagsIds]


def getStylesWithTag(tag):
    tagsArr = Tag.query.filter(Tag.name == tag)
    if len(tagsArr.all()) > 0:
        return tagsArr.first().styles
    return []


def getPostsWithTag(tag):
    return Tag.query.filter(Tag.name == tag).first().posts
