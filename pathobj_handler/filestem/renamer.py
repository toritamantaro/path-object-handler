from typing import Generator, Iterator, List, Dict, Tuple, Union, Optional, overload, Type, Any, Callable

from pathlib import Path

from ..base import ProcessorBase, GenerateBase


class RenameFilesByCustomFunction(ProcessorBase):

    def __init__(
            self,
            rename_method: Callable[[str], str],
    ):
        """
        :param rename_method:
        """
        self._rename = rename_method

    def process_handling(
            self,
            file: Union[str, Path],
    ) -> Path:
        """
        :param file:
        :return:
        """
        if isinstance(file, str):
            p_file = Path(file)
        elif isinstance(file, Path):
            p_file = file
        else:
            raise TypeError(f"Type '{type(file)}' is not assignable to type '{type(Path)}'.")

        if not p_file.is_file():
            raise ValueError(f"Need to specify a file path. {p_file} is not a file.")

        stem = p_file.stem
        suffix = p_file.suffix
        new_stem = self._rename(stem)
        new_path = p_file.with_name(new_stem + suffix)
        p_r_file = p_file.rename(new_path)
        return p_r_file


if __name__ == '__main__':
    """
    python -m pathobj_handler.filestem.renamer
    """
    import re
    from pathobj_handler.filestem.picker import PickFilesBySuffix
    from pathobj_handler.tool import make_pipeline


    # file_path = './resource/sample/hoge_01.text'
    # # file_path = './resource/sample/hoge_01_add1.text'
    # p_file_path = Path(file_path)

    def add_stem(stem: str) -> str:
        return stem + "_add_"


    def del_stem(stem: str) -> str:
        stem = re.sub('_add_', '', stem)
        return stem


    rn_1 = RenameFilesByCustomFunction(rename_method=add_stem)
    rn_2 = RenameFilesByCustomFunction(rename_method=del_stem)

    fp = PickFilesBySuffix(['.txt', '.text'], recursive=True)
    # fp = PickFilesBySuffix('.txt', recursive=True)
    dir_path = './resource'

    # mp = make_pipeline(fp, rn_1)
    mp = make_pipeline(fp, rn_2)

    mp_gen = mp(dir_path)
    file_list = list(mp_gen)
    print(file_list)

    # # rename_pipe = make_pipeline(rn_1, rn_2)
    # # rename_pipe = make_pipeline(rn_1)
    # rename_pipe = make_pipeline(rn_2)
    #
    # rn_gen = rename_pipe(p_file_path)
    # print(next(rn_gen))
