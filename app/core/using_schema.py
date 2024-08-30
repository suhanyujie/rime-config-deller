import yaml


# 找出配置文件中正在使用的方案，这些方案是不能删除的
class UsingSchema:
    default_schema_file = "default.custom.yaml"

    def __init__(self, default_file="") -> None:
        self.default_schema_file = default_file

    def get_using_list(self):
        using_id_list = []
        with open(self.default_schema_file, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            if "patch" in data and "schema_list" in data["patch"]:
                using_schema_list = data["patch"]["schema_list"]
                for item in using_schema_list:
                    using_id_list.append(item["schema"])
        return using_id_list

    def get_ingore_list(self):
        return self.get_using_list()


def test():
    o = UsingSchema()
    o.default_schema_file = "D:\\programData\\Rime1\\default.custom.yaml"
    list = o.get_ingore_list()
    print(list)
    pass
