import math

from djcelery.models import PeriodicTask

from mummyrest.apps.members.models import Member, Week
from mummyrest.apps.members.snippets import init_member_args
from mummyrest.apps.utils.snippets import get_random


def purge_schedule_tasks():
    PeriodicTask.objects.all().delete()


def find_investors(members_id, week_id, blocker):
    members = Member.objects.filter(id__in=members_id)
    current_week = Week.objects.get(id=week_id)
    potentials = 0
    new_members = list()
    members_to_leave = list()
    for member in members:
        direct_investors = Member.objects.filter(parent=member).count()
        catch_prob = member.experience * member.charisma * (1 - math.log(direct_investors))
        if member.recruit_probability < get_random():
            potentials += 1
            if catch_prob < get_random():
                new_members.append(init_member_args(Member(), member, current_week))
                member.mummy_money += 100
                direct_investors += 1
        if members.mumy_money < 500:
            weeks = current_week.id - member.start_week.id
            if weeks < member.max_weeks_without_money:
                members_to_leave.append(member.id)
    blocker.acquire()
    Member.objects.bulk_create(new_members)
    Member.objects.filter(id__in=members_to_leave).update(is_active=False)
    current_week = Week.objects.get(id=week_id)
    current_week.new_members += len(new_members)
    current_week.leave_members += len(members_to_leave)
    current_week.save()
    blocker.release()
