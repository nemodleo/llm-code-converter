# auto
import re

def convert_line(line: str, vo_type: str = "SecuritiesInqrPritMgmtVo") -> str:
    # Replace Map with VO type in ArrayList declarations and method parameters
    line = re.sub(r'(ArrayList<)Map(>)', rf'\1{vo_type}\2', line)
    line = re.sub(r'Map\s+pDoc', f'{vo_type} pDoc', line)

    # Convert camel case for getters and setters with proper handling of acronyms
    def to_camel_case(snake_str):
        components = snake_str.split('_')
        if len(components) == 1:
            return components[0].lower()
        else:
            result = []
            for i, component in enumerate(components):
                if component.isupper() and len(component) > 1:
                    # Handle acronyms by making only the first letter uppercase
                    result.append(component[0].upper() + component[1:].lower())
                elif i == 0:
                    result.append(component.lower())
                else:
                    result.append(component.capitalize())
            return ''.join(result)

    # Replace MapDataUtil.getString with VO getter methods
    line = re.sub(r'MapDataUtil\.getString\(pDoc,\s*"([^"]+)"\)',
                  lambda m: f'pDoc.get{to_camel_case(m.group(1))}()', line)

    # Replace MapDataUtil.setString with VO setter methods
    line = re.sub(r'MapDataUtil\.setString\(pDoc,\s*"([^"]+)"\s*,\s*([^)]+)\)',
                  lambda m: f'pDoc.set{to_camel_case(m.group(1))}({m.group(2)})', line)

    return line

