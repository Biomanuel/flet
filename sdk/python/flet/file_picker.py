import json
from dataclasses import dataclass, field
from typing import Any, Optional, Union

from beartype import beartype
from beartype.typing import List

from flet.control import Control, OptionalNumber
from flet.control_event import ControlEvent
from flet.dropdown import Option
from flet.event_handler import EventHandler
from flet.ref import Ref

try:
    from typing import Literal
except:
    from typing_extensions import Literal

FileType = Literal["any", "media", "image", "video", "audio", "custom"]
FilePickerState = Literal["pickFiles", "saveFile", "getDirectoryPath"]


@dataclass
class FilePickerUploadFile:
    name: str
    upload_url: str
    method: str = field(default="PUT")


@dataclass
class FilePickerFile:
    name: str
    path: str
    size: int


class FilePickerResultEvent(ControlEvent):
    def __init__(self, path, files) -> None:
        self.path: Optional[str] = path
        self.files: Optional[List[FilePickerFile]] = None
        if files != None and isinstance(files, List):
            self.files = []
            for fd in files:
                self.files.append(FilePickerFile(**fd))


@dataclass
class FilePickerUploadEvent(ControlEvent):
    file_name: str
    progress: Optional[float]
    error: Optional[str]


class FilePicker(Control):
    def __init__(
        self,
        ref: Optional[Ref] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        on_result=None,
        on_upload=None,
    ):

        Control.__init__(
            self,
            ref=ref,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        def convert_result_event_data(e):
            d = json.loads(e.data)
            self.__result = FilePickerResultEvent(**d)
            return self.__result

        self.__on_result = EventHandler(convert_result_event_data)
        self._add_event_handler("result", self.__on_result.handler)

        def convert_upload_event_data(e):
            d = json.loads(e.data)
            return FilePickerUploadEvent(**d)

        self.__on_upload = EventHandler(convert_upload_event_data)
        self._add_event_handler("upload", self.__on_upload.handler)

        self.__result: Optional[FilePickerResultEvent] = None
        self.__upload: List[FilePickerUploadFile] = []
        self.__allowed_extensions: Optional[List[str]] = None
        self.on_result = on_result
        self.on_upload = on_upload

    def _get_control_name(self):
        return "filepicker"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("allowedExtensions", self.__allowed_extensions)
        self._set_attr_json("upload", self.__upload)

    def pick_files(
        self,
        dialog_title: Optional[str] = None,
        initial_directory: Optional[str] = None,
        file_type: Optional[FileType] = "any",
        allowed_extensions: Optional[List[str]] = None,
        allow_multiple: Optional[bool] = False,
    ):
        self.state = "pickFiles"
        self.dialog_title = dialog_title
        self.initial_directory = initial_directory
        self.file_type = file_type
        self.allowed_extensions = allowed_extensions
        self.allow_multiple = allow_multiple
        self.update()

    def save_file(
        self,
        dialog_title: Optional[str] = None,
        file_name: Optional[str] = None,
        initial_directory: Optional[str] = None,
        file_type: Optional[FileType] = "any",
        allowed_extensions: Optional[List[str]] = None,
    ):
        self.state = "saveFile"
        self.dialog_title = dialog_title
        self.file_name = file_name
        self.initial_directory = initial_directory
        self.file_type = file_type
        self.allowed_extensions = allowed_extensions
        self.update()

    def get_directory_path(
        self,
        dialog_title: Optional[str] = None,
        initial_directory: Optional[str] = None,
    ):
        self.state = "getDirectoryPath"
        self.dialog_title = dialog_title
        self.initial_directory = initial_directory
        self.update()

    def upload(self, files: List[FilePickerUploadFile]):
        self.__upload = files
        self.update()

    # state
    @property
    def state(self) -> Optional[FilePickerState]:
        return self._get_attr("state")

    @state.setter
    @beartype
    def state(self, value: Optional[FilePickerState]):
        self._set_attr("state", value)

    # result
    @property
    def result(self) -> Optional[FilePickerResultEvent]:
        return self.__result

    # dialog_title
    @property
    def dialog_title(self):
        return self._get_attr("dialogTitle")

    @dialog_title.setter
    def dialog_title(self, value):
        self._set_attr("dialogTitle", value)

    # file_name
    @property
    def file_name(self):
        return self._get_attr("fileName")

    @file_name.setter
    @beartype
    def file_name(self, value: Optional[str]):
        self._set_attr("fileName", value)

    # initial_directory
    @property
    def initial_directory(self):
        return self._get_attr("initialDirectory")

    @initial_directory.setter
    @beartype
    def initial_directory(self, value: Optional[str]):
        self._set_attr("initialDirectory", value)

    # file_type
    @property
    def file_type(self):
        return self._get_attr("fileType")

    @file_type.setter
    @beartype
    def file_type(self, value: Optional[FileType]):
        self._set_attr("fileType", value)

    # allowed_extensions
    @property
    def allowed_extensions(self) -> Optional[List[str]]:
        return self.__allowed_extensions

    @allowed_extensions.setter
    @beartype
    def allowed_extensions(self, value: Optional[List[str]]):
        self.__allowed_extensions = value

    # allow_multiple
    @property
    def allow_multiple(self) -> Optional[bool]:
        return self._get_attr("allowMultiple", data_type="bool", def_value=False)

    @allow_multiple.setter
    @beartype
    def allow_multiple(self, value: Optional[bool]):
        self._set_attr("allowMultiple", value)

    # on_result
    @property
    def on_result(self):
        return self.__on_result

    @on_result.setter
    def on_result(self, handler):
        self.__on_result.subscribe(handler)

    # on_upload
    @property
    def on_upload(self):
        return self.__on_upload

    @on_upload.setter
    def on_upload(self, handler):
        self.__on_upload.subscribe(handler)
