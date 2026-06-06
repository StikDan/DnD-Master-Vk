from typing import Dict, List
from .state import State


STATE_FILES: Dict[State, List[str]] = {
    State.NONE: [],
    
    State.EXPLORATION: [
        "systemPrompt.md",
        "characters.md",
        "adventure.md",
        "exploreRules.md",
        "eid.md",
        "transitionRules.md"
    ],
    
    State.COMBAT: [
        "systemPrompt.md",
        "characters.md",
        "adventure.md",
        "fightRules.md",
        "eid.md",
        "drakman.md",
        "transitionRules.md"
    ],
    
    State.SOCIAL: [
        "systemPrompt.md",
        "characters.md",
        "adventure.md",
        "dialogRules.md",
        "eid.md",
        "drakman.md",
        "transitionRules.md"
    ],
    
    State.REST: [
        "systemPrompt.md",
        "characters.md",
        "adventure.md",
        "restRules.md",
        "eid.md",
        "transitionRules.md"
    ],
}