from typing import Dict, List
from .state import State


STATE_FILES: Dict[State, List[str]] = {
    State.NONE: [],
    
    State.EXPLORATION: [
        "systemPrompt.md",
        "characters.md",
        "adventure.md",
        "exploreRules.md",
        "transitionRules.md"
    ],
    
    State.COMBAT: [
        "systemPrompt.md",
        "characters.md",
        "adventure.md",
        "fightRules.md",
        "transitionRules.md"
    ],
    
    State.SOCIAL: [
        "systemPrompt.md",
        "characters.md",
        "adventure.md",
        "dialogRules.md",
        "transitionRules.md"
    ],
    
    State.REST: [
        "systemPrompt.md",
        "characters.md",
        "adventure.md",
        "restRules.md",
        "transitionRules.md"
    ],
}