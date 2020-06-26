import uuid
from datetime import datetime, timedelta
from faker.providers import BaseProvider


class ScopeProvider(BaseProvider):

    def __init__(self, *args, **kwargs):
        super(ScopeProvider, self).__init__(*args, **kwargs)
        self._scopes = {}

    def _inspect_scope(self, value, scope=None, version=0):
        if scope not in self._scopes:
            self._scopes[scope] = (version, value)
            return value
        else:
            oldVersion, oldValue = self._scopes[scope]
            if oldVersion != version:
                self._scopes[scope] = (version, value)
                return value
            else:
                return oldValue


class UUIDProvider(BaseProvider):

    def uuid(self):
        return uuid.uuid4().hex


class UUIDScopeProvider(ScopeProvider):

    def uuid_scope(self, scope=None, version=0):
        value = uuid.uuid4().hex
        return self._inspect_scope(value, scope=scope, version=version)


class ProcessingDatetimeProvider(BaseProvider):

    def processing_datetime(self, pattern="%Y-%m-%d %H:%M:%S", delta=0):
        now = datetime.now() + timedelta(milliseconds=delta)
        return now.strftime(pattern)


class ProcessingDatetimeScopeProvider(ScopeProvider):

    def processing_datetime_scope(self, pattern="%Y-%m-%d %H:%M:%S", delta=0, scope=None, version=0):
        now = datetime.now() + timedelta(milliseconds=delta)
        value = now.strftime(pattern)
        return self._inspect_scope(value, scope=scope, version=version)
