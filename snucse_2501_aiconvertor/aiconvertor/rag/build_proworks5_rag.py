import re
from pathlib import Path
from tqdm import tqdm
# from langchain_community.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
import javalang
from javalang.tree import (
    MethodDeclaration,
    ClassDeclaration,
    ConstructorDeclaration,
    FieldDeclaration,
    ArrayInitializer,
    InterfaceDeclaration,
    EnumDeclaration,
)


def collect_code_files(root_dir, extensions=None):
    """
    Collect code files with specified extensions from root directory.
    
    Args:
        root_dir: Path object pointing to the root directory
        extensions: List of file extensions to include (default: ['.java'])
        
    Returns:
        List of Path objects for matching files
    """
    if extensions is None:
        extensions = ['.java']
    
    files = []
    for ext in extensions:
        files.extend(list(root_dir.rglob(f"*{ext}")))
    
    print(f"[!] Found {len(files)} files with extensions: {', '.join(extensions)}")
    return files


def extract_code(file_path):
    """Extract code content from file with error handling."""
    try:
        return file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""


def preprocess_java_code(code):
    """
    Preprocesses Java code to handle common issues that might cause parsing errors.
    
    Args:
        code: Java code as string
        
    Returns:
        Preprocessed Java code
    """
    # Handle problematic imports or annotations that might cause parser issues
    replacements = [
        # Fix any complex or problematic generics that might confuse the parser
        (r"<\s*\?\s+extends\s+[^>]+\s*>", "<?>"),
        (r"<\s*\?\s+super\s+[^>]+\s*>", "<?>"),
        
        # Simplify complex annotations that might confuse the parser
        (r"@\w+\s*\(\s*[^)]+\s*\)", "@AnnotationSimplified"),
        
        # Handle inline annotations within parameter lists
        (r"(@\w+\s*(\([^)]*\))?\s*)+\s*(\w+\s+\w+)", r"/* \1 */ \3"),
        
        # Remove lambda expressions that might confuse the parser
        (r"\([^)]*\)\s*->\s*\{[^}]*\}", "/* lambda */"),
        
        # Fix issues with Diamond operator in generic instantiation
        (r"new\s+[\w.]+<>", "new GenericClass()"),
    ]
    
    # Apply replacements
    preprocessed = code
    for pattern, replacement in replacements:
        preprocessed = re.sub(pattern, replacement, preprocessed)
    
    return preprocessed


def direct_text_extraction(code: str, file_path: Path) -> list[Document]:
    """
    Extract chunks from Java files using direct text analysis without parsing.
    This is more robust but less semantically accurate.
    
    Args:
        code: Java code string
        file_path: Path to the file
        
    Returns:
        List of Document objects
    """
    # Split code into chunks based on patterns
    # Look for class, method, and field declarations
    documents = []
    lines = code.splitlines()
    
    # Identify class name from filename or from code
    class_pattern = re.compile(r'(public|private|protected)?\s*(abstract|final)?\s*class\s+(\w+)')
    class_match = class_pattern.search(code)
    class_name = class_match.group(3) if class_match else file_path.stem
    
    # Extract package name if available
    package_pattern = re.compile(r'package\s+([\w.]+);')
    package_match = package_pattern.search(code)
    package_name = package_match.group(1) if package_match else "unknown"
    
    # Find all method-like patterns
    method_pattern = re.compile(
        r'(public|private|protected)?\s*'
        r'(static|final|abstract|synchronized)?\s*'
        r'(?:<[^>]*>)?\s*'  # Generic type parameters
        r'(\w+(?:<[^>]*>)?)\s+'  # Return type
        r'(\w+)\s*\(([^)]*)\)'  # Method name and parameters
    )
    
    # Find imports for context
    import_pattern = re.compile(r'import\s+([\w.]+(?:\.\*)?);')
    imports = import_pattern.findall(code)
    
    # Add a document for class-level information
    class_start_idx = class_match.start() if class_match else 0
    
    # Determine where class declaration ends (first { after class declaration)
    class_decl_end = code.find('{', class_start_idx)
    if class_decl_end == -1:
        class_decl_end = len(code)
    
    # Extract header comments and annotations
    header_end = code.find('package') if 'package' in code else 0
    if header_end == -1:
        header_end = code.find('import') if 'import' in code else 0
    if header_end == -1:
        header_end = class_start_idx if class_match else 0
    
    header_text = code[:header_end].strip()
    
    # Create class-level document
    class_meta = {
        "file": str(file_path),
        "class": class_name,
        "package": package_name
    }
    
    class_header_lines = [
        f"// FILE: {file_path}",
        f"// CLASS: {class_name}",
        f"// PACKAGE: {package_name}",
        "// TYPE: CLASS_DECLARATION"
    ]
    
    # Add imports for context
    if imports:
        class_header_lines.append("// IMPORTS:")
        for imp in imports[:10]:  # Limit to avoid too much noise
            class_header_lines.append(f"// - {imp}")
    
    # Create class-level document with header, package, imports
    class_chunk = "\n".join(class_header_lines)
    if header_text:
        class_chunk += f"\n\n/* Header Comments */\n{header_text}\n"
    
    class_chunk += f"\n/* Class Declaration */\n{code[class_start_idx:class_decl_end + 1]}"
    
    documents.append(Document(page_content=class_chunk, metadata=class_meta))
    
    # Find and add all methods
    for match in method_pattern.finditer(code):
        method_name = match.group(4)
        return_type = match.group(3)
        parameters = match.group(5)
        
        # Find method body (everything between { and its matching })
        method_start = code.find('{', match.end())
        
        if method_start != -1:
            # Find matching closing brace
            open_braces = 1
            method_end = method_start + 1
            
            while open_braces > 0 and method_end < len(code):
                if code[method_end] == '{':
                    open_braces += 1
                elif code[method_end] == '}':
                    open_braces -= 1
                method_end += 1
            
            if open_braces == 0:
                # Extract the method signature and body
                method_signature = code[match.start():method_start + 1]
                method_body = code[method_start:method_end]
                
                # Look for annotations before method signature (up to 5 lines back)
                method_start_pos = match.start()
                lines_before = code[:method_start_pos].splitlines()
                annotations = []
                
                if lines_before:
                    for i in range(min(5, len(lines_before))):
                        line = lines_before[-i-1].strip()
                        if line.startswith('@'):
                            annotations.insert(0, line)
                        elif line and not line.startswith('//') and not line.startswith('/*'):
                            break
                
                method_meta = {
                    "file": str(file_path),
                    "class": class_name,
                    "method": method_name,
                    "return_type": return_type
                }
                
                method_header_lines = [
                    f"// FILE: {file_path}",
                    f"// CLASS: {class_name}",
                    "// TYPE: METHOD",
                    f"// NAME: {method_name}",
                    f"// RETURN_TYPE: {return_type}",
                    f"// PARAMETERS: {parameters}"
                ]
                
                if annotations:
                    method_header_lines.append("// ANNOTATIONS:")
                    for anno in annotations:
                        method_header_lines.append(f"// - {anno}")
                
                method_chunk = "\n".join(method_header_lines) + "\n"
                
                # Add annotations to the chunk
                if annotations:
                    method_chunk += "\n".join(annotations) + "\n"
                
                method_chunk += method_signature + method_body
                
                documents.append(Document(page_content=method_chunk, metadata=method_meta))
    
    # If we couldn't extract any methods, make sure we at least have the class document
    if len(documents) <= 1:
        # Add the full file as a document
        full_meta = {
            "file": str(file_path),
            "class": class_name,
            "package": package_name,
            "type": "FULL_FILE"
        }
        
        full_header_lines = [
            f"// FILE: {file_path}",
            f"// CLASS: {class_name}",
            f"// PACKAGE: {package_name}",
            "// TYPE: FULL_FILE"
        ]
        
        documents.append(Document(page_content="\n".join(full_header_lines) + "\n" + code, metadata=full_meta))
    
    return documents


def format_method_signature(member):
    """
    Format method signature in a more readable way.
    
    Args:
        member: A method declaration object from javalang
        
    Returns:
        str: A formatted method signature
    """
    try:
        if isinstance(member, MethodDeclaration):
            # Get modifiers
            modifiers = ' '.join(member.modifiers) if member.modifiers else ''
            
            # Get return type
            return_type = str(member.return_type) if member.return_type else 'void'
            
            # Get name
            name = member.name
            
            # Get parameters
            params = []
            for param in member.parameters:
                param_type = str(param.type)
                param_name = param.name
                param_str = f"{param_type} {param_name}"
                if param.varargs:
                    param_str += "..."
                params.append(param_str)
            params_str = ', '.join(params)
            
            # Get throws
            throws_str = ''
            if member.throws:
                throws_str = f" throws {', '.join(member.throws)}"
            
            # Combine everything
            return f"{modifiers} {return_type} {name}({params_str}){throws_str}"
        else:
            return str(member).strip()
    except Exception as e:
        return f"{str(member).strip()} (Error formatting: {e})"


def find_annotations_for_position(code_lines, position):
    """
    Find annotations that belong to a specific position by looking backward.
    This handles the case where annotations are followed by empty lines before the declaration.
    
    Args:
        code_lines: List of code lines
        position: The line position (1-based) of the declaration
    
    Returns:
        List of annotation lines and the line number where annotations start
    """
    if position <= 1:
        return [], position - 1
    
    annotations = []
    line_idx = position - 2  # Start from line before the declaration
    annotation_start_line = position - 1  # Default: no annotations
    
    # Go backward until we hit a non-annotation and non-empty line
    while line_idx >= 0:
        line = code_lines[line_idx].strip()
        
        # If we hit a non-empty line that's not an annotation, stop
        if line and not line.startswith("@"):
            break
            
        # If it's an annotation, add it to our list and track its position
        if line.startswith("@"):
            annotations.insert(0, code_lines[line_idx])
            annotation_start_line = line_idx
            
        line_idx -= 1
        
    return annotations, annotation_start_line


def split_java_by_module(code: str, file_path: Path) -> list[Document]:
    """
    Split Java code into semantic chunks based on class components.
    
    Args:
        code: The Java code as string
        file_path: Path to the source file
        
    Returns:
        List of Document objects with extracted code chunks
    """
    # First try preprocessed code
    preprocessed_code = preprocess_java_code(code)
    
    try:
        # Try parsing with preprocessed code
        tree = javalang.parse.parse(preprocessed_code)
        return process_parsed_tree(preprocessed_code, tree, file_path)
    except javalang.parser.JavaSyntaxError as e:
        print(f"[SyntaxError] Skipping {file_path}: {e}")
    except Exception as e:
        print(f"[ParseError] Skipping {file_path}: {e}")
    # except Exception as first_error:
    #     try:
    #         # If that fails, try parsing the original code
    #         tree = javalang.parse.parse(code)
    #         return process_parsed_tree(code, tree, file_path)
    #     except Exception as second_error:
    #         # If both parsing attempts fail, use direct text extraction
    #         print(f"Error parsing {file_path}: {second_error}")
    #         return direct_text_extraction(code, file_path)


def process_parsed_tree(code: str, tree, file_path: Path) -> list[Document]:
    """
    Process a successfully parsed Java syntax tree
    
    Args:
        code: Java code string
        tree: Parsed javalang syntax tree
        file_path: Path to the source file
        
    Returns:
        List of Document objects
    """
    lines = code.splitlines()
    documents = []

    for type_decl in tree.types:
        type_name = getattr(type_decl, 'name', 'UnknownClass')

        members = [
            m for m in type_decl.body
            if isinstance(m, (
                MethodDeclaration,
                ConstructorDeclaration,
                FieldDeclaration,
                ClassDeclaration,
                ArrayInitializer,
                InterfaceDeclaration,
                EnumDeclaration,
            ))
        ]

        member_positions = [
            (m.position.line if m.position else 1, m) for m in members
        ]
        member_positions.sort(key=lambda x: x[0])

        for idx, (start_line, member) in enumerate(member_positions):
            # Get annotations that belong to this member
            anno_lines, annotation_start_line = find_annotations_for_position(lines, start_line)
            
            # Get the end line for this member's code body
            if idx + 1 < len(member_positions):
                # For every member except the last one, end just before the annotations of the next member
                next_member_line = member_positions[idx + 1][0]
                next_member_annotations, next_annotation_start = find_annotations_for_position(lines, next_member_line)
                
                # If next member has annotations, end before those annotations
                if next_member_annotations:
                    end_line = next_annotation_start
                else:
                    end_line = next_member_line - 1
            else:
                # For the last member, include all lines until the end
                end_line = len(lines)
            
            # Get the code chunk for this member (annotations + declaration + body)
            if anno_lines:
                chunk_lines = lines[annotation_start_line:end_line]
            else:
                chunk_lines = lines[start_line - 1:end_line]
                
            chunk_code = "\n".join(chunk_lines)

            meta = {
                "file": str(file_path),
                "class": type_name,
            }

            header_lines = [
                f"// FILE: {file_path}",
                f"// CLASS: {type_name}"
            ]

            if isinstance(member, MethodDeclaration):
                meta["method"] = member.name
                formatted_signature = format_method_signature(member)
                header_lines += [
                    "// TYPE: METHOD",
                    f"// NAME: {member.name}",
                    f"// SIGNATURE: {formatted_signature}"
                ]
            elif isinstance(member, ConstructorDeclaration):
                meta["constructor"] = member.name
                header_lines += [
                    "// TYPE: CONSTRUCTOR",
                    f"// NAME: {member.name}",
                    f"// SIGNATURE: {format_method_signature(member)}"
                ]
            elif isinstance(member, FieldDeclaration):
                variable_names = [v.name for v in member.declarators]
                meta["field"] = variable_names
                header_lines += [
                    "// TYPE: FIELD",
                    f"// NAME: {', '.join(variable_names)}",
                    f"// SIGNATURE: {format_method_signature(member)}"
                ]
            elif isinstance(member, ClassDeclaration):
                meta["subclass"] = member.name
                header_lines += [
                    "// TYPE: SUBCLASS",
                    f"// NAME: {member.name}",
                    f"// SIGNATURE: {format_method_signature(member)}"
                ]
            elif isinstance(member, ArrayInitializer):
                meta["init_block"] = "static block"
                header_lines += [
                    "// TYPE: INITIALIZER",
                    "// NAME: <static block>"
                ]
            elif isinstance(member, InterfaceDeclaration):
                meta["interface"] = member.name
                header_lines += [
                    "// TYPE: INTERFACE",
                    f"// NAME: {member.name}",
                    f"// SIGNATURE: {format_method_signature(member)}"
                ]
            elif isinstance(member, EnumDeclaration):
                meta["enum"] = member.name
                header_lines += [
                    "// TYPE: ENUM",
                    f"// NAME: {member.name}",
                    f"// SIGNATURE: {format_method_signature(member)}"
                ]
            else:
                header_lines += ["// TYPE: UNKNOWN"]

            final_chunk = "\n".join(header_lines) + "\n" + chunk_code
            documents.append(Document(page_content=final_chunk, metadata=meta))

    return documents


def save_problematic_files(error_files, output_dir):
    """
    Save a list of problematic files for later analysis
    
    Args:
        error_files: List of files that caused errors
        output_dir: Directory to save the list
    """
    output_path = Path(output_dir) / "problematic_files.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        for file_path in error_files:
            f.write(f"{file_path}\n")
    
    print(f"Saved list of problematic files to: {output_path}")


def build_vectorstore(code_dir, vectorstore_path, embedding_model_name, output_dir="./output"):
    """
    Build a vector store from code files in the specified directory.
    
    Args:
        code_dir: Path to the directory containing code files
        vectorstore_path: Path to save the vector store
        embedding_model_name: Name of the embedding model to use
        output_dir: Directory to save analysis and debug information
    """
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    docs = []
    error_files = []
    code_files = collect_code_files(code_dir)
    total_files = len(code_files)
    
    print(f"Processing {total_files} Java files...")
    
    # Initialize progress tracking
    progress_bar = tqdm(total=total_files, desc="Processing Java files")
    
    # Track parsing stats
    successful_files = 0
    failed_files = 0
    direct_extraction_used = 0
    
    for path in code_files:
        try:
            code = extract_code(path)
            if not code:
                failed_files += 1
                error_files.append(path)
                progress_bar.update(1)
                continue
                
            # Get original number of docs
            original_doc_count = len(docs)
            
            # Try to parse the file
            new_docs = split_java_by_module(code, path)
            if new_docs is None:
                failed_files += 1
                error_files.append(path)
                progress_bar.update(1)
                continue
            
            # Check if direct extraction was used
            if any("TYPE: FULL_FILE" in doc.page_content for doc in new_docs):
                direct_extraction_used += 1
                
            docs.extend(new_docs)
            
            # If we added new docs, consider it successful
            if len(docs) > original_doc_count:
                successful_files += 1
            else:
                failed_files += 1
                error_files.append(path)
                
        except Exception as e:
            print(f"Error processing {path}: {e}")
            failed_files += 1
            error_files.append(path)
        
        # Update progress bar
        progress_bar.update(1)
    
    progress_bar.close()
    
    # Save list of problematic files
    save_problematic_files(error_files, output_dir)
    
    print(f"✅ Total chunks created: {len(docs)}")
    print(f"📊 Processing stats:")
    print(f"   - Successful files: {successful_files}")
    print(f"   - Failed files: {failed_files}")
    print(f"   - Direct text extraction used: {direct_extraction_used}")

    print(f"🔄 Creating embeddings with model: {embedding_model_name}")
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    
    # Show progress for vector store creation
    with tqdm(total=1, desc="Creating vector store") as progress_bar:
        vectorstore = FAISS.from_documents(docs, embeddings)
        progress_bar.update(1)
    
    # Show progress for saving
    with tqdm(total=1, desc="Saving vector store") as progress_bar:
        vectorstore.save_local(vectorstore_path)
        progress_bar.update(1)
        
    print(f"✅ FAISS vectorstore saved to: {vectorstore_path}")
    return vectorstore


if __name__ == "__main__":
    embedding_model_name = "microsoft/codebert-base" #"BAAI/bge-base-en-v1.5"
    code_dir = Path("data/snu_after_20250430/src")
    vectorstore_path = f"data/db/proworks5_vectorstore_{embedding_model_name.split('/')[-1]}"

    build_vectorstore(code_dir, vectorstore_path, embedding_model_name)
