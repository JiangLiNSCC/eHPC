# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Tianhe2CJobTable(models.Model):
    job_db_inx = models.IntegerField(primary_key=True)
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    account = models.TextField(blank=True)
    cpus_req = models.IntegerField()
    cpus_alloc = models.IntegerField()
    derived_ec = models.IntegerField()
    derived_es = models.TextField(blank=True)
    exit_code = models.IntegerField()
    job_name = models.TextField()
    id_assoc = models.IntegerField()
    id_block = models.TextField(blank=True)
    id_job = models.IntegerField()
    id_qos = models.IntegerField()
    id_resv = models.IntegerField()
    id_wckey = models.IntegerField()
    id_user = models.IntegerField()
    id_group = models.IntegerField()
    kill_requid = models.IntegerField()
    mem_req = models.IntegerField()
    nodelist = models.TextField(blank=True)
    nodes_alloc = models.IntegerField()
    node_inx = models.TextField(blank=True)
    partition = models.TextField()
    priority = models.IntegerField()
    state = models.IntegerField()
    timelimit = models.IntegerField()
    time_submit = models.IntegerField()
    time_eligible = models.IntegerField()
    time_start = models.IntegerField()
    time_end = models.IntegerField()
    time_suspended = models.IntegerField()
    gres_req = models.TextField()
    gres_alloc = models.TextField()
    gres_used = models.TextField()
    wckey = models.TextField()
    track_steps = models.IntegerField()
    class Meta:
        db_table = 'tianhe2-c_job_table'


