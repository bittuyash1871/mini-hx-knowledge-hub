"""Ontology for the Mini HX Knowledge Hub.

Defines WHAT kinds of things exist (entity types)
and HOW they are allowed to connect (relationship types).
"""

# Entity types: the "box labels", each with a short description.
ENTITY_TYPES = {
    "ResearchMethod": "A way of studying users, e.g. usability testing",
    "ResearchGoal": "What a study wants to learn, e.g. task completion",
    "AccessibilityGuideline": "A rule so people with disabilities can use the product",
    "Workflow": "A process users complete, e.g. employee onboarding",
    "UIComponent": "A piece of interface, e.g. a form or button",
    "Document": "A source document in our knowledge repository",
}

# Relationship types: the allowed "arrows".
# Each is (from_type, relationship_name, to_type).
RELATIONSHIP_TYPES = [
    ("ResearchMethod", "SUPPORTS_GOAL", "ResearchGoal"),
    ("Workflow", "CONTAINS", "UIComponent"),
    ("Workflow", "EVALUATED_FOR", "ResearchGoal"),
    ("UIComponent", "MUST_MEET", "AccessibilityGuideline"),
    ("Document", "DESCRIBES", "ResearchMethod"),
    ("Document", "DESCRIBES", "AccessibilityGuideline"),
]

if __name__ == "__main__":
    print("Entity types:")
    for name, description in ENTITY_TYPES.items():
        print(f"  {name}: {description}")

    print("\nAllowed relationships:")
    for source, relation, target in RELATIONSHIP_TYPES:
        print(f"  {source} --{relation}--> {target}")