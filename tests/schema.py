import json
from typing import Any, Dict, List, Union
from datetime import datetime

class SchemaGenerator:
    def __init__(self, make_all_required=True):
        self.make_all_required = make_all_required

    def infer_type(self, value: Any) -> str:
        """Infer the JSON Schema type from a Python value."""
        if value is None:
            return "null"
        if isinstance(value, bool):
            return "boolean"
        if isinstance(value, int):
            return "integer"
        if isinstance(value, float):
            return "number"
        if isinstance(value, str):
            return "string"
        if isinstance(value, list):
            return "array"
        if isinstance(value, dict):
            return "object"
        raise ValueError(f"Unsupported type: {type(value)}")

    def generate_schema(self, data: Any, path: str = "") -> Dict:
        """Generate a JSON schema for the given data."""
        data_type = self.infer_type(data)
        schema: Dict[str, Any] = {"type": data_type}

        if data_type == "object":
            properties = {}
            required = []
            
            for key, value in data.items():
                properties[key] = self.generate_schema(value, f"{path}.{key}")
                if self.make_all_required and value is not None:
                    required.append(key)
            
            schema["properties"] = properties
            if required:
                schema["required"] = required

        elif data_type == "array" and data:
            # Handle arrays by looking at the first item
            # You might want to examine more items for more accurate schemas
            item_schema = self.generate_schema(data[0], f"{path}[]")
            schema["items"] = item_schema

        elif data_type in ["string", "integer", "number"]:
            # Handle potential null values
            if data is None:
                schema["type"] = ["null", data_type]

        return schema

def load_json_file(file_path: str) -> Dict:
    """Load JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_schema(schema: Dict, output_file: str):
    """Save the generated schema to a file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)
 
def main():
    # Example usage
    try:
        # Load your JSON data
        json_data = load_json_file('response.json')
        
        # Generate schema
        generator = SchemaGenerator(make_all_required=True)
        schema = generator.generate_schema(json_data)
        
        # Save schema to file
        save_schema(schema, 'schema.json')
        print("Schema generated successfully!")
        
        # Print schema stats
        print("\nSchema Statistics:")
        print(f"Total properties: {len(str(schema).split('properties'))}")
        print(f"Required fields: {sum(len(v.get('required', [])) for v in str(schema).split('properties') if isinstance(v, dict))}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()