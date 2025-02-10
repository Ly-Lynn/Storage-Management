class ProductDatabaseRouter:
    """Chỉ định database cho từng model"""

    def db_for_read(self, model, **hints):
        if model._meta.app_label == "logs":
            return "mongodb"
        return "default"  

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "logs":
            return "mongodb"
        return "default"

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == "mongodb":
            return False
        return True
