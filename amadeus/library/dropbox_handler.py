from io import BytesIO
from os.path import splitext

from requests import Response
from dropbox import Dropbox
from dropbox.files import ListFolderResult
from PIL import Image


def fetch_filenames(
    dbx_client:     Dropbox,
    file_directory: str,
    extension:      bool = True,
) -> list[str]:
    try:
        dbx_file_result: ListFolderResult = dbx_client.files_list_folder(
            file_directory,
        ).entries

        if extension:
            return [ file.name for file in dbx_file_result ]
        else:
            def clean_filename(filename: str) -> str:
                basename, _extension = splitext(filename)
                return basename

            return [ clean_filename(file.name) for file in dbx_file_result ]
    except Exception as exn:
        raise exn


def _compress_image(image: bytes) -> bytes:
    img = Image.open(BytesIO(image))
    image_buffer: BytesIO = BytesIO()
    img = img.convert('RGB')
    img.save(image_buffer, format='jpeg', optimize=True, quality=45)
    image_buffer.seek(0)

    return image_buffer.read()

def save_file(
    dbx_client: Dropbox,
    filename:   str,
    save_path:  str,
    file:       bytes,
):
    filename, extension = splitext(filename)
    file_to_save = None

    # HACK: I haven't figured a cleaner way to handle images yet.
    try:
        file_to_save = _compress_image(file)
        extension = '.jpg'
    except Exception as exn:
        print("Image compression failed, or file not an image.")
        print(exn)
        file_to_save = file

    try:
        dbx_client.files_upload(
            f    = file_to_save,
            path = f"{save_path}{filename}{extension}"
        )
    except Exception as exn:
        raise exn


def retrieve_streamable_file_response(
    dbx_client:    Dropbox,
    filename:      str,
    file_location: str,
) -> Response:
    path_to_download = f"{file_location}{filename}"
    _metadata, response = dbx_client.files_download(path_to_download)
    return response


def retrieve_file_content(
    dbx_client:    Dropbox,
    filename:      str,
    file_location: str,
) -> bytes:
    path_to_download = f"{file_location}{filename}"
    _metadata, response = dbx_client.files_download(path_to_download)
    return response.content


def retrieve_temporary_file_link(
    dbx_client:    Dropbox,
    filename:      str,
    file_location: str
) -> str:
    return dbx_client.files_get_temporary_link(f"{file_location}{filename}").link