from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from instagrapi.types import Location


@dataclass
class InstagramPostData:
    path: Path
    caption: str
    location: Optional[Location] = None
