# coding=UTF-8
#
# Copyright (C) 2015  Michell Stuttgart

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.

# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

from src.lib.pynocchio_exception import DependenceNotFoundException

try:
    import rarfile
except ImportError as err:
    msg = 'rarfile module not installed.\n' \
          'you not can load .rar and .cbr files.' \
          'Please install it using: sudo pip install rarfile\n'
    raise DependenceNotFoundException(msg)

from compact_file_loader import Loader
from utility import Utility
from src.lib.pynocchio_exception import LoadComicsException
from src.lib.pynocchio_exception import InvalidTypeFileException
from src.lib.pynocchio_exception import NoDataFindException
from page import Page


class RarLoader(Loader):

    EXTENSION = '.rar'

    def __init__(self, extension):
        super(RarLoader, self).__init__(extension)

    def load(self, file_name):
        try:
            rar = rarfile.RarFile(file_name, 'r')
        except rarfile.RarOpenError as excp:
            # self.done.emit()
            raise InvalidTypeFileException(excp.message)
        except IOError as excp:
            # self.done.emit()
            raise LoadComicsException(excp.strerror)

        name_list = rar.namelist()
        name_list.sort()

        # list_size = len(name_list)
        # count = 1
        aux = 100.0 / len(name_list)
        page_number = 1

        for idx, name in enumerate(name_list):
            # file_extension = Utility.get_file_extension(name)

            if Utility.get_file_extension(name).lower() in self.extension:
                # self.data.append({'data': rar.read(name), 'name': name})
                self.data.append(Page(rar.read(name), name, page_number))
                page_number += 1

            self.progress.emit(idx * aux)

            # count += 1

        # self.done.emit()
        rar.close()

        if not self.data:
            raise NoDataFindException


class CbrLoader(RarLoader):

    EXTENSION = '.cbr'

    def __init__(self, extension):
        super(CbrLoader, self).__init__(extension)