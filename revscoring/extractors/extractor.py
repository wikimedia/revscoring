import yamlconf


class Extractor:

    def extract(self, rev_id, features, cache=None):
        raise NotImplementedError()

    @classmethod
    def from_config(cls, config, name, section_key="extractors"):
        section = config[section_key][name]
        if 'module' in section:
            return yamlconf.import_module(section['module'])
        elif 'class' in section:
            Class = yamlconf.import_module(section['class'])
            return Class.from_config(config, name)
