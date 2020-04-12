from logging import ERROR, Filter, Formatter, StreamHandler
from logging.handlers import TimedRotatingFileHandler

from flask import request
from flask.ext.login import current_user


class ContextualFilter(Filter):
    def filter(self, log_record):
        log_record.url = request.path
        log_record.method = request.method
        log_record.ip = request.environ.get("REMOTE_ADDR")
        log_record.user_id = (-1 if current_user.is_anonymous()
                              else current_user.get_id())

        return True


def init_app(app, remove_existing_handlers=False):
    # Create the filter and add it to the base application logger
    context_provider = ContextualFilter()
    app.logger.addFilter(context_provider)  # 将日志需要输出的信息都定义在filter()中

    # Optionally, remove Flask's default debug handler
    if remove_existing_handlers:  # 移除logger的处理器，为新建处理器做准备
        del app.logger.handlers[:]

    # Create a new handler for log messages
    # that will send them to standard error
    handler = StreamHandler()

    # Add a formatter that makes use of our new contextual information
    log_format = ("%(asctime)s\t%(levelname)s\t%(user_id)s\t"
                  "%(ip)s\t%(method)s\t%(url)s\t%(message)s")  # 其中asctime(访问时间)由系统生成，
                                                               # levelname和message在生成日志时指定
    formatter = Formatter(log_format)
    handler.setFormatter(formatter)

    # Finally, attach the handler to our logger
    app.logger.addHandler(handler)  # 控制日志记录格式

    # Only set up a file handler if we know where to put the logs
    if app.config.get("ERROR_LOG_PATH"):  # 如果config配置文件中有配置“ERROR_LOG_PATH”(错误路径日志)，
                                          # 就把ERROR级别的日志以特定的格式保存到这个路径下的文件中。

        # Create one file for each day. Delete logs over 7 days old.
        file_handler = TimedRotatingFileHandler(app.config["ERROR_LOG_PATH"],
                                                when="D", backupCount=7)

        # Use a multi-line format for this logger, for easier scanning
        file_formatter = Formatter("""
        Time: %(asctime)s
        Level: %(levelname)s
        Method: %(method)s
        Path: %(url)s
        IP: %(ip)s
        User ID: %(user_id)s

        Message: %(message)s

        ---------------------""")

        # Filter out all log messages that are lower than Error.
        file_handler.setLevel(ERROR)

        file_handler.setFormatter(file_formatter)
        app.logger.addHandler(file_handler)
