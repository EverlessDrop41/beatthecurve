from playhouse.migrate import migrate, PostgresqlMigrator
from app.models import DATABASE
from app.notes.models import Note

migrator = PostgresqlMigrator(DATABASE)

Note.lesson.default = 2
Note.semester.default = 1
Note.year.default = 2016

try:
    migrate(
        migrator.add_column('TBL_NOTE', Note.semester.db_column, Note.semester)
    )
except:
    pass

try:
    migrate(
        migrator.add_column('TBL_NOTE', Note.year.db_column, Note.year)
    )
except:
    pass


try:
    migrate(
        migrator.add_column('TBL_NOTE', Note.lesson.db_column, Note.lesson)
    )
except:
    pass

