import contacts.config as config
import contacts.core as api
import contacts.file_storage as persistence
import contacts.ui as ui

if __name__ == "__main__":
    config.parse()
    persistence.init(config)
    api.init(persistence)
    ui.init(config, api)
    ui.start()
