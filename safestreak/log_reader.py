import copy
import pathlib, os.path
import re
import sys

import watchdog.events, watchdog.observers, watchdog.observers.polling

class LogReader:
    log_file_path = pathlib.Path.home () / ".lunarclient" / "offline" / "multiver" / "logs"
    log_file_name = "latest.log"
    log_file_full_path_str = str (log_file_path / log_file_name)
    def __init__ (self, app):
        self.app = app

        self.last_size = self._calc_size ()

        self.event_handler = watchdog.events.FileSystemEventHandler ()
        self.event_handler.on_modified = self._on_modification
        self.observer = watchdog.observers.polling.PollingObserver () if sys.platform == "win32" else watchdog.observers.Observer ()
        # print (f"scheduling on {self.log_file_path}")
        self.observer.schedule (self.event_handler, str (self.log_file_path))
        self.observer.start ()
    def _calc_size (self): return os.path.getsize (self.log_file_full_path_str)
    def _on_modification (self, event: watchdog.events.FileModifiedEvent):
        # print (f"file at {event.src_path} modified, type of event is {type (event)}")
        if event.src_path != self.log_file_full_path_str:
            # print (f"{event.src_path} != {self.log_file_full_path_str}, returning")
            return
        try:
            new_size = self._calc_size ()
        except FileNotFoundError:
            # print ("FileNotFoundError, returning")
            return
        size_diff = new_size - self.last_size
        offset = copy.deepcopy (self.last_size)
        self.last_size = new_size
        if size_diff < 1:
            # print (f"size_diff ({size_diff}) < 1, returning")
            return
        # print (f"new size is {new_size}, size diff {size_diff} at offset {offset}")
        with open (self.log_file_full_path_str, "rb") as log_file:
            log_file.seek (offset)
            new_text_bytes = log_file.read (size_diff)
        # print (new_text_bytes)
        
        new_text = new_text_bytes.decode ("utf-8", "ignore")
        # print (f"new text is {new_text}")
        lines = new_text.strip ().splitlines ()
        first = True
        for line in lines:
            success = self._feed_line (line, first)
            if first:
                if not success: break
                first = False
    def _feed_line (self, line: str, first: bool) -> bool:
        match = re.fullmatch (r"\[[0-9]{2}:[0-9]{2}:[0-9]{2}\] \[Client thread\/INFO\]: \[CHAT\] (?P<message>.+)", line)
        if match is None:
            if not first:
                message = line
            else:
                # print (f"line {line} is not a chat message")
                return False
        else:
            message = match.group ("message")
        for escape_code in (f"§{escape_char}" for escape_char in "0123456789abcdefklmnor"): message = message.replace (escape_code, "")
        self.app.chat_processor.process (message)
        return True
