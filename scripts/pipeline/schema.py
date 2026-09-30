"""
Data models and schema definitions for multi-agent slide generation.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any

@dataclass
class BrowserAction:
    type: str  # 'navigate', 'click', 'fill', 'wait', 'wait_for_selector'
    selector: Optional[str] = None
    value: Optional[str] = None
    ms: Optional[int] = 1000

@dataclass
class SlideDefinition:
    step_id: str
    filename: str
    heading: str
    where: str
    steps: List[str]
    note: str = ""
    target_route: str = "/settings"
    actions: List[Dict[str, Any]] = field(default_factory=list)
    screen_filename: str = ""

@dataclass
class PartSpecification:
    part_id: str
    part_title: str
    output_dir: str
    slides: List[SlideDefinition]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
