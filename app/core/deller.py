from typing import Dict, List, Tuple
from pathlib import Path
import os
import yaml
import winreg


class Deller:
    def __init__(self, rime_user_dir="") -> None:
        if rime_user_dir == "":
            print("rime user dir is unknown.")
            raise ValueError("rime user dir is unknown.")
        self.schema_list = []
        self.schema_map_keyby_id: Dict[str, RimeSchema] = {}
        self.schema_files = []
        self.yaml_files = []

        path = Path(rime_user_dir)
        self.files = [str(file) for file in path.iterdir() if file.is_file()]
        self.dirs = [str(file) for file in path.iterdir() if file.is_dir()]
        pass

    def init_schema_list(self):
        schema_file_list = []
        for f in self.files:
            tmp_base_name = os.path.basename(f)
            if ".schema.yaml" in tmp_base_name:
                schema_file_list.append(f)
        schema_list = []
        schema_map = {}
        for schema_file in schema_file_list:
            (tmp_schema_id, tmp_schema_name) = self.get_schema_id_name_by_file(
                schema_file
            )
            tmp_schema_obj = RimeSchema(tmp_schema_id, self.files, self.dirs)
            schema_list.append(tmp_schema_obj)
            schema_map[tmp_schema_id] = tmp_schema_obj
        self.schema_list = schema_list
        self.schema_map_keyby_id = schema_map

    # delete rime schema files
    def delete_by_schema_ids(self, sid_list: List):
        for schema_id in sid_list:
            if schema_id in self.schema_map_keyby_id:
                self.schema_map_keyby_id[schema_id].delete()
        pass

    def list_files_in_directory(self, directory):
        try:
            path = Path(directory)
            files = [str(file) for file in path.iterdir() if file.is_file()]
            yaml_list = []
            schema_file_list = []
            for f in files:
                if ".yaml" in f:
                    yaml_list.append(f)
                if ".schema.yaml" in f:
                    schema_file_list.append(f)
            self.yaml_files = yaml_list
            self.schema_files = schema_file_list
            return files
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def get_schema_id_name_by_file(self, schema_file="") -> Tuple[str, str]:
        # 解析 yaml 获取输入法 scheme id todo
        data = {}
        schema_id = ""
        schema_name = ""
        with open(schema_file, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            schema_id = data["schema"]["schema_id"]
            schema_name = data["schema"]["name"]
        if schema_id == "":
            return (schema_id, schema_name)
        return (schema_id, schema_name)

    def get_schema_name_list(self) -> Dict[str, str]:
        pass


class RimeSchema:
    def __init__(
        self,
        schema_id="",
        file_list=[],
        dir_list=[],
    ) -> None:
        self.name = schema_id
        self.nick_name = ""
        self.schema_file = ""
        self.relate_files = []
        self.relate_dirs = []

        self.yaml_files = []
        self.schema_files = []

        self.init_file_list()
        self.file_list = file_list
        self.dir_list = dir_list
        pass

    def init_file_list(self):
        try:
            files = self.file_list
            dirs = self.dir_list
            schema_file_list = []
            relate_files = []
            # 获取相关的配置文件列表
            for f in files:
                tmp_base_name = os.path.basename(f)
                if ".schema.yaml" in tmp_base_name:
                    schema_file_list.append(f)
                if self.name + "." in tmp_base_name:
                    relate_files.append(f)
            self.schema_files = schema_file_list
            self.relate_files = relate_files
            for tmp in dirs:
                if self.name + "." in tmp:
                    self.relate_dirs.append(tmp)
        except Exception as e:
            print(f"An error occurred: {e}")

    def delete(self, include_dir = False):
        if len(self.relate_files) <= 0:
            return
        for tmp in self.relate_files:
            os.remove(tmp)
        if include_dir:
            for dir in self.relate_dirs:
                os.removedirs(dir)
        pass

    def get_schema_name(self):
        pass


def get_rime_user_dir() -> str:
    h_key = winreg.HKEY_CURRENT_USER
    sub_key = "Software\\Rime\\Weasel"
    rime_key = winreg.OpenKey(h_key, sub_key=sub_key)
    # 判断是否打开成功 todo
    rime_user_dir, ret = winreg.QueryValueEx(rime_key, "RimeUserDir")
    if ret != 1:
        raise ValueError("获取输入法用户目录异常。")
    return rime_user_dir


# 示例用法
rime_user_dir = "D:\programData\Rime1"
deller = Deller(rime_user_dir)
deller.list_files_in_directory(rime_user_dir)
# print("Files in directory:", files)

# ['D:\\programData\\Rime1\\double_pinyin.schema.yaml', 'D:\\programData\\Rime1\\double_pinyin_abc.schema.yaml', 'D:\\programData\\Rime1\\double_pinyin_flypy.schema.yaml', 'D:\\programData\\Rime1\\double_pinyin_mspy.schema.yaml', 'D:\\programData\\Rime1\\double_pinyin_sogou.schema.yaml', 'D:\\programData\\Rime1\\double_pinyin_ziguang.schema.yaml', 'D:\\programData\\Rime1\\japanese.schema.yaml', 'D:\\programData\\Rime1\\melt_eng.schema.yaml', 'D:\\programData\\Rime1\\radical_pinyin.schema.yaml', 'D:\\programData\\Rime1\\radical_pinyin_flypy.schema.yaml', 'D:\\programData\\Rime1\\rime_mint.schema.yaml', 'D:\\programData\\Rime1\\rime_mint_flypy.schema.yaml', 'D:\\programData\\Rime1\\stroke.schema.yaml', 'D:\\programData\\Rime1\\t9.schema.yaml', 'D:\\programData\\Rime1\\terra_pinyin.schema.yaml', 'D:\\programData\\Rime1\\wubi86_jidian.schema.yaml', 'D:\\programData\\Rime1\\wubi98_mint.schema.yaml']
res = deller.get_schema_id_name_by_file("D:\\programData\\Rime1\\rime_mint.schema.yaml")
print(res)
