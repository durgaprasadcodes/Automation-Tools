
# File Automation Tool
```code
FileAutomationTool
│
├── Creation & Deletion
│   ├── create_files()
│   ├── create_dirs()
│   ├── delete_dir() 
│   ├── delete_file()
│   └── create_project_structure()
│
├── Reading & Writing
│   ├── read_file()
│   ├── write_file()
│   └── append_file()
│
├── Searching
│   ├── search_files_by_filename()
│   ├── search_files_by_extension()
│   └── search_text_in_files()
│
├── Listing & Navigation
│   ├── list_files()
│   ├── list_dirs()
│   └── get_directory_tree()
│
├── File Management
│   ├── rename_file()
│   ├── move_file()
│   └── copy_file()
│   
│
├── Metadata
│   ├── get_file_info()
│   └── path_exists()
│
└── Archive
    ├── create_zip()
    └── extract_zip()
```

```mermaid
flowchart TD
    A["User: Fix the bug in main.py"] --> B["Jarvis reads main.py"]
    B --> C["Send code + instruction to LLM"]
    C --> D["LLM identifies the bug"]
    D --> E["LLM generates old_content and new_content"]
    E --> F["Validate the proposed changes"]
    F --> G{"User approval?"}
    G -->|Yes| H["replace_content()"]
    G -->|No| I["Cancel modification"]
    H --> J["Validate Python syntax"]
    J --> K["Report modification result"]
```