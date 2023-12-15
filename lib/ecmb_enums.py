from enum import Enum

class ALLOWED_IMAGE_EXTENTIONS(Enum):
    JPG = 'jpg'
    JPEG = 'jpeg'
    PNG = 'png'
    WEBP = 'webp'

class BOOK_TYPE(Enum):
    MANGA = 'manga'
    COMIC = 'comic'
    

class AUTOR_TYPE(Enum):
    AUTHOR = 'author'
    COAUTHOR = 'coauthor'
    STORY = 'story'
    ILLUSTRATION = 'illustration'
    

class BASED_ON_BOOK_TYPE(Enum):
    NOVEL = 'novel'
    LIGHTNOVEL = 'lightnovel'
    MANGA = 'manga'
    COMIC = 'comic'
    ANIME = 'anime'
    GAME = 'game'
    OTHER ='other'


class CONTENT_WARNING(Enum):
    MATURE_THEMES = 'Mature Themes'
    NUDITY = 'Nudity'
    SEXUAL_CONTENT = 'Sexual Content'
    EXPLICIT_SEX = 'Explict Sex'
    HENTAI = 'Hentai'
    PROSTITUTION = 'Prostitution'
    INCEST = 'Incest'
    VIOLENCE = 'Violence'
    EXPLICIT_VIOLENCE = 'Explicit Violence'
    TERRORISM = 'Terrorism'
    EMOTIONAL_ABUSE= 'Emotional Abuse'
    SEXUAL_ABUSE = 'Sexual Abuse'
    PHYSICAL_ABUSE = 'Physical Abuse'
    DOMESTIC_ABUSE = 'Domestic Abuse'
    SELF_HARM = 'Self-Harm'
    SUICIDE = 'Suicide'
    DRUGS = 'Drugs'


class TARGET_SIDE(Enum):
    AUTO = 'auto'
    LEFT = 'left'
    RIGHT = 'right'