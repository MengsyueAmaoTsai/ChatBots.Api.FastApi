from typing import Optional


class WebApplicationOptions:
    args: Optional[list[str]] = None
    environment_name: Optional[str] = None
    application_name: Optional[str] = None
    content_root_path: Optional[str] = None
    web_root_path: Optional[str] = None
