#encoding: utf-8

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from exts import db
from MIOMI_v1_Web import app
from models import Customer, Employee, Glass, Eyedrop, Nursing, Washing, Consumption, EmployeeLog

manager = Manager(app)

# 使用绑定app, db
migrate = Migrate(app, db)

# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
