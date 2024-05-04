from pathlib import Path

from pathobj_handler.filestem.picker import PickFilesBySuffix
from pathobj_handler.tool import make_pipeline

test_files = [
    './resource/sample/20240410T150525_DDDDDD111111_AAA.txt',
    './resource/sample/20240411T150625_DDDDDD111111_BBB.txt',
    './resource/sample/20240412T150725_DDDDDD222222_AAA.txt',
    './resource/sample/20240413T150825_DDDDDD333333_BBB.txt',
    './resource/sample/fuga_01.txt',
    './resource/sample/fuga_02.txt',
    './resource/sample/hoge_01.text',
    './resource/sample/hoge_02.text',
]


def path_check(path: str) -> None:
    p_path = Path(path)
    if p_path.exists():
        return
    p_path.parent.mkdir(parents=True, exist_ok=True)
    p_path.touch()


''' ------------ test_* functions ------------ '''


def test_picker() -> None:
    for f in test_files:
        path_check(f)

    ''' Answers to the test '''
    p_test_files = [Path(f) for f in test_files]

    ''' Processing by the module '''
    fp = PickFilesBySuffix(['.txt', '.text'], recursive=True)
    dir_path = './resource'

    file_path_gen = fp(dir_path)

    assert p_test_files == list(file_path_gen)
