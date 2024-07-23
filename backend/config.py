import os
from typing import Any, Callable, Dict, List, Literal, Optional, Union

from pydantic.dataclasses import Field, dataclass

from backend.logger import logger
from backend.version import __version__

BACKEND_ROOT = os.path.dirname(__file__)
PACKAGE_ROOT = os.path.dirname(os.path.dirname(BACKEND_ROOT))

APP_ROOT = os.getcwd()


DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
DEFAULT_ROOT_PATH = ""

# create the directory to store the upload files
config_dir = os.path.join(APP_ROOT, ".backend")
config_file = os.path.join(config_dir, "config.toml")
config_translation_dir = os.path.join(config_dir, "transaltion")

DEFAULT_CONFIG_STR = f"""[project]
# Whether to enable telemetry (default: true). No personal data is collected.
enable_telemetry = true


# List of environment variables to be provided by each user to use the app.
user_env = []

# Duration (in seconds) during which the session is saved when the connection is lost
session_timeout = 3600

# Enable third parties caching (e.g LangChain cache)
cache = false

# Authorized origins
allow_origins = ["*"]

# Follow symlink for asset mount (see https://github.com/Chainlit/chainlit/issues/317)
# follow_symlink = false

[features]
# Process and display HTML in messages. This can be a security risk (see https://stackoverflow.com/questions/19603097/why-is-it-dangerous-to-render-user-generated-html-or-javascript)
unsafe_allow_html = false

# Process and display mathematical expressions. This can clash with "$" characters in messages.
latex = false

# Automatically tag threads with the current chat profile (if a chat profile is used)
auto_tag_thread = true

# Authorize users to spontaneously upload files with messages
[features.spontaneous_file_upload]
    enabled = true
    accept = ["*/*"]
    max_files = 20
    max_size_mb = 500

[features.audio]
    # Threshold for audio recording
    min_decibels = -45
    # Delay for the user to start speaking in MS
    initial_silence_timeout = 3000
    # Delay for the user to continue speaking in MS. If the user stops speaking for this duration, the recording will stop.
    silence_timeout = 1500
    # Above this duration (MS), the recording will forcefully stop.
    max_duration = 15000
    # Duration of the audio chunks in MS
    chunk_duration = 1000
    # Sample rate of the audio
    sample_rate = 44100

edit_message = true

[UI]
# Name of the assistant.
name = "Assistant"

# Description of the assistant. This is used for HTML tags.
# description = ""

# Large size content are by default collapsed for a cleaner ui
default_collapse_content = true

# Chain of Thought (CoT) display mode. Can be "hidden", "tool_call" or "full".
cot = "full"

# Link to your github repo. This will add a github button in the UI's header.
# github = ""

# Specify a CSS file that can be used to customize the user interface.
# The CSS file can be served from the public directory or via an external link.
# custom_css = "/public/test.css"

# Specify a Javascript file that can be used to customize the user interface.
# The Javascript file can be served from the public directory.
# custom_js = "/public/test.js"

# Specify a custom font url.
# custom_font = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap"

# Specify a custom meta image url.
# custom_meta_image_url = "https://chainlit-cloud.s3.eu-west-3.amazonaws.com/logo/chainlit_banner.png"

# Specify a custom build directory for the frontend.
# This can be used to customize the frontend code.
# Be careful: If this is a relative path, it should not start with a slash.
# custom_build = "./public/build"

[UI.theme]
    default = "dark"
    #layout = "wide"
    #font_family = "Inter, sans-serif"
# Override default MUI light theme. (Check theme.ts)
[UI.theme.light]
    #background = "#FAFAFA"
    #paper = "#FFFFFF"

    [UI.theme.light.primary]
        #main = "#F80061"
        #dark = "#980039"
        #light = "#FFE7EB"
    [UI.theme.light.text]
        #primary = "#212121"
        #secondary = "#616161"

# Override default MUI dark theme. (Check theme.ts)
[UI.theme.dark]
    #background = "#FAFAFA"
    #paper = "#FFFFFF"

    [UI.theme.dark.primary]
        #main = "#F80061"
        #dark = "#980039"
        #light = "#FFE7EB"
    [UI.theme.dark.text]
        #primary = "#EEEEEE"
        #secondary = "#BDBDBD"

[meta]
generated_by = "{__version__}"""


@dataclass()
class RunSetting:
    module_name: Optional[str] = None
    host: str = DEFAULT_HOST
    port: str = DEFAULT_PORT
    root_path: str = DEFAULT_ROOT_PATH
    headless: bool = False
    watch: bool = False
    no_cache: bool = False
    debug: bool = False
    ci: bool = False


@dataclass()
class BackendConfig:
    root: APP_ROOT  # type: ignore
    backend_service: str
    run: RunSetting

    def load_translation(self, language: str):
        translation = {}
        default_language = "en-US"
        translation["default_language":default_language]
        return translation.get(language, translation.get(default_language))


def init_config(log=False):

    if not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)
        with open(config_dir, "w", encoding="utf-8") as f:
            f.write(DEFAULT_CONFIG_STR)
            logger.info(f"Created default config file at {config_file}")
    elif log:
        logger.info(f"Config file already exists at {config_file}")


init_config(log=True)
