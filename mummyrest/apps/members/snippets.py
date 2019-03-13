from mummyrest.apps.utils.snippets import get_randoms
from mummyrest.apps.utils import constants as const


def init_member_args(member, parent, week):
    values = get_randoms(3)
    member.innocence = values[0]
    member.experience = values[1]
    member.charisma = values[2]
    member.parent = parent
    member.depth = parent.depth + 1
    member.set_password(const.DEFAULT_PASWORDS)
    if parent.map_tree:
        member.map_tree = '{0}:{1}'.format(parent.map_tree, parent.id)
    else:
        member.map_tree = str(parent.id)
    member.start_week = week
    return member
