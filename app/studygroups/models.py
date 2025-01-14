from peewee import *
from app.models import DATABASE
from app.auth.models import User
from app.lesson.models import Lesson
from datetime import datetime


class StudyGroup(Model):
    """Model representing a studygroup for a lesson a user can join"""
    id = PrimaryKeyField(db_column='ID')
    number_of_members = IntegerField(db_column='NUMBER_OF_MEMBERS', default=1)
    productivity = DecimalField(db_column='PRODUCTIVITY', default=0)
    location = TextField(db_column='LOCATION')
    founder = ForeignKeyField(User, db_column='FOUNDER_ID')
    lesson = ForeignKeyField(Lesson, db_column='LESSON_ID')

    class Meta:
        database = DATABASE
        db_table = 'TBL_STUDY_GROUP'

    def get_next_session(self):
        """Method to get the next upcoming session for an instance of a StudyGroup"""
        try:
            query = StudyGroupSession.select().where((StudyGroupSession.datetime >= datetime.now()) & (StudyGroupSession.cancelled == False) & (StudyGroupSession.study_group == self.id)).order_by(StudyGroupSession.datetime.asc())
            for q in query:
                return q
        except Exception as e:
            print(e)
            return None

    def get_all_upcoming_sessions(self):
        """Method to get all the upcoming sessions for a StudyGroup"""
        try:
            query = StudyGroupSession.select().where((StudyGroupSession.datetime >= datetime.now()) & (StudyGroupSession.study_group == self.id)).order_by(StudyGroupSession.datetime.asc())
            print([q for q in query])
            return [q for q in query]
        except Exception as e:
            print(e)
            return None

    def add_member(self, user):
        """Method to add a user to a StudyGroup"""
        try:
            if self.is_member(user):
                return None

            self.number_of_members += 1
            self.save()

            StudyGroupMembers.create(
                user=user.user_id,
                study_group=self.id
            )
            return True
        except:
            return None

    def remove_member(self, user):
        """Method to remove of member from a StudyGroup"""
        try:
            self.number_of_members -= 1
            self.save()
            StudyGroupMembers.delete().where((StudyGroupMembers.study_group == self.id) & (StudyGroupMembers.user == user.user_id)).execute()
            return True
        except:
            return False

    def is_member(self, user):
        """Returns True if a User is in a StudyGroup"""
        if StudyGroupMembers.select().where((StudyGroupMembers.user == user.user_id) & (StudyGroupMembers.study_group == self.id)).exists():
                return True
        return False

    def add_comment(self, content, user):
        """Creates a comment for a StudyGroup"""
        try:
            StudyGroupComment.create(
                user=user.user_id,
                content=content,
                study_group=self.id
            )
            return True
        except:
            return False

    def get_comments(self):
        """Returns a list of StudyGroupComments for a StudyGroup"""
        comments = StudyGroupComment.select().where(StudyGroupComment.study_group == self.id)
        return [c for c in comments]


class StudyGroupMembers(Model):
    """Model that represents a User in a StudyGroup"""
    id = PrimaryKeyField(db_column='ID')
    user = ForeignKeyField(User, db_column='USER_ID')
    study_group = ForeignKeyField(StudyGroup, db_column='STUDY_GROUP_ID')

    class Meta:
        database = DATABASE
        db_table = 'TBL_STUDY_GROUP_MEMBER'
        indexes = (
            (('user', 'study_group'), True),
        )


class StudyGroupSession(Model):
    """Model representing a session for a StudyGroup"""
    id = PrimaryKeyField(db_column='ID')
    study_group = ForeignKeyField(StudyGroup, db_column='STUDY_GROUP_ID')
    cancelled = BooleanField(default=False, db_column='CANCELLED')
    datetime = DateTimeField(db_column='DATETIME')

    class Meta:
        indexes = (
            (('study_group', 'datetime'), True),
        )
        database = DATABASE
        db_table = 'TBL_STUDY_GROUP_SESSION'


class StudyGroupComment(Model):
    """Model representing a comment about a StudyGroup"""
    id = PrimaryKeyField(db_column='ID')
    user = ForeignKeyField(User, db_column='USER_ID')
    content = CharField(db_column='CONTENT')
    study_group = ForeignKeyField(StudyGroup, db_column='STUDY_GROUP_ID')

    class Meta:
        database = DATABASE
        db_table = 'TBL_STUDY_GROUP_COMMENT'
