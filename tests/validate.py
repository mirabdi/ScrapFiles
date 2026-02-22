import json
from typing import Any, Dict, List, Union
from datetime import datetime

class ValidationError(Exception):
    def __init__(self, message: str, path: str = ""):
        self.message = message
        self.path = path
        super().__init__(f"{path}: {message}")

class JSONValidator:
    def __init__(self, schema: Dict):
        self.schema = schema
        self.errors: List[ValidationError] = []

    def validate_type(self, value: Any, expected_type: Union[str, List[str]], path: str) -> bool:
        """Validate that the value matches the expected type(s)."""
        if isinstance(expected_type, list):
            return any(self.validate_type(value, t, path) for t in expected_type)

        if expected_type == "null":
            return value is None
        if expected_type == "boolean":
            return isinstance(value, bool)
        if expected_type == "integer":
            return isinstance(value, int)
        if expected_type == "number":
            return isinstance(value, (int, float))
        if expected_type == "string":
            return isinstance(value, str)
        if expected_type == "array":
            return isinstance(value, list)
        if expected_type == "object":
            return isinstance(value, dict)

        return False

    def validate(self, data: Any, schema: Dict = None, path: str = "") -> bool:
        """Validate data against the schema."""
        if schema is None:
            schema = self.schema

        # Check type
        value_type = schema.get("type")
        if value_type and not self.validate_type(data, value_type, path):
            self.errors.append(
                ValidationError(
                    f"Expected {value_type}, got {type(data).__name__}",
                    path
                )
            )
            return False

        # For objects, validate properties and required fields
        if isinstance(data, dict) and schema.get("type") in ["object", ["object", "null"]]:
            properties = schema.get("properties", {})
            required = schema.get("required", [])

            # Check required fields
            for field in required:
                if field not in data:
                    self.errors.append(
                        ValidationError(f"Missing required field: {field}", path)
                    )
                    return False

            # Validate each property
            for key, value in data.items():
                if key in properties:
                    property_path = f"{path}.{key}" if path else key
                    self.validate(value, properties[key], property_path)

        # For arrays, validate items
        elif isinstance(data, list) and schema.get("type") in ["array", ["array", "null"]]:
            item_schema = schema.get("items", {})
            for i, item in enumerate(data):
                item_path = f"{path}[{i}]"
                self.validate(item, item_schema, item_path)

        return len(self.errors) == 0

def load_json(file_path: str) -> Dict:
    """Load JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    try:
        # Load schema and data
        schema = load_json('schema.json')
        data = load_json('response.json')

        # Validate
        validator = JSONValidator(schema)
        is_valid = validator.validate(data)

        # Print results
        if is_valid:
            print("✅ Validation successful! Data matches schema.")
        else:
            print("❌ Validation failed!")
            print("\nErrors:")
            for error in validator.errors:
                print(f"- Path: {error.path}")
                print(f"  Error: {error.message}")
                print()

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

# Example usage in code:
"""
# Load your schema and data
schema = load_json('schema.json')
data = load_json('response.json')

# Create validator
validator = JSONValidator(schema)

# Validate
is_valid = validator.validate(data)

if not is_valid:
    for error in validator.errors:
        print(f"{error.path}: {error.message}")
"""