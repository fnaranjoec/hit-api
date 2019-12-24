def decide_on_model(model):
    """Small helper function to pipe all DB operations of a apiwingo model to the wingo_data DB"""
    return 'wingo_data' if model._meta.app_label == 'apiwingo' else None


class WingoDbRouter:
    """
    Implements a database router so that:

    * Django related data - DB alias `default` - MySQL DB `world_django`
    * Legacy "wingodb" database data (everything "non-Django") - DB alias `wingo_data` - MySQL DB `wingodb`
    """
    def db_for_read(self, model, **hints):
        return decide_on_model(model)

    def db_for_write(self, model, **hints):
        return decide_on_model(model)

    def allow_relation(self, obj1, obj2, **hints):
        # Allow any relation if both models are part of the apiwingo app
        if obj1._meta.app_label == 'apiwingo' and obj2._meta.app_label == 'apiwingo':
            return True
        # Allow if neither is part of apiwingo app
        elif 'apiwingo' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        # by default return None - "undecided"

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # allow migrations on the "default" (django related data) DB
        if db == 'default' and app_label != 'apiwingo':
            return True

        # allow migrations on the legacy database too:
        # this will enable to actually alter the database schema of the legacy DB!
        if db == 'wingo_data' and app_label == "apiwingo":
           return True

        return False