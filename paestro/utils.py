import pytz
import random
import re
import string
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from PIL import Image
from io import BytesIO
import base64
import gzip
import io
import os
import ssl
import socket
import OpenSSL
import json
import requests
import paramiko
import time

class Paestro:
    """Utility class with static methods for common operations."""

    @staticmethod
    def test() -> None:
        """Prints 'paestro' to the console. Test method."""
        print("paestro")

    @staticmethod
    def random_id() -> str:
        """Generates a random hexadecimal ID of 16 characters.

        Returns:
            str: String with 16 random hexadecimal characters.
        """
        return ''.join(random.choices('abcdef0123456789', k=16))

    @staticmethod
    def random_string(
        length: int, chars: str = (string.ascii_letters + string.digits)
    ) -> str:
        """Generates a random string with the specified length.

        Args:
            length (int): Length of the string to be generated.
            chars (str, optional): Characters to be used in generation. Defaults to
                uppercase letters, lowercase letters and digits.

        Returns:
            str: Random string with the specified length.
        """
        return ''.join(random.choices(chars, k=length))

    @staticmethod
    def datetime(custom_tz: Optional[int] = None) -> datetime:
        """Returns the current date and time.

        Args:
            custom_tz (int, optional): Timezone offset in hours. If None, uses
                São Paulo timezone.

        Returns:
            datetime: Datetime object with the current date and time.
        """
        if custom_tz is not None:
            now = datetime.now()
            now = now + timedelta(hours=custom_tz)
            return now
        else:
            tz = pytz.timezone("America/Sao_Paulo") 
            return datetime.now(tz)
        
    @staticmethod
    def dateCompare(date1: datetime, date2: datetime) -> int:
        """Compares two dates and returns the comparison result.

        Args:
            date1 (datetime): First date to be compared.
            date2 (datetime): Second date to be compared.

        Returns:
            int: 1 if date1 > date2, -1 if date1 < date2, 0 if date1 == date2.

        Raises:
            TypeError: If date1 or date2 are not datetime objects.
        """
        if not isinstance(date1, datetime) or not isinstance(date2, datetime):
            raise TypeError("date1 and date2 must be datetime objects")
        if date1 > date2:
            return 1
        elif date1 < date2:
            return -1
        else:
            return 0

    @staticmethod
    def unitToSeconds(value: Union[int, float], unit: str) -> Union[int, float]:
        """Converts a value from a time unit to seconds.

        Args:
            value (int | float): Value to be converted.
            unit (str): Time unit. One of: 'seconds', 'minutes', 'hours',
                'days', 'weeks', 'months', 'years'.

        Returns:
            int | float: Value converted to seconds.

        Raises:
            ValueError: If the unit is not one of the valid options.
        """
        if unit == 'seconds':
            return value
        elif unit == 'minutes':
            return value * 60
        elif unit == 'hours':
            return value * 60 * 60
        elif unit == 'days':
            return value * 60 * 60 * 24
        elif unit == 'weeks':
            return value * 60 * 60 * 24 * 7
        elif unit == 'months':
            return value * 60 * 60 * 24 * 30
        elif unit == 'years':
            return value * 60 * 60 * 24 * 365
        else:
            raise ValueError("unit must be seconds, minutes, hours, days, weeks, months or years")
        
    @staticmethod
    def secondsToUnit(seconds: Union[int, float], unit: str) -> float:
        """Converts a value in seconds to another time unit.

        Args:
            seconds (int | float): Value in seconds to be converted.
            unit (str): Target time unit. One of: 'seconds', 'minutes',
                'hours', 'days', 'weeks', 'months', 'years'.

        Returns:
            float: Value converted to the specified unit.

        Raises:
            ValueError: If the unit is not one of the valid options.
        """
        if unit == 'seconds':
            return seconds
        elif unit == 'minutes':
            return seconds / 60
        elif unit == 'hours':
            return seconds / 60 / 60
        elif unit == 'days':
            return seconds / 60 / 60 / 24
        elif unit == 'weeks':
            return seconds / 60 / 60 / 24 / 7
        elif unit == 'months':
            return seconds / 60 / 60 / 24 / 30
        elif unit == 'years':
            return seconds / 60 / 60 / 24 / 365
        else:
            raise ValueError("unit must be seconds, minutes, hours, days, weeks, months or years")
        
    @staticmethod
    def dateAdd(
        date: datetime, value: Union[int, float], unit: str
    ) -> datetime:
        """Adds a time value to a date.

        Args:
            date (datetime): Base date to add the value to.
            value (int | float): Value to be added.
            unit (str): Time unit. One of: 'seconds', 'minutes', 'hours',
                'days', 'weeks', 'months', 'years', 'datetime'. If 'datetime',
                the value is treated as seconds directly.

        Returns:
            datetime: New date with the value added.

        Raises:
            TypeError: If date is not a datetime object.
        """
        if not isinstance(date, datetime):
            raise TypeError("date must be a datetime object")
        if unit == 'datetime':
            return date + timedelta(seconds=value)
        else:
            return date + timedelta(seconds=Paestro.unitToSeconds(value, unit))
        
    @staticmethod
    def secondsBetween(date1: datetime, date2: datetime) -> float:
        """Calculates the absolute difference in seconds between two dates.

        Args:
            date1 (datetime): First date.
            date2 (datetime): Second date.

        Returns:
            float: Absolute difference in seconds between the two dates.

        Raises:
            TypeError: If date1 or date2 are not datetime objects.
        """
        if not isinstance(date1, datetime) or not isinstance(date2, datetime):
            raise TypeError("date1 and date2 must be datetime objects")
        
        return abs((date2 - date1).total_seconds())

    @staticmethod
    def dateToJsDate(date: datetime) -> Optional[str]:
        """Converts a datetime object to JavaScript-compatible format (ISO string).

        Args:
            date (datetime): Date to be converted.

        Returns:
            str | None: String in ISO format (with 'T' instead of space), or
                None if date is not a datetime object.
        """
        if not isinstance(date, datetime):
            return None
        return str(date).replace(' ', 'T')

    @staticmethod
    def fill_zeros(value: Union[int, str], length: int) -> str:
        """Pads a value with leading zeros until it reaches the specified length.

        Args:
            value (int | str): Value to be padded. Will be converted to string.
            length (int): Desired length of the resulting string.

        Returns:
            str: String padded with leading zeros.
        """
        return str(value).zfill(length)

    @staticmethod
    def randomize_list(items: List[Any]) -> List[Any]:
        """Randomly shuffles the elements of a list in place.

        Args:
            items (list): List to be shuffled. Modified in place.

        Returns:
            list: The same list (shuffled) passed as parameter.
        """
        random.shuffle(items)
        return items

    @staticmethod
    def random_int(min_val: int, max_val: int) -> int:
        """Generates a random integer within a range.

        Args:
            min_val (int): Minimum value (inclusive).
            max_val (int): Maximum value (inclusive).

        Returns:
            int: Random integer between min_val and max_val (inclusive).
        """
        return random.randint(min_val, max_val)

    @staticmethod
    def seconds_to_duration(seconds: Union[int, float]) -> str:
        """Converts seconds to a human-readable duration string in Portuguese.

        Args:
            seconds (int | float): Value in seconds to be converted.

        Returns:
            str: Formatted string (e.g., "2 dias, 3 horas e 15 minutos").
        """
        units = [
            (24 * 3600, "dia"),
            (3600, "hora"),
            (60, "minuto"),
            (1, "segundo"),
        ]
        result = []
        for divisor, unit in units:
            value, seconds = divmod(seconds, divisor)
            if value > 0:
                result.append(f"{value} {unit}{'s' if value > 1 else ''}")

        if len(result) > 1:
            return " e ".join([", ".join(result[:-1]), result[-1]])
        else:
            return result[0]
        
    @staticmethod
    def split_chunks(
        array: Union[List[Any], str], chunk_size: int = 1
    ) -> List[Any]:
        """Splits a list or string into chunks of the specified size.

        Args:
            array (list | str): List or string to be split.
            chunk_size (int, optional): Size of each chunk. Defaults to 1.

        Returns:
            list: List containing the chunks of the original array.
        """
        return [array[i:i+chunk_size] for i in range(0, len(array), chunk_size)]

    @staticmethod
    def random_choice(array: Union[List[Any], str]) -> Any:
        """Selects a random element from a list or string.

        Args:
            array (list | str): List or string from which to select an element.

        Returns:
            Any: Random element from the array.
        """
        return random.choice(array)

    @staticmethod
    def string_pad_left(text: str, length: int, char: str = ' ') -> str:
        """Pads a string on the left until it reaches the specified length.

        Args:
            text (str): String to be padded.
            length (int): Desired length of the resulting string.
            char (str, optional): Character used for padding. Defaults to ' '.

        Returns:
            str: String padded to the left.
        """
        return char * (length - len(text)) + text

    @staticmethod
    def string_pad_right(text: str, length: int, char: str = ' ') -> str:
        """Pads a string on the right until it reaches the specified length.

        Args:
            text (str): String to be padded.
            length (int): Desired length of the resulting string.
            char (str, optional): Character used for padding. Defaults to ' '.

        Returns:
            str: String padded to the right.
        """
        return text + char * (length - len(text))

    @staticmethod
    def remove_duplicated_spaces(text: str) -> str:
        """Removes duplicated spaces, keeping only one space between words.

        Args:
            text (str): Text to be processed.

        Returns:
            str: Text with duplicated spaces removed.
        """
        return ' '.join(text.split())

    @staticmethod
    def date_weekday(date: datetime) -> int:
        """Returns the weekday of a date (1=Monday, 2=Tuesday, ..., 7=Sunday).

        Args:
            date (datetime): Date from which to get the weekday.

        Returns:
            int: Weekday number (1-7, where 1 is Monday and 7 is Sunday).
        """
        return [1,2,3,4,5,6,0][date.weekday()]

    @staticmethod
    def datetime_set_time(dt: datetime, time: str) -> datetime:
        """Sets the time of a datetime object while keeping the date.

        Args:
            dt (datetime): Datetime object to be modified.
            time (str): Time string in 'HH:MM:SS' format.

        Returns:
            datetime: New datetime object with the time set and microseconds zeroed.
        """
        hours, minutes, seconds = time.split(':')
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)
        return dt.replace(hour=hours, minute=minutes, second=seconds, microsecond=0)
    
    @staticmethod
    def msort(
        arr: List[Any], key: Optional[Union[str, List[str]]] = None
    ) -> List[Any]:
        """Sorts a list in place using the bubble sort algorithm.

        Args:
            arr (list): List to be sorted. Modified in place.
            key (str | list | None, optional): Key(s) for sorting if arr contains
                dictionaries. If None, sorts elements directly. If list, sorts
                by multiple keys in order.

        Returns:
            list: The same sorted list (modified in place).
        """
        def compare(a, b):
            if key is None:
                return a < b
            else:
                if type(key) == list:
                    for k in key:
                        if a[k] < b[k]:
                            return True
                        elif a[k] > b[k]:
                            return False
                    return False
                else:
                    return a[key] < b[key]
        
        while True:
            for i in range(len(arr)):
                if i == 0:
                    continue
                
                if (compare(arr[i], arr[i-1])):
                    arr[i], arr[i-1] = arr[i-1], arr[i]
                    break
            else:
                return arr
            
    @staticmethod
    def reduce_jpeg_quality(
        source_path: str, target_path: str, quality: int = 100
    ) -> None:
        """Reduces the quality of a JPEG image and saves it to a new file.

        Args:
            source_path (str): Path of the source JPEG file.
            target_path (str): Path where to save the image with reduced quality.
            quality (int, optional): Image quality (0-100). Defaults to 100.
        """
        im1 = Image.open(source_path)
        buffer = BytesIO()
        im1.save(buffer, "JPEG", quality=quality)
        with open(target_path, "wb") as handle:
            handle.write(buffer.getvalue())
            
    @staticmethod
    def file_to_base64(source_path: str) -> str:
        """Converts a file to base64 string.

        Args:
            source_path (str): Path of the file to be converted.

        Returns:
            str: Base64 string representing the file content.
        """
        with open(source_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
        
    @staticmethod
    def base64_to_file(base64_string: str, target_path: str) -> None:
        """Converts a base64 string to a file.

        Args:
            base64_string (str): Base64 string to be decoded.
            target_path (str): Path where to save the decoded file.
        """
        with open(target_path, "wb") as image_file:
            image_file.write(base64.b64decode(base64_string))
            
    @staticmethod
    def gzip_compress(text: str) -> bytes:
        """Compresses a string using gzip.

        Args:
            text (str): String to be compressed.

        Returns:
            bytes: Compressed data in gzip format.

        Raises:
            TypeError: If the input is not a string.
        """
        if not isinstance(text, str):
            raise TypeError("Input needs to be a string")

        bytes_buffer = io.BytesIO()
        with gzip.GzipFile(fileobj=bytes_buffer, mode='wb') as f:
            f.write(text.encode('utf-8'))
            
        compressed_bytes = bytes_buffer.getvalue()
        return compressed_bytes
    
    @staticmethod
    def gzip_decompress(compressed_bytes: bytes) -> str:
        """Decompresses gzip data to string.

        Args:
            compressed_bytes (bytes): Compressed data in gzip format.

        Returns:
            str: Decompressed string.

        Raises:
            TypeError: If the input is not bytes.
        """
        if not isinstance(compressed_bytes, bytes):
            raise TypeError("Input needs to be bytes")

        bytes_buffer = io.BytesIO(compressed_bytes)
        with gzip.GzipFile(fileobj=bytes_buffer, mode='rb') as f:
            decompressed_string = f.read().decode('utf-8')
        return decompressed_string
    
    @staticmethod
    def save_file_bytes(data: bytes, target_path: str) -> None:
        """Saves binary data to a file.

        Args:
            data (bytes): Binary data to be saved.
            target_path (str): File path where to save the data.
        """
        with open(target_path, "wb") as file:
            file.write(data)
            
    @staticmethod
    def read_file_bytes(source_path: str) -> bytes:
        """Reads the binary content of a file.

        Args:
            source_path (str): Path of the file to be read.

        Returns:
            bytes: Binary content of the file.
        """
        with open(source_path, "rb") as file:
            return file.read()
        
    @staticmethod
    def gzip_compress_bytes(data: bytes) -> bytes:
        """Compresses binary data using gzip.

        Args:
            data (bytes): Binary data to be compressed.

        Returns:
            bytes: Compressed data in gzip format.

        Raises:
            TypeError: If the input is not bytes.
        """
        if not isinstance(data, bytes):
            raise TypeError("Input needs to be bytes")

        bytes_buffer = io.BytesIO()
        with gzip.GzipFile(fileobj=bytes_buffer, mode='wb') as f:
            f.write(data)
        return bytes_buffer.getvalue()
    
    @staticmethod
    def gzip_decompress_bytes(compressed_bytes: bytes) -> bytes:
        """Decompresses gzip data to binary data.

        Args:
            compressed_bytes (bytes): Compressed data in gzip format.

        Returns:
            bytes: Decompressed data.

        Raises:
            TypeError: If the input is not bytes.
        """
        if not isinstance(compressed_bytes, bytes):
            raise TypeError("Input needs to be bytes")

        bytes_buffer = io.BytesIO(compressed_bytes)

        with gzip.GzipFile(fileobj=bytes_buffer, mode='rb') as f:
            decompressed_bytes = f.read()

        return decompressed_bytes
    
    @staticmethod
    def string_to_datetime(text: str, format: str = '%Y-%m-%dT%H:%M:%S.%fZ') -> datetime:
        """Converts a string to a datetime object.

        Args:
            text (str): String to be converted.
            format (str, optional): Format of the string. Defaults to '%Y-%m-%dT%H:%M:%S.%fZ'.

        Returns:
            datetime: Datetime object.
        """
        return datetime.strptime(text, format)
    
    @staticmethod
    def get_ssl_info(domain: str, max_tries: int = 3) -> Optional[Dict[str, Any]]:
        """Retrieves SSL certificate information for a domain.

        Connects to the domain on port 443, fetches the certificate and returns
        a dictionary with subject, issuer, serial number, version, validity
        dates and extensions. Keys are in snake_case. Returns None if all
        attempts fail.

        Args:
            domain (str): Domain name to query (e.g. "example.com").
            max_tries (int, optional): Maximum number of connection attempts.
                Defaults to 3.

        Returns:
            Optional[Dict[str, Any]]: Certificate data (subject, issuer,
                serial_number, version, valid_from, valid_to, plus extension
                fields), or None if unable to retrieve the certificate.
        """
        def get_certificate(host: str, port: int = 443, timeout: int = 10) -> str:
            context = ssl.create_default_context()
            conn = socket.create_connection((host, port))
            sock = context.wrap_socket(conn, server_hostname=host)
            sock.settimeout(timeout)
            try:
                der_cert = sock.getpeercert(True)
            finally:
                sock.close()
            return ssl.DER_cert_to_PEM_cert(der_cert)
        
        for i in range(max_tries):
            try:
                certificate = get_certificate(domain)
                x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate)
                
                result = {
                    'subject': dict(x509.get_subject().get_components()),
                    'issuer': dict(x509.get_issuer().get_components()),
                    'serial_number': x509.get_serial_number(),
                    'version': x509.get_version(),
                    'valid_from': datetime.strptime(x509.get_notBefore().decode('utf-8'), '%Y%m%d%H%M%SZ'),
                    'valid_to': datetime.strptime(x509.get_notAfter().decode('utf-8'), '%Y%m%d%H%M%SZ'),
                }

                extensions = (x509.get_extension(i) for i in range(x509.get_extension_count()))
                extension_data = {e.get_short_name(): str(e) for e in extensions}
                result.update(extension_data)


                def convert_to_strings(data):
                    if isinstance(data, bytes):
                        return data.decode('utf-8')
                    elif isinstance(data, dict):
                        return dict(map(convert_to_strings, data.items()))
                    elif isinstance(data, list):
                        return list(map(convert_to_strings, data))
                    elif isinstance(data, tuple):
                        return tuple(map(convert_to_strings, data))
                    else:
                        return data

                result = convert_to_strings(result)
                result = json.dumps(result, default=str)
                result = json.loads(result)
                
                result['valid_from'] = datetime.strptime(result['valid_from'], '%Y-%m-%d %H:%M:%S')
                result['valid_to'] = datetime.strptime(result['valid_to'], '%Y-%m-%d %H:%M:%S')
                
                def camel_to_snake(camel_case_string):
                    snake_case_string = ""
                    for i, char in enumerate(camel_case_string):
                        if i > 0 and char.isupper():
                            snake_case_string += "_"
                        snake_case_string += char
                    return snake_case_string.lower()
                
                new_result = {}
                for key, value in result.items():
                    new_result[camel_to_snake(key)] = value
                
                return new_result
            except Exception as e:
                print(f'Error: {e}')
                print(f'Attempt {i+1} of {max_tries}')
                pass
            
        return None
    
    @staticmethod
    def get_url_base64(url: str) -> str:
        """Gets the base64 encoded content of a URL.

        Args:
            url (str): URL to be fetched.

        Returns:
            str: Base64 encoded content of the URL.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        data = base64.b64encode(requests.get(url, headers=headers, timeout=120).content).decode("utf-8")
        return data
    
    @staticmethod
    def listdir(path: str) -> List[str]:
        """Lists the contents of a directory.

        Args:
            path (str): Path of the directory to be listed.

        Returns:
            List[str]: List of files and directories in the directory.
        """
        return os.listdir(path)
    
    @staticmethod
    def base64_encode(data: bytes) -> str:
        """Encodes data to base64.

        Args:
            data (bytes): Data to be encoded.

        Returns:
            str: Base64 encoded data.
        """
        return base64.b64encode(data.encode()).decode()
    
    @staticmethod
    def base64_decode(base64_string: str) -> bytes:
        """Decodes base64 data to bytes.

        Args:
            base64_string (str): Base64 encoded data.

        Returns:
            bytes: Decoded bytes.
        """
        return base64.b64decode(base64_string.encode())
    
    @staticmethod
    def ssh_exec(cmd: str, host: str, username: str, password: str, pty: bool = False) -> tuple[str, List[str], float]:
        """Executes a command on a remote server.

        Args:
            cmd (str): Command to be executed.
            host (str): Host of the remote server.
            username (str): Username of the remote server.
            password (str): Password of the remote server.
            pty (bool, optional): Whether to allocate a pseudo-terminal for the
                command. Required for interactive shells (e.g. "bash -ic") and
                for programs that only emit ANSI color codes when attached to a
                tty. Defaults to False.

        Returns:
            tuple[str, List[str], float]: (result, lines, delay in milliseconds)
        """
        start = time.time()

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd, get_pty=pty)
        ssh_stdout_content = ssh_stdout.read()
        ssh_stderr_content = ssh_stderr.read()
        ssh.close()

        ssh_stdout = ssh_stdout_content.decode('utf-8')
        ssh_stderr = ssh_stderr_content.decode('utf-8')
        
        ssh_stdout = ssh_stdout.replace('\\n', '\n').replace('\\r', '\r').replace('\\t', '\t')
        ssh_stderr = ssh_stderr.replace('\\n', '\n').replace('\\r', '\r').replace('\\t', '\t')
        
        result = ''
        if ssh_stdout.replace('\n', '') != '':
            result = ssh_stdout
        elif ssh_stderr.replace('\n', '') != '':
            result = ssh_stderr
        
        if (result.endswith('\n')):
            result = result[:-1]
            
        lines = result.split('\n')
        lines = list(filter(lambda x: x != '', lines))
    
        end = time.time()
        ms = (end - start) * 1000
        
        return result, lines, ms
    
    @staticmethod
    def ssh_send_file(localpath: str, remotepath: str, host: str, username: str, password: str) -> float:
        """Sends a file to a remote server via SFTP.

        Args:
            localpath (str): Local path of the file to send.
            remotepath (str): Remote destination path.
            host (str): Host of the remote server.
            username (str): Username of the remote server.
            password (str): Password of the remote server.

        Returns:
            float: Delay in milliseconds.
        """
        start = time.time()

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)
        sftp = ssh.open_sftp()
        sftp.put(localpath, remotepath)
        sftp.close()
        ssh.close()

        end = time.time()
        ms = (end - start) * 1000

        return ms

    @staticmethod
    def parse_ansi_modifiers(text_with_formats: str, ignore_extended_colors: bool = True) -> tuple[str, List[Dict[str, Any]]]:
        """Parses ANSI escape codes (e.g. colored SSH/terminal output) out of a string.

        Args:
            text_with_formats (str): Text containing ANSI SGR escape sequences
                (e.g. "\\x1b[01;34m").
            ignore_extended_colors (bool): When True (default), 256-color and
                truecolor sequences (38/48;5;n and 38/48;2;r;g;b) are consumed but
                not emitted as styling. When False, they produce "color256(n)" and
                "rgb(r,g,b)" values.

        Returns:
            tuple[str, List[Dict[str, Any]]]: (plain_text, formats), where
                plain_text has all escape sequences stripped, and formats is a
                list of dicts with 'start', 'end' (offsets into plain_text) and
                'format' (a dict describing the modifiers, e.g. {'bold': True,
                'text': 'blue'}, or {} for unformatted segments).
        """
        def fill_format_gaps(plain_text, formats):
            filled = []
            pos = 0
            for f in formats:
                if f['start'] > pos:
                    filled.append({'start': pos, 'end': f['start'], 'format': None})
                filled.append(f)
                pos = f['end']
            if pos < len(plain_text):
                filled.append({'start': pos, 'end': len(plain_text), 'format': None})
            return filled

        def parse_format(format_code):
            format_obj = {}
            if format_code is None:
                return format_obj
            modifiers = {
                "0": {},
                "1": {"bold": True},
                "2": {"dim": True},
                "3": {"italic": True},
                "4": {"undeline": True},
                "7": {"reverse": True},
                "8": {"invisible": True},
                "9": {"strikethrough": True},
            }
            colors = {
                "0": "black",
                "1": "red",
                "2": "green",
                "3": "yellow",
                "4": "blue",
                "5": "magenta",
                "6": "cyan",
                "7": "white"
            }
            items = format_code.split(";")
            i = 0
            while i < len(items):
                item = items[i].lstrip("0") or "0"

                # Extended color: 38/48 followed by 5;n (256-color) or 2;r;g;b (truecolor)
                if item in ("38", "48"):
                    key = "text" if item == "38" else "bg"
                    mode = items[i + 1] if i + 1 < len(items) else None
                    if mode == "5" and i + 2 < len(items):
                        if not ignore_extended_colors:
                            format_obj = format_obj | {key: "color256(" + items[i + 2] + ")"}
                        i += 3
                    elif mode == "2" and i + 4 < len(items):
                        if not ignore_extended_colors:
                            rgb = ",".join(items[i + 2:i + 5])
                            format_obj = format_obj | {key: "rgb(" + rgb + ")"}
                        i += 5
                    else:
                        i += 1
                    continue

                if item in modifiers:
                    format_obj = format_obj | modifiers[item]
                elif item in ("39", "49"):
                    pass  # default foreground/background — no styling
                elif len(item) == 2 and item[0] == "3" and item[1] in colors:
                    format_obj = format_obj | {"text": colors[item[1]]}
                elif len(item) == 2 and item[0] == "4" and item[1] in colors:
                    format_obj = format_obj | {"bg": colors[item[1]]}
                elif len(item) == 2 and item[0] == "9" and item[1] in colors:
                    format_obj = format_obj | {"text": "dark " + colors[item[1]]}
                elif len(item) == 3 and item[:2] == "10" and item[2] in colors:
                    format_obj = format_obj | {"bg": "dark " + colors[item[2]]}

                i += 1

            return format_obj

        ansi_re = re.compile(r'\x1b\[([0-9;]*)m')
        plain = []
        formats = []
        pos = 0
        cur_format = None
        cur_start = None
        last_end = 0

        for match in ansi_re.finditer(text_with_formats):
            text = text_with_formats[last_end:match.start()]
            plain.append(text)
            pos += len(text)

            code = match.group(1)
            is_reset = code in ('', '0', '00')

            if cur_format is not None:
                formats.append({'start': cur_start, 'end': pos, 'format': cur_format})
                cur_format = None

            if not is_reset:
                cur_format = code
                cur_start = pos

            last_end = match.end()

        tail = text_with_formats[last_end:]
        plain.append(tail)
        pos += len(tail)

        if cur_format is not None:
            formats.append({'start': cur_start, 'end': pos, 'format': cur_format})

        plain_text = ''.join(plain)

        formats = fill_format_gaps(plain_text, formats)
        for i in range(len(formats)):
            formats[i]["format"] = parse_format(formats[i]["format"])

        return plain_text, formats