from pathlib import Path
import re

from pathobj_handler.filestem.picker import PickFilesBySuffix
from pathobj_handler.tool import make_pipeline
from pathobj_handler.filestem.renamer import RenameFilesByCustomFunction, RenamerWithReplaceStr

dir_path = './resource'
test_files = [
    f"{dir_path}/sample/20240410T150525_DDDDDD111111_AAA.txt",
    f"{dir_path}/sample/20240411T150625_DDDDDD111111_BBB.txt",
    f"{dir_path}/sample/20240412T150725_DDDDDD222222_AAA.txt",
    f"{dir_path}/sample/20240413T150825_DDDDDD333333_BBB.txt",
    f"{dir_path}/sample/fuga_01.txt",
    f"{dir_path}/sample/fuga_02.txt",
    f"{dir_path}/sample/hoge_01.text",
    f"{dir_path}/sample/hoge_02.text",
]


def path_check(path: str) -> None:
    p_path = Path(path)
    if p_path.exists():
        return
    p_path.parent.mkdir(parents=True, exist_ok=True)
    p_path.touch()


''' ------------ test_* functions ------------ '''


def test_renamer_custom_function() -> None:
    for f in test_files:
        path_check(f)

    add_word = '_add'

    ''' Answers to the test '''
    p_test_files = [Path(f) for f in test_files]
    p_add_files = []
    for p in p_test_files:
        stem = p.stem
        suffix = p.suffix
        new_stem = stem + add_word
        new_path = p.with_name(new_stem + suffix)
        p_add_files.append(new_path)

    ''' Processing by the module '''
    fp = PickFilesBySuffix(['.txt', '.text'], recursive=True)

    def add_stem(src_stem: str) -> str:
        return src_stem + add_word

    def del_stem(src_stem: str) -> str:
        return re.sub(add_word, '', src_stem)

    rn_1 = RenameFilesByCustomFunction(rename_method=add_stem)
    fp_filter = make_pipeline(fp, rn_1)
    fp_gen = fp_filter(dir_path)

    # print(p_add_files)  # pytest -s
    assert p_add_files == list(fp_gen)

    rn_2 = RenameFilesByCustomFunction(rename_method=del_stem)

    fp_filter = make_pipeline(fp, rn_2)
    fp_gen = fp_filter(dir_path)

    # print(p_test_files)  # pytest -s
    assert p_test_files == list(fp_gen)


def test_renamer_replace_str() -> None:
    for f in test_files:
        path_check(f)

    old_str = '_AAA'
    new_str = '_ZZZ'
    assert new_str  # new_str is not ''

    ''' Answers to the test '''
    p_test_files = [Path(f) for f in test_files]
    p_replace_files = []
    for p in p_test_files:
        stem = p.stem
        suffix = p.suffix
        new_stem = stem.replace(old_str, new_str)
        new_path = p.with_name(new_stem + suffix)
        p_replace_files.append(new_path)

    ''' Processing by the module '''
    fp = PickFilesBySuffix(['.txt', '.text'], recursive=True)

    rn_1 = RenamerWithReplaceStr(old=old_str, new=new_str)
    fp_filter = make_pipeline(fp, rn_1)
    fp_gen = fp_filter(dir_path)

    # print(p_replace_files)  # pytest -s
    assert p_replace_files == list(fp_gen)

    rn_2 = RenamerWithReplaceStr(old=new_str, new=old_str)

    fp_filter = make_pipeline(fp, rn_2)
    fp_gen = fp_filter(dir_path)

    # print(p_test_files)  # pytest -s
    assert p_test_files == list(fp_gen)
