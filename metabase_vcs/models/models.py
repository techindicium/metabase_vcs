# coding: utf-8
from sqlathanor import declarative_base, Column, relationship
from sqlalchemy import BigInteger, Boolean, CHAR, DateTime, ForeignKey, ForeignKeyConstraint, Index, Integer, LargeBinary, Numeric, SmallInteger, String, Table, Text, UniqueConstraint, text

BaseModel = declarative_base()
metadata = BaseModel.metadata


class CoreUser(BaseModel):
    __tablename__ = 'core_user'

    id = Column(Integer, primary_key=True, server_default=text("nextval('core_user_id_seq'::regclass)"), supports_json=True)
    email = Column(String(254), nullable=False, unique=True, supports_json=True)
    first_name = Column(String(254), nullable=False, supports_json=True)
    last_name = Column(String(254), nullable=False, supports_json=True)
    password = Column(String(254), nullable=False, supports_json=True)
    password_salt = Column(String(254), nullable=False, server_default=text("'default'::character varying"), supports_json=True)
    date_joined = Column(DateTime(True), nullable=False, supports_json=True)
    last_login = Column(DateTime(True), supports_json=False)
    is_superuser = Column(Boolean, nullable=False, supports_json=True)
    is_active = Column(Boolean, nullable=False, supports_json=True)
    reset_token = Column(String(254), supports_json=True)
    reset_triggered = Column(BigInteger, supports_json=True)
    is_qbnewb = Column(Boolean, nullable=False, server_default=text("true"), supports_json=True)
    google_auth = Column(Boolean, nullable=False, server_default=text("false"), supports_json=True)
    ldap_auth = Column(Boolean, nullable=False, server_default=text("false"), supports_json=True)
    login_attributes = Column(Text, comment='JSON serialized map with attributes used for row level permissions', supports_json=True)
    updated_at = Column(DateTime, comment='When was this User last updated?', supports_json=False)


class DataMigration(BaseModel):
    __tablename__ = 'data_migrations'

    id = Column(String(254), primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)


t_databasechangelog = Table(
    'databasechangelog', metadata,
    Column('id', String(255), nullable=False),
    Column('author', String(255), nullable=False),
    Column('filename', String(255), nullable=False),
    Column('dateexecuted', DateTime, nullable=False),
    Column('orderexecuted', Integer, nullable=False),
    Column('exectype', String(10), nullable=False),
    Column('md5sum', String(35)),
    Column('description', String(255)),
    Column('comments', String(255)),
    Column('tag', String(255)),
    Column('liquibase', String(20)),
    Column('contexts', String(255)),
    Column('labels', String(255)),
    Column('deployment_id', String(10)),
    UniqueConstraint('id', 'author', 'filename')
)


class Databasechangeloglock(BaseModel):
    __tablename__ = 'databasechangeloglock'

    id = Column(Integer, primary_key=True)
    locked = Column(Boolean, nullable=False)
    lockgranted = Column(DateTime)
    lockedby = Column(String(255))


class Dependency(BaseModel):
    __tablename__ = 'dependency'

    id = Column(Integer, primary_key=True, server_default=text("nextval('dependency_id_seq'::regclass)"))
    model = Column(String(32), nullable=False, index=True)
    model_id = Column(Integer, nullable=False, index=True)
    dependent_on_model = Column(String(32), nullable=False, index=True)
    dependent_on_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(True), nullable=False)


class Label(BaseModel):
    __tablename__ = 'label'

    id = Column(Integer, primary_key=True, server_default=text("nextval('label_id_seq'::regclass)"))
    name = Column(String(254), nullable=False)
    slug = Column(String(254), nullable=False, unique=True)
    icon = Column(String(128))


class MetabaseDatabase(BaseModel):
    __tablename__ = 'metabase_database'

    id = Column(Integer, primary_key=True, server_default=text("nextval('metabase_database_id_seq'::regclass)"), supports_json=True)
    created_at = Column(DateTime(True), nullable=False, supports_json=True)
    updated_at = Column(DateTime(True), nullable=False, supports_json=True)
    name = Column(String(254), nullable=False, supports_json=True)
    description = Column(Text, supports_json=True)
    details = Column(Text, supports_json=False) # metabase shows the password here, so no details.
    engine = Column(String(254), nullable=False, supports_json=True)
    is_sample = Column(Boolean, nullable=False, server_default=text("false"), supports_json=True)
    is_full_sync = Column(Boolean, nullable=False, server_default=text("true"), supports_json=True)
    points_of_interest = Column(Text, supports_json=True)
    caveats = Column(Text, supports_json=True)
    metadata_sync_schedule = Column(String(254), nullable=False, server_default=text("'0 50 * * * ? *'::character varying"), comment='The cron schedule string for when this database should undergo the metadata sync process (and analysis for new fields).', supports_json=False)
    cache_field_values_schedule = Column(String(254), nullable=False, server_default=text("'0 50 0 * * ? *'::character varying"), comment='The cron schedule string for when FieldValues for eligible Fields should be updated.', supports_json=True)
    timezone = Column(String(254), comment='Timezone identifier for the database, set by the sync process', supports_json=True)
    is_on_demand = Column(Boolean, nullable=False, server_default=text("false"), comment='Whether we should do On-Demand caching of FieldValues for this DB. This means FieldValues are updated when their Field is used in a Dashboard or Card param.', supports_json=True)
    options = Column(Text, comment='Serialized JSON containing various options like QB behavior.', supports_json=True)
    auto_run_queries = Column(Boolean, nullable=False, server_default=text("true"), comment='Whether to automatically run queries when doing simple filtering and summarizing in the Query Builder.', supports_json=True)


class PermissionsGroup(BaseModel):
    __tablename__ = 'permissions_group'

    id = Column(Integer, primary_key=True, server_default=text("nextval('permissions_group_id_seq'::regclass)"))
    name = Column(String(255), nullable=False, unique=True)


class QrtzCalendar(BaseModel):
    __tablename__ = 'qrtz_calendars'
    __table_args__ = {'comment': 'Used for Quartz scheduler.'}

    sched_name = Column(String(120), primary_key=True, nullable=False)
    calendar_name = Column(String(200), primary_key=True, nullable=False)
    calendar = Column(LargeBinary, nullable=False)


class QrtzFiredTrigger(BaseModel):
    __tablename__ = 'qrtz_fired_triggers'
    __table_args__ = (
        Index('idx_qrtz_ft_j_g', 'sched_name', 'job_name', 'job_group'),
        Index('idx_qrtz_ft_tg', 'sched_name', 'trigger_group'),
        Index('idx_qrtz_ft_t_g', 'sched_name', 'trigger_name', 'trigger_group'),
        Index('idx_qrtz_ft_inst_job_req_rcvry', 'sched_name', 'instance_name', 'requests_recovery'),
        Index('idx_qrtz_ft_trig_inst_name', 'sched_name', 'instance_name'),
        Index('idx_qrtz_ft_jg', 'sched_name', 'job_group'),
        {'comment': 'Used for Quartz scheduler.'}
    )

    sched_name = Column(String(120), primary_key=True, nullable=False)
    entry_id = Column(String(95), primary_key=True, nullable=False)
    trigger_name = Column(String(200), nullable=False)
    trigger_group = Column(String(200), nullable=False)
    instance_name = Column(String(200), nullable=False)
    fired_time = Column(BigInteger, nullable=False)
    sched_time = Column(BigInteger)
    priority = Column(Integer, nullable=False)
    state = Column(String(16), nullable=False)
    job_name = Column(String(200))
    job_group = Column(String(200))
    is_nonconcurrent = Column(Boolean)
    requests_recovery = Column(Boolean)


class QrtzJobDetail(BaseModel):
    __tablename__ = 'qrtz_job_details'
    __table_args__ = (
        Index('idx_qrtz_j_grp', 'sched_name', 'job_group'),
        Index('idx_qrtz_j_req_recovery', 'sched_name', 'requests_recovery'),
        {'comment': 'Used for Quartz scheduler.'}
    )

    sched_name = Column(String(120), primary_key=True, nullable=False)
    job_name = Column(String(200), primary_key=True, nullable=False)
    job_group = Column(String(200), primary_key=True, nullable=False)
    description = Column(String(250))
    job_class_name = Column(String(250), nullable=False)
    is_durable = Column(Boolean, nullable=False)
    is_nonconcurrent = Column(Boolean, nullable=False)
    is_update_data = Column(Boolean, nullable=False)
    requests_recovery = Column(Boolean, nullable=False)
    job_data = Column(LargeBinary)


class QrtzLock(BaseModel):
    __tablename__ = 'qrtz_locks'
    __table_args__ = {'comment': 'Used for Quartz scheduler.'}

    sched_name = Column(String(120), primary_key=True, nullable=False)
    lock_name = Column(String(40), primary_key=True, nullable=False)


class QrtzPausedTriggerGrp(BaseModel):
    __tablename__ = 'qrtz_paused_trigger_grps'
    __table_args__ = {'comment': 'Used for Quartz scheduler.'}

    sched_name = Column(String(120), primary_key=True, nullable=False)
    trigger_group = Column(String(200), primary_key=True, nullable=False)


class QrtzSchedulerState(BaseModel):
    __tablename__ = 'qrtz_scheduler_state'
    __table_args__ = {'comment': 'Used for Quartz scheduler.'}

    sched_name = Column(String(120), primary_key=True, nullable=False)
    instance_name = Column(String(200), primary_key=True, nullable=False)
    last_checkin_time = Column(BigInteger, nullable=False)
    checkin_interval = Column(BigInteger, nullable=False)


class Query(BaseModel):
    __tablename__ = 'query'
    __table_args__ = {'comment': 'Information (such as average execution time) for different queries that have been previously ran.'}

    query_hash = Column(LargeBinary, primary_key=True, comment='The hash of the query dictionary. (This is a 256-bit SHA3 hash of the query dict.)')
    average_execution_time = Column(Integer, nullable=False, comment='Average execution time for the query, round to nearest number of milliseconds. This is updated as a rolling average.')
    query = Column(Text, comment='The actual "query dictionary" for this query.')


class QueryCache(BaseModel):
    __tablename__ = 'query_cache'
    __table_args__ = {'comment': 'Cached results of queries are stored here when using the DB-based query cache.'}

    query_hash = Column(LargeBinary, primary_key=True, comment='The hash of the query dictionary. (This is a 256-bit SHA3 hash of the query dict).')
    updated_at = Column(DateTime(True), nullable=False, index=True, comment='The timestamp of when these query results were last refreshed.')
    results = Column(LargeBinary, nullable=False, comment='Cached, compressed results of running the query with the given hash.')


class QueryExecution(BaseModel):
    __tablename__ = 'query_execution'
    __table_args__ = {'comment': 'A log of executed queries, used for calculating historic execution times, auditing, and other purposes.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('query_execution_id_seq'::regclass)"))
    hash = Column(LargeBinary, nullable=False, comment='The hash of the query dictionary. This is a 256-bit SHA3 hash of the query.')
    started_at = Column(DateTime, nullable=False, index=True, comment='Timestamp of when this query started running.')
    running_time = Column(Integer, nullable=False, comment='The time, in milliseconds, this query took to complete.')
    result_rows = Column(Integer, nullable=False, comment='Number of rows in the query results.')
    native = Column(Boolean, nullable=False, comment='Whether the query was a native query, as opposed to an MBQL one (e.g., created with the GUI).')
    context = Column(String(32), comment='Short string specifying how this query was executed, e.g. in a Dashboard or Pulse.')
    error = Column(Text, comment='Error message returned by failed query, if any.')
    executor_id = Column(Integer, comment='The ID of the User who triggered this query execution, if any.')
    card_id = Column(Integer, comment='The ID of the Card (Question) associated with this query execution, if any.')
    dashboard_id = Column(Integer, comment='The ID of the Dashboard associated with this query execution, if any.')
    pulse_id = Column(Integer, comment='The ID of the Pulse associated with this query execution, if any.')
    database_id = Column(Integer, comment='ID of the database this query was ran against.')


class Setting(BaseModel):
    __tablename__ = 'setting'

    key = Column(String(254), primary_key=True)
    value = Column(Text, nullable=False)


class TaskHistory(BaseModel):
    __tablename__ = 'task_history'
    __table_args__ = {'comment': 'Timing and metadata info about background/quartz processes'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('task_history_id_seq'::regclass)"))
    task = Column(String(254), nullable=False, comment='Name of the task')
    db_id = Column(Integer, index=True)
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=False, index=True)
    duration = Column(Integer, nullable=False)
    task_details = Column(Text, comment='JSON string with additional info on the task')


class Activity(BaseModel):
    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True, server_default=text("nextval('activity_id_seq'::regclass)"))
    topic = Column(String(32), nullable=False)
    timestamp = Column(DateTime(True), nullable=False, index=True)
    user_id = Column(ForeignKey('core_user.id', deferrable=True), index=True)
    model = Column(String(16))
    model_id = Column(Integer)
    database_id = Column(Integer)
    table_id = Column(Integer)
    custom_id = Column(String(48), index=True)
    details = Column(String, nullable=False)

    user = relationship('CoreUser')


class Collection(BaseModel):
    __tablename__ = 'collection'
    __table_args__ = {'comment': 'Collections are an optional way to organize Cards and handle permissions for them.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('collection_id_seq'::regclass)"), supports_json=True)
    name = Column(Text, nullable=False, comment='The user-facing name of this Collection.', supports_json=True)
    description = Column(Text, comment='Optional description for this Collection.', supports_json=True)
    color = Column(CHAR(7), nullable=False, comment='Seven-character hex color for this Collection, including the preceding hash sign.', supports_json=True)
    archived = Column(Boolean, nullable=False, server_default=text("false"), comment='Whether this Collection has been archived and should be hidden from users.', supports_json=True)
    location = Column(String(254), nullable=False, index=True, server_default=text("'/'::character varying"), comment='Directory-structure path of ancestor Collections. e.g. "/1/2/" means our Parent is Collection 2, and their parent is Collection 1.', supports_json=True)
    personal_owner_id = Column(ForeignKey('core_user.id', deferrable=True), unique=True, comment='If set, this Collection is a personal Collection, for exclusive use of the User with this ID.', supports_json=True)
    slug = Column(String(254), nullable=False, comment='Sluggified version of the Collection name. Used only for display purposes in URL; not unique or indexed.', supports_json=True)

    personal_owner = relationship('CoreUser', uselist=False)


class CollectionRevision(BaseModel):
    __tablename__ = 'collection_revision'
    __table_args__ = {'comment': 'Used to keep track of changes made to collections.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('collection_revision_id_seq'::regclass)"))
    before = Column(Text, nullable=False, comment='Serialized JSON of the collections graph before the changes.')
    after = Column(Text, nullable=False, comment='Serialized JSON of the collections graph after the changes.')
    user_id = Column(ForeignKey('core_user.id', deferrable=True), nullable=False, comment='The ID of the admin who made this set of changes.')
    created_at = Column(DateTime, nullable=False, comment='The timestamp of when these changes were made.')
    remark = Column(Text, comment='Optional remarks explaining why these changes were made.')

    user = relationship('CoreUser')


class ComputationJob(BaseModel):
    __tablename__ = 'computation_job'
    __table_args__ = {'comment': 'Stores submitted async computation jobs.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('computation_job_id_seq'::regclass)"))
    creator_id = Column(ForeignKey('core_user.id', deferrable=True))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    type = Column(String(254), nullable=False)
    status = Column(String(254), nullable=False)
    context = Column(Text)
    ended_at = Column(DateTime)

    creator = relationship('CoreUser')


class CoreSession(BaseModel):
    __tablename__ = 'core_session'

    id = Column(String(254), primary_key=True)
    user_id = Column(ForeignKey('core_user.id', deferrable=True), nullable=False)
    created_at = Column(DateTime(True), nullable=False)

    user = relationship('CoreUser')



class Permission(BaseModel):
    __tablename__ = 'permissions'
    __table_args__ = (
        UniqueConstraint('group_id', 'object'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('permissions_id_seq'::regclass)"))
    object = Column(String(254), nullable=False, index=True)
    group_id = Column(ForeignKey('permissions_group.id', deferrable=True), nullable=False, index=True)

    group = relationship('PermissionsGroup')


class PermissionsGroupMembership(BaseModel):
    __tablename__ = 'permissions_group_membership'
    __table_args__ = (
        UniqueConstraint('user_id', 'group_id'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('permissions_group_membership_id_seq'::regclass)"))
    user_id = Column(ForeignKey('core_user.id', deferrable=True), nullable=False, index=True)
    group_id = Column(ForeignKey('permissions_group.id', deferrable=True), nullable=False, index=True)

    group = relationship('PermissionsGroup')
    user = relationship('CoreUser')


class PermissionsRevision(BaseModel):
    __tablename__ = 'permissions_revision'
    __table_args__ = {'comment': 'Used to keep track of changes made to permissions.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('permissions_revision_id_seq'::regclass)"))
    before = Column(Text, nullable=False, comment='Serialized JSON of the permissions before the changes.')
    after = Column(Text, nullable=False, comment='Serialized JSON of the permissions after the changes.')
    user_id = Column(ForeignKey('core_user.id', deferrable=True), nullable=False, comment='The ID of the admin who made this set of changes.')
    created_at = Column(DateTime, nullable=False, comment='The timestamp of when these changes were made.')
    remark = Column(Text, comment='Optional remarks explaining why these changes were made.')

    user = relationship('CoreUser')


class QrtzTrigger(BaseModel):
    __tablename__ = 'qrtz_triggers'
    __table_args__ = (
        ForeignKeyConstraint(['sched_name', 'job_name', 'job_group'], ['qrtz_job_details.sched_name', 'qrtz_job_details.job_name', 'qrtz_job_details.job_group'], deferrable=True),
        Index('idx_qrtz_t_nft_st_misfire', 'sched_name', 'misfire_instr', 'next_fire_time', 'trigger_state'),
        Index('idx_qrtz_t_n_g_state', 'sched_name', 'trigger_group', 'trigger_state'),
        Index('idx_qrtz_t_n_state', 'sched_name', 'trigger_name', 'trigger_group', 'trigger_state'),
        Index('idx_qrtz_t_g', 'sched_name', 'trigger_group'),
        Index('idx_qrtz_t_nft_st_misfire_grp', 'sched_name', 'misfire_instr', 'next_fire_time', 'trigger_group', 'trigger_state'),
        Index('idx_qrtz_t_j', 'sched_name', 'job_name', 'job_group'),
        Index('idx_qrtz_t_next_fire_time', 'sched_name', 'next_fire_time'),
        Index('idx_qrtz_t_c', 'sched_name', 'calendar_name'),
        Index('idx_qrtz_t_state', 'sched_name', 'trigger_state'),
        Index('idx_qrtz_t_nft_misfire', 'sched_name', 'misfire_instr', 'next_fire_time'),
        Index('idx_qrtz_t_nft_st', 'sched_name', 'trigger_state', 'next_fire_time'),
        Index('idx_qrtz_t_jg', 'sched_name', 'job_group'),
        {'comment': 'Used for Quartz scheduler.'}
    )

    sched_name = Column(String(120), primary_key=True, nullable=False)
    trigger_name = Column(String(200), primary_key=True, nullable=False)
    trigger_group = Column(String(200), primary_key=True, nullable=False)
    job_name = Column(String(200), nullable=False)
    job_group = Column(String(200), nullable=False)
    description = Column(String(250))
    next_fire_time = Column(BigInteger)
    prev_fire_time = Column(BigInteger)
    priority = Column(Integer)
    trigger_state = Column(String(16), nullable=False)
    trigger_type = Column(String(8), nullable=False)
    start_time = Column(BigInteger, nullable=False)
    end_time = Column(BigInteger)
    calendar_name = Column(String(200))
    misfire_instr = Column(SmallInteger)
    job_data = Column(LargeBinary)

    qrtz_job_detail = relationship('QrtzJobDetail')


class QrtzBlobTrigger(QrtzTrigger):
    __tablename__ = 'qrtz_blob_triggers'
    __table_args__ = (
        ForeignKeyConstraint(['sched_name', 'trigger_name', 'trigger_group'], ['qrtz_triggers.sched_name', 'qrtz_triggers.trigger_name', 'qrtz_triggers.trigger_group'], deferrable=True),
        {'comment': 'Used for Quartz scheduler.'}
    )

    sched_name = Column(String(120), primary_key=True, nullable=False)
    trigger_name = Column(String(200), primary_key=True, nullable=False)
    trigger_group = Column(String(200), primary_key=True, nullable=False)
    blob_data = Column(LargeBinary)


class QrtzCronTrigger(QrtzTrigger):
    __tablename__ = 'qrtz_cron_triggers'
    __table_args__ = (
        ForeignKeyConstraint(['sched_name', 'trigger_name', 'trigger_group'], ['qrtz_triggers.sched_name', 'qrtz_triggers.trigger_name', 'qrtz_triggers.trigger_group'], deferrable=True),
        {'comment': 'Used for Quartz scheduler.'}
    )

    sched_name = Column(String(120), primary_key=True, nullable=False)
    trigger_name = Column(String(200), primary_key=True, nullable=False)
    trigger_group = Column(String(200), primary_key=True, nullable=False)
    cron_expression = Column(String(120), nullable=False)
    time_zone_id = Column(String(80))


class QrtzSimpleTrigger(QrtzTrigger):
    __tablename__ = 'qrtz_simple_triggers'
    __table_args__ = (
        ForeignKeyConstraint(['sched_name', 'trigger_name', 'trigger_group'], ['qrtz_triggers.sched_name', 'qrtz_triggers.trigger_name', 'qrtz_triggers.trigger_group'], deferrable=True),
        {'comment': 'Used for Quartz scheduler.'}
    )

    sched_name = Column(String(120), primary_key=True, nullable=False)
    trigger_name = Column(String(200), primary_key=True, nullable=False)
    trigger_group = Column(String(200), primary_key=True, nullable=False)
    repeat_count = Column(BigInteger, nullable=False)
    repeat_interval = Column(BigInteger, nullable=False)
    times_triggered = Column(BigInteger, nullable=False)


class QrtzSimpropTrigger(QrtzTrigger):
    __tablename__ = 'qrtz_simprop_triggers'
    __table_args__ = (
        ForeignKeyConstraint(['sched_name', 'trigger_name', 'trigger_group'], ['qrtz_triggers.sched_name', 'qrtz_triggers.trigger_name', 'qrtz_triggers.trigger_group'], deferrable=True),
        {'comment': 'Used for Quartz scheduler.'}
    )

    sched_name = Column(String(120), primary_key=True, nullable=False)
    trigger_name = Column(String(200), primary_key=True, nullable=False)
    trigger_group = Column(String(200), primary_key=True, nullable=False)
    str_prop_1 = Column(String(512))
    str_prop_2 = Column(String(512))
    str_prop_3 = Column(String(512))
    int_prop_1 = Column(Integer)
    int_prop_2 = Column(Integer)
    long_prop_1 = Column(BigInteger)
    long_prop_2 = Column(BigInteger)
    dec_prop_1 = Column(Numeric(13, 4))
    dec_prop_2 = Column(Numeric(13, 4))
    bool_prop_1 = Column(Boolean)
    bool_prop_2 = Column(Boolean)


class Revision(BaseModel):
    __tablename__ = 'revision'

    id = Column(Integer, primary_key=True, server_default=text("nextval('revision_id_seq'::regclass)"))
    model = Column(String(16), nullable=False)
    model_id = Column(Integer, nullable=False, index=True)
    user_id = Column(ForeignKey('core_user.id', deferrable=True), nullable=False)
    timestamp = Column(DateTime(True), nullable=False)
    object = Column(String, nullable=False)
    is_reversion = Column(Boolean, nullable=False, server_default=text("false"))
    is_creation = Column(Boolean, nullable=False, server_default=text("false"))
    message = Column(Text)

    user = relationship('CoreUser')


class ViewLog(BaseModel):
    __tablename__ = 'view_log'

    id = Column(Integer, primary_key=True, server_default=text("nextval('view_log_id_seq'::regclass)"))
    user_id = Column(ForeignKey('core_user.id', deferrable=True), index=True)
    model = Column(String(16), nullable=False)
    model_id = Column(Integer, nullable=False, index=True)
    timestamp = Column(DateTime(True), nullable=False)

    user = relationship('CoreUser')


class ComputationJobResult(BaseModel):
    __tablename__ = 'computation_job_result'
    __table_args__ = {'comment': 'Stores results of async computation jobs.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('computation_job_result_id_seq'::regclass)"))
    job_id = Column(ForeignKey('computation_job.id', deferrable=True), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    permanence = Column(String(254), nullable=False)
    payload = Column(Text, nullable=False)

    job = relationship('ComputationJob')


class MetabaseTable(BaseModel):
    __tablename__ = 'metabase_table'
    __table_args__ = (
        UniqueConstraint('db_id', 'schema', 'name'),
        Index('idx_uniq_table_db_id_schema_name_2col', 'db_id', 'name', unique=True)
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('metabase_table_id_seq'::regclass)"), supports_json=True)
    created_at = Column(DateTime(True), nullable=False, supports_json=True)
    updated_at = Column(DateTime(True), nullable=False, supports_json=True)
    name = Column(String(254), nullable=False, supports_json=True)
    description = Column(Text, supports_json=True)
    entity_name = Column(String(254), supports_json=True)
    entity_type = Column(String(254), supports_json=True)
    active = Column(Boolean, nullable=False, supports_json=True)
    db_id = Column(ForeignKey('metabase_database.id', deferrable=True), nullable=False, index=True, supports_json=True)
    display_name = Column(String(254), supports_json=True)
    visibility_type = Column(String(254), supports_json=True)
    schema = Column(String(254), index=True, supports_json=True)
    points_of_interest = Column(Text, supports_json=True)
    caveats = Column(Text, supports_json=True)
    show_in_getting_started = Column(Boolean, nullable=False, index=True, server_default=text("false"), supports_json=True)

    metabase_table_fields = relationship("MetabaseField", supports_json=True)
    db = relationship('MetabaseDatabase')

class MetabaseField(BaseModel):
    __tablename__ = 'metabase_field'
    __table_args__ = (
        UniqueConstraint('table_id', 'parent_id', 'name'),
        Index('idx_uniq_field_table_id_parent_id_name_2col', 'table_id', 'name', unique=True)
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('metabase_field_id_seq'::regclass)"), supports_json=True)
    created_at = Column(DateTime(True), nullable=False, supports_json=True)
    updated_at = Column(DateTime(True), nullable=False, supports_json=True)
    name = Column(String(254), nullable=False, supports_json=True)
    base_type = Column(String(255), nullable=False, supports_json=True)
    special_type = Column(String(255), supports_json=True)
    active = Column(Boolean, nullable=False, server_default=text("true"), supports_json=True)
    description = Column(Text, supports_json=True)
    preview_display = Column(Boolean, nullable=False, server_default=text("true"), supports_json=True)
    position = Column(Integer, nullable=False, server_default=text("0"), supports_json=True)
    table_id = Column(ForeignKey('metabase_table.id', deferrable=False), nullable=False, index=True, supports_json=True)
    parent_id = Column(ForeignKey('metabase_field.id', deferrable=True), index=True, supports_json=True)
    display_name = Column(String(254), supports_json=True)
    visibility_type = Column(String(32), nullable=False, server_default=text("'normal'::character varying"), supports_json=True)
    fk_target_field_id = Column(Integer, supports_json=True)
    last_analyzed = Column(DateTime(True), supports_json=True)
    points_of_interest = Column(Text, supports_json=True)
    caveats = Column(Text, supports_json=True)
    fingerprint = Column(Text, comment='Serialized JSON containing non-identifying information about this Field, such as min, max, and percent JSON. Used for classification.', supports_json=True)
    fingerprint_version = Column(Integer, nullable=False, server_default=text("0"), comment='The version of the fingerprint for this Field. Used so we can keep track of which Fields need to be analyzed again when new things are added to fingerprints.', supports_json=True)
    database_type = Column(Text, nullable=False, comment='The actual type of this column in the database. e.g. VARCHAR or TEXT.', supports_json=True)
    has_field_values = Column(Text, comment='Whether we have FieldValues ("list"), should ad-hoc search ("search"), disable entirely ("none"), or infer dynamically (null)"', supports_json=True)
    settings = Column(Text, comment='Serialized JSON FE-specific settings like formatting, etc. Scope of what is stored here may increase in future.', supports_json=True)

    parent = relationship('MetabaseField', remote_side=[id])
    #table = relationship('MetabaseTable', back_populates="metabase_table_fields")


class Metric(BaseModel):
    __tablename__ = 'metric'

    id = Column(Integer, primary_key=True, server_default=text("nextval('metric_id_seq'::regclass)"))
    table_id = Column(ForeignKey('metabase_table.id', deferrable=True), nullable=False, index=True)
    creator_id = Column(ForeignKey('core_user.id', deferrable=True), nullable=False, index=True)
    name = Column(String(254), nullable=False)
    description = Column(Text)
    archived = Column(Boolean, nullable=False, server_default=text("false"))
    definition = Column(Text, nullable=False)
    created_at = Column(DateTime(True), nullable=False)
    updated_at = Column(DateTime(True), nullable=False)
    points_of_interest = Column(Text)
    caveats = Column(Text)
    how_is_this_calculated = Column(Text)
    show_in_getting_started = Column(Boolean, nullable=False, index=True, server_default=text("false"))

    creator = relationship('CoreUser')
    table = relationship('MetabaseTable')


class Pulse(BaseModel):
    __tablename__ = 'pulse'

    id = Column(Integer, primary_key=True, server_default=text("nextval('pulse_id_seq'::regclass)"))
    creator_id = Column(ForeignKey('core_user.id', deferrable=True), nullable=False, index=True)
    name = Column(String(254))
    created_at = Column(DateTime(True), nullable=False)
    updated_at = Column(DateTime(True), nullable=False)
    skip_if_empty = Column(Boolean, nullable=False, server_default=text("false"), comment='Skip a scheduled Pulse if none of its questions have any results')
    alert_condition = Column(String(254), comment='Condition (i.e. "rows" or "goal") used as a guard for alerts')
    alert_first_only = Column(Boolean, comment='True if the alert should be disabled after the first notification')
    alert_above_goal = Column(Boolean, comment='For a goal condition, alert when above the goal')
    collection_id = Column(ForeignKey('collection.id', deferrable=True), index=True, comment='Options ID of Collection this Pulse belongs to.')
    collection_position = Column(SmallInteger, comment='Optional pinned position for this item in its Collection. NULL means item is not pinned.')
    archived = Column(Boolean, server_default=text("false"), comment='Has this pulse been archived?')

    collection = relationship('Collection')
    creator = relationship('CoreUser')


class ReportDashboard(BaseModel):
    __tablename__ = 'report_dashboard'

    id = Column(Integer, primary_key=True, supports_json=True, server_default=text("nextval('report_dashboard_id_seq'::regclass)"))
    created_at = Column(DateTime(True), nullable=False, supports_json=False)
    updated_at = Column(DateTime(True), nullable=False, supports_json=False)
    name = Column(String(254), nullable=False, supports_json=True)
    description = Column(Text, supports_json=True)
    creator_id = Column(ForeignKey('core_user.id', deferrable=True), nullable=False, index=True, supports_json=True)
    parameters = Column(Text, nullable=False, supports_json=True)
    points_of_interest = Column(Text, supports_json=True)
    caveats = Column(Text, supports_json=True)
    show_in_getting_started = Column(Boolean, nullable=False, index=True, server_default=text("false"), supports_json=True)
    public_uuid = Column(CHAR(36), unique=True, comment='Unique UUID used to in publically-accessible links to this Dashboard.', supports_json=True)
    made_public_by_id = Column(ForeignKey('core_user.id', deferrable=True), comment='The ID of the User who first publically shared this Dashboard.', supports_json=True)
    enable_embedding = Column(Boolean, nullable=False, server_default=text("false"), comment='Is this Dashboard allowed to be embedded in different websites (using a signed JWT)?', supports_json=True)
    embedding_params = Column(Text, comment='Serialized JSON containing information about required parameters that must be supplied when embedding this Dashboard.', supports_json=True)
    archived = Column(Boolean, nullable=False, server_default=text("false"), comment='Is this Dashboard archived (effectively treated as deleted?)', supports_json=True)
    position = Column(Integer, comment='The position this Dashboard should appear in the Dashboards list, lower-numbered positions appearing before higher numbered ones.', supports_json=True)
    collection_id = Column(ForeignKey('collection.id', deferrable=True), index=True, comment='Optional ID of Collection this Dashboard belongs to.', supports_json=True)
    collection_position = Column(SmallInteger, comment='Optional pinned position for this item in its Collection. NULL means item is not pinned.', supports_json=True)

    collection = relationship('Collection')
    creator = relationship('CoreUser', primaryjoin='ReportDashboard.creator_id == CoreUser.id', supports_json=False)
    made_public_by = relationship('CoreUser', primaryjoin='ReportDashboard.made_public_by_id == CoreUser.id', supports_json=False)

    report_dashboard_cards = relationship("ReportDashboardcard", supports_json=True)


class ReportDashboardcard(BaseModel):
    __tablename__ = 'report_dashboardcard'

    id = Column(Integer, primary_key=True, server_default=text("nextval('report_dashboardcard_id_seq'::regclass)"), supports_json=True)
    created_at = Column(DateTime(True), nullable=False, supports_json=False)
    updated_at = Column(DateTime(True), nullable=False, supports_json=False)
    sizeX = Column(Integer, nullable=False, supports_json=True)
    sizeY = Column(Integer, nullable=False, supports_json=True)
    row = Column(Integer, nullable=False, server_default=text("0"), supports_json=True)
    col = Column(Integer, nullable=False, server_default=text("0"), supports_json=True)
    card_id = Column(ForeignKey('report_card.id', deferrable=True), index=True, supports_json=True)
    dashboard_id = Column(ForeignKey('report_dashboard.id', deferrable=True), nullable=False, index=True, supports_json=True)
    
    parameter_mappings = Column(Text, nullable=False, supports_json=True)
    visualization_settings = Column(Text, nullable=False, supports_json=True)

    card = relationship('ReportCard', supports_json=True)
    dashboard = relationship('ReportDashboard', back_populates="report_dashboard_cards")


class ReportCard(BaseModel):
    __tablename__ = 'report_card'

    id = Column(Integer, primary_key=True, server_default=text("nextval('report_card_id_seq'::regclass)"), supports_json=True)
    created_at = Column(DateTime(True), nullable=False,supports_json=False)
    updated_at = Column(DateTime(True), nullable=False, supports_json=False)
    name = Column(String(254), nullable=False, supports_json=True)
    description = Column(Text, supports_json=True)
    display = Column(String(254), nullable=False, supports_json=True)
    dataset_query = Column(Text, nullable=False, supports_json=True)
    visualization_settings = Column(Text, nullable=False, supports_json=True)
    creator_id = Column(ForeignKey('core_user.id', deferrable=True), nullable=False, index=True, supports_json=True)
    database_id = Column(ForeignKey('metabase_database.id', deferrable=True), supports_json=True)
    table_id = Column(ForeignKey('metabase_table.id', deferrable=True), supports_json=True)
    query_type = Column(String(16), supports_json=True)
    archived = Column(Boolean, nullable=False, server_default=text("false"), supports_json=True)
    collection_id = Column(ForeignKey('collection.id', deferrable=True), index=True, comment='Optional ID of Collection this Card belongs to.', supports_json=True)
    public_uuid = Column(CHAR(36), unique=True, comment='Unique UUID used to in publically-accessible links to this Card.', supports_json=True)
    made_public_by_id = Column(ForeignKey('core_user.id', deferrable=True), comment='The ID of the User who first publically shared this Card.', supports_json=True)
    enable_embedding = Column(Boolean, nullable=False, server_default=text("false"), comment='Is this Card allowed to be embedded in different websites (using a signed JWT)?', supports_json=True)
    embedding_params = Column(Text, comment='Serialized JSON containing information about required parameters that must be supplied when embedding this Card.', supports_json=True)
    cache_ttl = Column(Integer, comment='The maximum time, in seconds, to return cached results for this Card rather than running a new query.', supports_json=True)
    result_metadata = Column(Text, comment='Serialized JSON containing metadata about the result columns from running the query.', supports_json=False)
    collection_position = Column(SmallInteger, comment='Optional pinned position for this item in its Collection. NULL means item is not pinned.', supports_json=True)

    collection = relationship('Collection')
    creator = relationship('CoreUser', primaryjoin='ReportCard.creator_id == CoreUser.id')
    database = relationship('MetabaseDatabase')
    made_public_by = relationship('CoreUser', primaryjoin='ReportCard.made_public_by_id == CoreUser.id')
    table = relationship('MetabaseTable')
    report_dashboard_card = relationship('ReportDashboardcard', back_populates='card')

class Segment(BaseModel):
    __tablename__ = 'segment'

    id = Column(Integer, primary_key=True, server_default=text("nextval('segment_id_seq'::regclass)"))
    table_id = Column(ForeignKey('metabase_table.id', deferrable=True), nullable=False, index=True)
    creator_id = Column(ForeignKey('core_user.id', deferrable=True), nullable=False, index=True)
    name = Column(String(254), nullable=False)
    description = Column(Text)
    archived = Column(Boolean, nullable=False, server_default=text("false"))
    definition = Column(Text, nullable=False)
    created_at = Column(DateTime(True), nullable=False)
    updated_at = Column(DateTime(True), nullable=False)
    points_of_interest = Column(Text)
    caveats = Column(Text)
    show_in_getting_started = Column(Boolean, nullable=False, index=True, server_default=text("false"))

    creator = relationship('CoreUser')
    table = relationship('MetabaseTable')


class CardLabel(BaseModel):
    __tablename__ = 'card_label'
    __table_args__ = (
        UniqueConstraint('card_id', 'label_id'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('card_label_id_seq'::regclass)"))
    card_id = Column(ForeignKey('report_card.id', deferrable=True), nullable=False, index=True)
    label_id = Column(ForeignKey('label.id', deferrable=True), nullable=False, index=True)

    card = relationship('ReportCard')
    label = relationship('Label')


class DashboardFavorite(BaseModel):
    __tablename__ = 'dashboard_favorite'
    __table_args__ = (
        UniqueConstraint('user_id', 'dashboard_id'),
        {'comment': 'Presence of a row here indicates a given User has favorited a given Dashboard.'}
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('dashboard_favorite_id_seq'::regclass)"))
    user_id = Column(ForeignKey('core_user.id', ondelete='CASCADE', deferrable=True), nullable=False, index=True, comment='ID of the User who favorited the Dashboard.')
    dashboard_id = Column(ForeignKey('report_dashboard.id', ondelete='CASCADE', deferrable=True), nullable=False, index=True, comment='ID of the Dashboard favorited by the User.')

    dashboard = relationship('ReportDashboard')
    user = relationship('CoreUser')


class Dimension(BaseModel):
    __tablename__ = 'dimension'
    __table_args__ = (
        UniqueConstraint('field_id', 'name'),
        {'comment': 'Stores references to alternate views of existing fields, such as remapping an integer to a description, like an enum'}
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('dimension_id_seq'::regclass)"))
    field_id = Column(ForeignKey('metabase_field.id', ondelete='CASCADE', deferrable=True), nullable=False, index=True, comment='ID of the field this dimension row applies to')
    name = Column(String(254), nullable=False, comment='Short description used as the display name of this new column')
    type = Column(String(254), nullable=False, comment='Either internal for a user defined remapping or external for a foreign key based remapping')
    human_readable_field_id = Column(ForeignKey('metabase_field.id', ondelete='CASCADE', deferrable=True), comment='Only used with external type remappings. Indicates which field on the FK related table to use for display')
    created_at = Column(DateTime, nullable=False, comment='The timestamp of when the dimension was created.')
    updated_at = Column(DateTime, nullable=False, comment='The timestamp of when these dimension was last updated.')

    field = relationship('MetabaseField', primaryjoin='Dimension.field_id == MetabaseField.id')
    human_readable_field = relationship('MetabaseField', primaryjoin='Dimension.human_readable_field_id == MetabaseField.id')


class MetabaseFieldvalue(BaseModel):
    __tablename__ = 'metabase_fieldvalues'

    id = Column(Integer, primary_key=True, server_default=text("nextval('metabase_fieldvalues_id_seq'::regclass)"))
    created_at = Column(DateTime(True), nullable=False)
    updated_at = Column(DateTime(True), nullable=False)
    values = Column(Text)
    human_readable_values = Column(Text)
    field_id = Column(ForeignKey('metabase_field.id', deferrable=True), nullable=False, index=True)

    field = relationship('MetabaseField')


class MetricImportantField(BaseModel):
    __tablename__ = 'metric_important_field'
    __table_args__ = (
        UniqueConstraint('metric_id', 'field_id'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('metric_important_field_id_seq'::regclass)"))
    metric_id = Column(ForeignKey('metric.id', deferrable=True), nullable=False, index=True)
    field_id = Column(ForeignKey('metabase_field.id', deferrable=True), nullable=False, index=True)

    field = relationship('MetabaseField')
    metric = relationship('Metric')


class PulseCard(BaseModel):
    __tablename__ = 'pulse_card'

    id = Column(Integer, primary_key=True, server_default=text("nextval('pulse_card_id_seq'::regclass)"))
    pulse_id = Column(ForeignKey('pulse.id', deferrable=True), nullable=False, index=True)
    card_id = Column(ForeignKey('report_card.id', deferrable=True), nullable=False, index=True)
    position = Column(Integer, nullable=False)
    include_csv = Column(Boolean, nullable=False, server_default=text("false"), comment='True if a CSV of the data should be included for this pulse card')
    include_xls = Column(Boolean, nullable=False, server_default=text("false"), comment='True if a XLS of the data should be included for this pulse card')

    card = relationship('ReportCard')
    pulse = relationship('Pulse')


class PulseChannel(BaseModel):
    __tablename__ = 'pulse_channel'

    id = Column(Integer, primary_key=True, server_default=text("nextval('pulse_channel_id_seq'::regclass)"))
    pulse_id = Column(ForeignKey('pulse.id', deferrable=True), nullable=False, index=True)
    channel_type = Column(String(32), nullable=False)
    details = Column(Text, nullable=False)
    schedule_type = Column(String(32), nullable=False, index=True)
    schedule_hour = Column(Integer)
    schedule_day = Column(String(64))
    created_at = Column(DateTime(True), nullable=False)
    updated_at = Column(DateTime(True), nullable=False)
    schedule_frame = Column(String(32))
    enabled = Column(Boolean, nullable=False, server_default=text("true"))

    pulse = relationship('Pulse')


class ReportCardfavorite(BaseModel):
    __tablename__ = 'report_cardfavorite'
    __table_args__ = (
        UniqueConstraint('card_id', 'owner_id'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('report_cardfavorite_id_seq'::regclass)"))
    created_at = Column(DateTime(True), nullable=False)
    updated_at = Column(DateTime(True), nullable=False)
    card_id = Column(ForeignKey('report_card.id', deferrable=True), nullable=False, index=True)
    owner_id = Column(ForeignKey('core_user.id', deferrable=True), nullable=False, index=True)

    card = relationship('ReportCard')
    owner = relationship('CoreUser')


class DashboardcardSery(BaseModel):
    __tablename__ = 'dashboardcard_series'

    id = Column(Integer, primary_key=True, server_default=text("nextval('dashboardcard_series_id_seq'::regclass)"))
    dashboardcard_id = Column(ForeignKey('report_dashboardcard.id', deferrable=True), nullable=False, index=True)
    card_id = Column(ForeignKey('report_card.id', deferrable=True), nullable=False, index=True)
    position = Column(Integer, nullable=False)

    card = relationship('ReportCard')
    dashboardcard = relationship('ReportDashboardcard')


class PulseChannelRecipient(BaseModel):
    __tablename__ = 'pulse_channel_recipient'

    id = Column(Integer, primary_key=True, server_default=text("nextval('pulse_channel_recipient_id_seq'::regclass)"))
    pulse_channel_id = Column(ForeignKey('pulse_channel.id', deferrable=True), nullable=False)
    user_id = Column(ForeignKey('core_user.id', deferrable=True), nullable=False)

    pulse_channel = relationship('PulseChannel')
    user = relationship('CoreUser')
