from crewai.tools import BaseTool

class CheckResourceAvailabilityTool(BaseTool):
    name: str = "Check Resource Availability Tool"
    description: str = "Checks if a required medical resource (e.g., doctor, equipment, room) is available."

    def _run(self, resource_name: str) -> str:
        # Mock logic to simulate an external system
        available_resources = ["Dr. Smith", "MRI Scanner", "ICU Bed 1", "Consultation Room A"]
        if any(res.lower() in resource_name.lower() for res in available_resources) or "available" in resource_name.lower() or "doctor" in resource_name.lower():
            return f"{resource_name} is available."
        elif "unavailable" in resource_name.lower():
            return f"{resource_name} is NOT available."
        else:
            # Default to available for the sake of the demo
            return f"Resource '{resource_name}' is available for scheduling."
