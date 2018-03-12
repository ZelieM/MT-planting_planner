# DB router for the library app


class VegetablesLibraryDBRouter(object):
    """
    A router to control vegetables_library db operations
    """
    def db_for_read(self, model, **hints):
        "Point all operations on vegetables_library models to 'db_vegetables_library'"
        if model._meta.app_label == 'vegetables_library':
            return 'db_vegetables_library'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on vegetables_library models to 'db_vegetables_library'"
        if model._meta.app_label == 'vegetables_library':
            return 'db_vegetables_library'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in vegetables_library is involved"
        if obj1._meta.app_label == 'vegetables_library' or \
                obj2._meta.app_label == 'vegetables_library':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        "Make sure the vegetables_library app only appears on the 'vegetables_library' db"
        if app_label == 'vegetables_library':
            return db == 'db_vegetables_library'
        return db == 'default'
