import re
import bleach
import markdown
from .models import (
    DBSession,
    User,
)

from markdown_extensions import OEmbedExtension

amp = re.compile('&amp;')

md = markdown.Markdown(extensions=[OEmbedExtension()])


def markdown_filter(text):
    ''' Mako filter for markdown and bleach
    '''
    cleaned = bleach.clean(text, strip=True)
    parsed = md.convert(cleaned)
    return re.sub(amp, '&', parsed)


p = re.compile(ur'(@\d+)')


def convert_mentions(request):
    ''' Mako filter to convert any @id mention to link to user profile
    '''
    def d(text):
        def repl(val):
            user_id = val.group()[1:]
            user = DBSession.query(User).get(user_id)
            link = request.route_path('user', username=user.username)
            return '[@%s](%s)' % (user.username, link)

        return re.sub(p, repl, text)

    return d
