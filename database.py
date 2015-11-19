# -*- coding: utf-8 -*-
__author__ = 'guenther@eberl.se'

# Import program components / modules from python standard library / non-standard modules.
import logging
import logging.config
import os
import sys

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Logging config on sub-module level.
logger = logging.getLogger(__name__)

# Determine if program is running compiled to *.exe/*.app or from Python interpreter.
if hasattr(sys, 'frozen'):
    app_path = os.path.abspath(os.path.dirname(sys.executable)) + os.sep
else:
    app_path = os.path.abspath(os.path.dirname(__file__)) + os.sep

# Database config, SQLite version.
database_type = 'sqlite:///'
database_path = os.path.abspath(app_path + 'database.sqlite')

# Database config, PostgreSQL version.
# database_type = 'postgresql://'
# database_path = 'scott:tiger@localhost:5432/my_processes'

engine = create_engine(database_type + database_path, encoding='utf8')
Base = declarative_base()
logger.info('Using %s database.' % database_type)


def flatten_list(input_list):
    """
    Return an list that consists of one nesting level less then the input list.

    Gets rid of one level of nesting per run. As soon as the input_list contains one non-list element an error occurs.

    Example: flatten_list([[1], [2], [3]]) -> [1, 2, 3]
             flatten_list([[[1], [2], [3]], [[4], [5], [6]]]) -> [[1], [2], [3], [4], [5], [6]]
             flatten_list([[1], [2], 3]) -> error

    :param input_list: A list of lists.
    """
    output_list = [item for sub_list in input_list for item in sub_list]
    return output_list


def create_all_tables():
    """
    Create all tables that are defined in here.

    This doesn't change the design of any already present tables. Drop these tables first to have them recreated.
    """
    try:
        Base.metadata.create_all(engine)
        create_success = True
    except Exception as err:
        print err
        create_success = False
    return create_success


# noinspection PyPep8Naming
def start_session():
    logger.debug('Starting SQLAlchemy session.')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def vacuum_database():
    size_bytes_before = os.path.getsize(database_path)
    logger.info('Starting database vacuum. Current database file size is %s bytes.' % size_bytes_before)
    db = engine.connect()
    db.execute('VACUUM')
    db.close()
    size_bytes_after = os.path.getsize(database_path)
    size_bytes_difference = size_bytes_before - size_bytes_after
    logger.info('Database vacuum finished. New database size is %s bytes (%s bytes less).' %
                (size_bytes_after, size_bytes_difference))


def create_window_record(window_info):
    session = start_session()
    new_window = OpenWindow(pos_x=window_info[0], pos_y=window_info[1], size_x=window_info[2], size_y=window_info[3],
                            title_name=window_info[4], class_name=window_info[5], pid=window_info[6],
                            date_time=window_info[7])
    session.add(new_window)
    session.flush()
    session.refresh(new_window)
    # noinspection PyProtectedMember
    window_db_id = int(new_window._id)
    session.commit()
    session.close()
    logger.debug('New OpenWindow record created, db_id %i.' % window_db_id)
    return window_db_id


def query_process_to_monitor():
    session = start_session()
    # noinspection PyProtectedMember
    processes_to_monitor = session.query(ProcessToMonitor._id, ProcessToMonitor.by_name).all()
    session.close()
    return processes_to_monitor


def create_process_record(process_info):
    session = start_session()
    new_process = ProcessInfo(_id_process_to_monitor=process_info[0], date_time=process_info[1], name=process_info[2],
                              instance=process_info[3], pid=process_info[4], parent_pid=process_info[5],
                              status=process_info[6], user_name=process_info[7], create_time=process_info[8],
                              command_line=process_info[9], connections=process_info[10], cpu_affinity=process_info[11],
                              cpu_percent=process_info[12], cpu_times=process_info[13], executable_dir=process_info[14],
                              io_stats=process_info[15], io_niceness=process_info[16], memory_info=process_info[17],
                              memory_info_extended=process_info[18], memory_maps=process_info[19],
                              memory_percent=process_info[20], num_ctx_switches=process_info[21],
                              num_handles=process_info[22], num_threads=process_info[23], threads=process_info[24],
                              niceness=process_info[25], open_files=process_info[26])
    session.add(new_process)
    session.flush()
    session.refresh(new_process)
    # noinspection PyProtectedMember
    process_db_id = int(new_process._id)
    session.commit()
    session.close()
    logger.debug('New Process record created, db_id %i.' % process_db_id)
    return process_db_id


class OpenWindow(Base):
    __tablename__ = 'open_window'

    _id = Column(Integer, primary_key=True)
    pos_x = Column(Integer)
    pos_y = Column(Integer)
    size_x = Column(Integer)
    size_y = Column(Integer)
    title_name = Column(Text)
    class_name = Column(Text)
    pid = Column(Integer)
    date_time = Column(DateTime)

    def __init__(self, pos_x=None, pos_y=None, size_x=None, size_y=None, title_name=None, class_name=None, pid=None,
                 date_time=None):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y
        self.title_name = title_name
        self.class_name = class_name
        self.pid = pid
        self.date_time = date_time


class ProcessToMonitor(Base):
    __tablename__ = 'process_to_monitor'

    _id = Column(Integer, primary_key=True)
    by_name = Column(Text)


class ProcessInfo(Base):
    __tablename__ = 'process_info'

    _id = Column(Integer, primary_key=True)
    _id_process_to_monitor = Column(Integer, ForeignKey('process_to_monitor._id'), nullable=False)

    name = Column(Text)
    instance = Column(Integer)
    pid = Column(Text)
    parent_pid = Column(Text)
    status = Column(Text)
    user_name = Column(Text)
    create_time = Column(DateTime)
    command_line = Column(Text)
    connections = Column(Text)
    cpu_affinity = Column(Text)
    cpu_percent = Column(Text)
    cpu_times = Column(Text)
    executable_dir = Column(Text)
    io_stats = Column(Text)
    io_niceness = Column(Text)
    memory_info = Column(Text)
    memory_info_extended = Column(Text)
    memory_maps = Column(Text)
    memory_percent = Column(Text)
    num_ctx_switches = Column(Text)
    num_handles = Column(Text)
    num_threads = Column(Text)
    threads = Column(Text)
    niceness = Column(Text)
    open_files = Column(Text)
    date_time = Column(DateTime)


# Do the following if this file is run by itself and not used via an import in another module.
if __name__ == '__main__':
    # The logging config from main.py is not present when run individually.
    logger = logging.getLogger(__name__)
    logging.config.fileConfig(r'logging_to_terminal.ini', disable_existing_loggers=False)

    # Create all tables of the scheme.
    print create_all_tables()
