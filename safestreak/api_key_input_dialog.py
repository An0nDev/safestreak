import typing
import tkinter

import safestreak.hypixel_api as hypixel_api


class APIKeyPrompt(tkinter.Toplevel):
    def __init__(self, root: tkinter.Tk):
        super().__init__(root)
        self.root = root

        self.initial_frame = tkinter.Frame(self)
        self.initial_text = tkinter.Label(self.initial_frame, text="Verifying your API key...")
        self.initial_text.pack()
        self.initial_frame.pack()

        self.input_frame = tkinter.Frame(self)
        self.error_text = tkinter.Label(self.input_frame, text="Try again.", fg="red")
        self.showing_error_text = False
        self.label = tkinter.Label(self.input_frame, text="Enter your API key: ")
        self.label.grid(row=1, column=0)
        self.api_key_var = tkinter.StringVar(self.input_frame)
        self.input = tkinter.Entry(self.input_frame, textvariable=self.api_key_var)
        self.input.grid(row=1, column=1)
        self.submit_button = tkinter.Button(self.input_frame, text="Submit", command=self._submit)
        self.submit_button.grid(row=2, column=0, columnspan=2)

        self.api_key: typing.Optional[str] = None
        self.username: typing.Optional[str] = None

    def retrieve(self, orig_api_key: typing.Optional[str]) -> (typing.Optional[str], str):
        try:
            self.username = hypixel_api.test(api_key=orig_api_key)
        except hypixel_api.InvalidAPIKeyException:
            self.initial_frame.pack_forget()
            self.input_frame.pack()
            self.root.wait_window(self)
            if self.api_key is None:
                raise Exception("API key prompt was closed prematurely")
            return self.api_key, self.username

        self.destroy()
        return None, self.username  # (given key was OK)

    def _submit(self):
        api_key = self.api_key_var.get()

        try:
            self.username = hypixel_api.test(api_key=api_key)
        except hypixel_api.InvalidAPIKeyException:
            if not self.showing_error_text:
                self.error_text.grid(row=0, column=0, columnspan=2)
                self.showing_error_text = True
            self.api_key_var.set("")
            return

        self.api_key = api_key
        self.destroy()


def prompt_for_api_key(root: tkinter.Tk, initial_api_key: typing.Optional[str]) -> (typing.Optional[str], str):
    return APIKeyPrompt(root).retrieve(initial_api_key)
