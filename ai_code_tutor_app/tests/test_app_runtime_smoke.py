from __future__ import annotations

import importlib
import sys
import types


class AttrDict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name, value):
        self[name] = value


class FakeElement:
    def __init__(self, streamlit_module: "FakeStreamlit"):
        self._st = streamlit_module

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def __getattr__(self, name):
        return getattr(self._st, name)


class FakeStreamlit(types.ModuleType):
    def __init__(self):
        super().__init__("streamlit")
        self.session_state = AttrDict()
        self.sidebar = FakeElement(self)

    def set_page_config(self, **kwargs):
        return None

    def markdown(self, *args, **kwargs):
        return None

    def header(self, *args, **kwargs):
        return None

    def subheader(self, *args, **kwargs):
        return None

    def write(self, *args, **kwargs):
        return None

    def caption(self, *args, **kwargs):
        return None

    def success(self, *args, **kwargs):
        return None

    def warning(self, *args, **kwargs):
        return None

    def error(self, *args, **kwargs):
        return None

    def info(self, *args, **kwargs):
        return None

    def divider(self, *args, **kwargs):
        return None

    def code(self, *args, **kwargs):
        return None

    def progress(self, *args, **kwargs):
        return FakeElement(self)

    def metric(self, *args, **kwargs):
        return None

    def text_input(self, label, value="", **kwargs):
        return value

    def text_area(self, label, value="", **kwargs):
        return value

    def selectbox(self, label, options, index=0, **kwargs):
        options = list(options)
        return options[index] if options else None

    def radio(self, label, options, index=0, **kwargs):
        options = list(options)
        if index is None:  # st.radio(..., index=None) starts with no selection
            return None
        return options[index] if options else None

    def checkbox(self, label, value=False, **kwargs):
        return value

    def toggle(self, label, value=False, **kwargs):
        return value

    def slider(self, label, min_value=None, max_value=None, value=None, step=None, **kwargs):
        return value if value is not None else min_value

    def button(self, *args, **kwargs):
        return False

    def form_submit_button(self, *args, **kwargs):
        return False

    def download_button(self, *args, **kwargs):
        return False

    def file_uploader(self, *args, **kwargs):
        return None

    def chat_input(self, *args, **kwargs):
        return None

    def rerun(self, *args, **kwargs):
        return None

    def columns(self, spec, **kwargs):
        count = spec if isinstance(spec, int) else len(spec)
        return [FakeElement(self) for _ in range(count)]

    def tabs(self, labels):
        return [FakeElement(self) for _ in labels]

    def expander(self, *args, **kwargs):
        return FakeElement(self)

    def container(self, *args, **kwargs):
        return FakeElement(self)

    def form(self, *args, **kwargs):
        return FakeElement(self)

    def chat_message(self, *args, **kwargs):
        return FakeElement(self)


def test_app_imports_with_fake_streamlit_without_name_errors(monkeypatch):
    fake_streamlit = FakeStreamlit()
    monkeypatch.setitem(sys.modules, "streamlit", fake_streamlit)
    sys.modules.pop("app", None)
    imported = importlib.import_module("app")
    assert imported.LESSON_IDS[0].startswith("01-")
