import logging
import os

from celery import Celery
from django import db
from django.conf import settings
from django.core.cache import cache

import multiprocessing as mp
from mummyrest.apps.members.models import Member, Week
from mummyrest.apps.simulations.snippets import find_investors
from mummyrest.apps.utils import constants as const
from mummyrest.apps.utils.snippets import chunks


logger = logging.getLogger(__name__)


if not settings.configured:

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mummyrest.config.common')

app = Celery('mummy_pyramid')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    cache.set('BLOK_DB', False, timeout=None)
    cache.set('CURRENT_WEEK', 1, timeout=None)
    time_week = os.environ.get('DEFAULT_WEEK', const.DEFAULT_WEEK)
    sender.add_periodic_task(time_week, simulate_week())


@app.task
def simulate_week():
    lock = mp.Lock()
    members_id = list(Member.objects.filter(is_active=True).exclude(
        id=const.DEFAULT_ADMIN_ID).values_list('id', flat=True))

    cpus_count = mp.cpu_count()

    chunk_members = chunks(members_id, cpus_count)

    del members_id

    current_week = cache.get('CURRENT_WEEK')

    if not current_week:
        return

    cache.set('NEW_MEMBERS', 0, timeout=None)
    cache.set('LEAVE_MEMBERS', 0, timeout=None)

    process_list = list()

    week = Week.objects.create(id=current_week)

    db.connections.close_all()

    for members in chunk_members:
        p = mp.Process(target=find_investors, args=(members, week.id, lock))
        process_list.append(p)
        p.start()

    del chunk_members

    for p in process_list:
        p.join()

    cache.set('CURRENT_WEEK', current_week + 1)
