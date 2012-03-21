machine_dict = (
'id', 'machine_id', 'name', 'ip', 'last_connection_to_client', 'is_busy', 'running_backup', 'running_restore',
'get_next_backup_time', 'get_last_backup_time','auto_version','current_agent_version','current_updater_version','selected_agent_version','selected_updater_version')

schedule_dict = (
    'id', 'name', 'machine_id', 'storage', 'current_day_folder_path', 'current_version_in_loop', 'versions_count',
    'get_next_backup_time', 'get_last_backup_time', 'running_backup',
    'running_restore', 'from_date', 'get_next_backup_time',
    ('folder_backups', ('id', 'local_folder_path')),
    ('sql_backups', ('id', 'type', 'host', 'port', 'database', 'username', 'password')),
    ('backups', ('id', 'time_started')))

backup_dict = ('id', 'time_started', 'day_folder_path', 'is_recoverable', ('schedule', ('id', 'name',)))

client_versions_dict = ('id','updater_link','current_agent','name','current_updater','agent_link','datetime')