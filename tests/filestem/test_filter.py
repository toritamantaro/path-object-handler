from pathlib import Path
from datetime import datetime
import re

from pathobj_handler.filestem.picker import PickFilesBySuffix
from pathobj_handler.tool import make_pipeline
from pathobj_handler.filestem.filter import FilterByCustomFunction, FilterWithDateRange, FilterWithRegExp

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


def test_filter_custom_function() -> None:
    for f in test_files:
        path_check(f)

    target_word = 'hoge'

    ''' Answers to the test '''
    target_files = [f for f in test_files if target_word in f]
    p_target_files = [Path(f) for f in target_files]

    ''' Processing by the module '''
    fp = PickFilesBySuffix(['.txt', '.text'], recursive=True)

    def is_target(stem: str) -> bool:
        return target_word in stem

    fl_1 = FilterByCustomFunction(filter_method=is_target)

    fp_filter = make_pipeline(fp, fl_1)
    fp_gen = fp_filter(dir_path)

    assert p_target_files == list(fp_gen)


def test_filter_date_range() -> None:
    for f in test_files:
        path_check(f)

    re_time = r'\d+T\d+'
    dt_from = datetime(2024, 4, 11)
    dt_to = datetime(2024, 4, 13)

    ''' Answers to the test '''
    target_files = [f for f in test_files if re.search(re_time, f)]
    target_files = [f for f in target_files if ('20240411' in f) | ('20240412' in f)]
    # print(target_files)  # pytest -s
    p_target_files = [Path(f) for f in target_files]

    ''' Processing by the module '''
    fp = PickFilesBySuffix(['.txt', '.text'], recursive=True)

    fl_1 = FilterWithDateRange(
        re_time=re_time,
        dt_from=dt_from,
        dt_to=dt_to,
    )

    fp_filter = make_pipeline(fp, fl_1)
    fp_gen = fp_filter(dir_path)

    assert p_target_files == list(fp_gen)


def test_filter_reg_exp() -> None:
    for f in test_files:
        path_check(f)

    target_list = ['DDDDDD111111', 'DDDDDD333333']

    ''' Answers to the test '''
    target_files = [f for f in test_files if any([t in f for t in target_list])]
    # print(target_files)  # pytest -s
    p_target_files = [Path(f) for f in target_files]

    ''' Processing by the module '''
    fp = PickFilesBySuffix(['.txt', '.text'], recursive=True)

    fl_1 = FilterWithRegExp(re_list=target_list)

    fp_filter = make_pipeline(fp, fl_1)
    fp_gen = fp_filter(dir_path)

    assert p_target_files == list(fp_gen)
