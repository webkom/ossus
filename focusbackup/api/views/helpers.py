# -*- coding: utf-8 -*-
from django.conf import settings


def build_sql_backup(sql_backups):
    send_object = []
    for sql_backup in sql_backups:
        send_object.append(
            {
                'id': sql_backup.id,
                'host': sql_backup.host,
                'username': sql_backup.username,
                'password': sql_backup.password,
                'database': sql_backup.database,
                'type': sql_backup.type,
                'port': sql_backup.port
            }
        )
    return send_object


def build_folder_backup(folder_backups):
    send_object = []
    for folder_backup in folder_backups:
        send_object.append(
            {
                'id': folder_backup.id,
                'local_folder_path': folder_backup.local_folder_path,
            }
        )
    return send_object


def build_machine_log_fields(machine_log):
    return {
        'id': machine_log.id,
        'datetime': machine_log.datetime,
        'text': machine_log.text,
        'type': machine_log.type,
    }


def build_machine_log(machine_logs):
    send_object = []
    for machine_log in machine_logs:
        send_object.append(
            build_machine_log_fields(machine_log)
        )

    return send_object


def build_client_version(obj):
    if obj is None:
        return {}

    agent = {}
    updater = {}
    agent_link = ""
    updater_link = ""

    if obj.agent:
        agent = {'name': obj.agent.name}
        agent_link = settings.URL_TO_SITE + "uploads/" + obj.agent.name

    if obj.updater:
        updater = {'name': obj.updater.name}
        updater_link = settings.URL_TO_SITE + "uploads/" + obj.updater.name

    return {
        'id': obj.id,
        'datetime': obj.datetime,
        'name': obj.name,
        'agent': agent,
        'agent_link': agent_link,
        'updater_link': updater_link,
        'updater': updater,
        'current_agent': obj.current_agent,
        'current_updater': obj.current_updater,
    }


def build_backup_fields(backup):
    return {
        'id': backup.id,
        'machine': {
            'id': backup.machine.id,
            'name': backup.machine.name,
        },
        'schedule': {
            'id': backup.schedule.id,
            'name': backup.schedule.name,
        },
        'time_started': backup.time_started,
        'time_ended': backup.time_ended,
        'day_folder_path': backup.day_folder_path,
    }


def build_schedule_fields(schedule):
    return {
        'id': schedule.id,
        'name': schedule.name,
        'current_version_in_loop': schedule.current_version_in_loop,
        'versions_count': schedule.versions_count,
        'get_next_backup_time': schedule.get_next_run_time().strftime("%Y-%m-%d %H:%M:%S"),
        'storage': {
            'id': schedule.storage.id,
            'host': schedule.storage.host,
            'username': schedule.storage.username,
            'password': schedule.storage.password,
            'folder': schedule.storage.folder,
            'current_day_folder_path': schedule.current_day_folder_path(),
        },
        'running_backup': schedule.running_backup,
        'running_restore': schedule.running_restore,

        'sql_backups': build_sql_backup(schedule.sql_backups.all()),
        'folder_backups': build_folder_backup(schedule.folders.all())
    }


def build_machine_fields(machine):
    current_agent_version = machine.current_agent_version
    selected_agent_version = machine.get_selected_agent_version()
    current_updater_version = machine.current_updater_version
    selected_updater_version = machine.get_selected_updater_version()

    return {
        'id': machine.id,
        'name': machine.name,
        'is_busy': machine.is_busy(),
        'active': machine.active,
        'external_ip': machine.external_ip,
        'run_install': machine.run_install,
        'auto_update': machine.auto_version,
        'current_agent_version': build_client_version(current_agent_version),
        'current_updater_version': build_client_version(current_updater_version),
        'selected_agent_version': build_client_version(selected_agent_version),
        'selected_updater_version': build_client_version(selected_updater_version),
    }


def build_machine_settings(request, machine):
    return {
        'agent_folder': "%s" % machine.agent_folder,
        'local_temp_folder': "%s" % machine.local_temp_folder,
        'id': "%s" % machine.id,
        'api_user': "%s" % request.user.id,
        'api_token': "%s" % request.user.profile.get_token().api_token,
        'server_ip': settings.URL_TO_SITE,
        'force_action': '0',
        'mysql_dump': "%s" % machine.mysql_dump,
    }