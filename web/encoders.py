import json
from .models import User, PsychicList


class UserJsonEncoder(json.JSONEncoder):
    def default(self, obj: User):
        if isinstance(obj, User):
            return {
                'conceived_numbers': obj.conceived_numbers,
            }

        return super().default(obj)


class PsychicListJsonEncoder(json.JSONEncoder):
    def default(self, obj: PsychicList):
        if isinstance(obj, PsychicList):
            list_json = []

            for el in obj.list_psychics:
                list_json.append({
                    'name': el.name,
                    'predict_number': el.predict_number,
                    'success': el.success
                })
            return list_json

        return super().default(obj)