import json

from importlib import import_module
from django.conf import settings

from .encoders import PsychicListJsonEncoder, UserJsonEncoder
from .models import PsychicList, Psychic, User

SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


class AbstractStorage:

    def __init__(self, session_key):
        self.session_key = session_key

    def save(self, obj: object):
        raise NotImplementedError

    def load(self) -> object:
        raise NotImplementedError

    def save_user(self, obj: object):
        raise NotImplementedError

    def load_user(self) -> object:
        raise NotImplementedError


class PsychicAbstractStorage(AbstractStorage):

    def save(self, obj: PsychicList):
        raise NotImplementedError

    def load(self) -> PsychicList:
        raise NotImplementedError

    def save_user(self, obj: User):
        raise NotImplementedError

    def load_user(self) -> User:
        raise NotImplementedError


class PsychicSessionStorage(PsychicAbstractStorage):

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.store = SessionStore(session_key=self.session_key)

    def save(self, obj: PsychicList) -> None:
        self.store['psychic_list'] = json.dumps(obj, cls=PsychicListJsonEncoder)
        self.store.save()

    def save_user(self, user: User) -> None:
        self.store['conceived_numbers'] = json.dumps(user, cls=UserJsonEncoder)
        self.store.save()

    def load(self) -> PsychicList():
        list_json = json.loads(self.store['psychic_list'])

        the_list_psychics = PsychicList()
        for psy in list_json:
            psy = Psychic(name=psy['name'], predict_number=psy['predict_number'], success=psy['success'])
            the_list_psychics.add_psychics_to_list(psy)
        return the_list_psychics

    def load_user(self) -> User():
        list_json = json.loads(self.store['conceived_numbers'])

        gamer = User(conceived_numbers=list_json['conceived_numbers'])
        return gamer


class StorageFactory:

    @staticmethod
    def create_storage(session_key) -> AbstractStorage:
        assert issubclass(settings.STORAGE, AbstractStorage)
        return settings.STORAGE(session_key)

