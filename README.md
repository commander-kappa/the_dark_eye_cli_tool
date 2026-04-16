# The Dark Eye (5th Edition) CLI Tool
*Access your character data (from the official pdf sheet or Optolith .json) and roll on your stats from the command line*

**IMPORTANT INFO: PDF Conversion currently ONLY works with the GERMAN OFFICIAL deluxe character sheet!**
For copyright reasons I am, unfortunately, not able to provide you a copy of said character sheet.

## Converting PDF file
- run 'src/python extract_deluxe_pdf.py relative_path/to/your/character.pdf' from your terminal
- copy/move your character.pdf to the 'res/' direcotry and then manually enter the name while running the 'extract_deluxe_pdf.py'

## Using the CLI tool
Run src/main.py.

The character .json file will be loaded by the following priority:
1. By a CLI argument ('python main.py **relative_path/character.json**')
2. By an **JSON=character.json** entry in res/default.ini
3. By manual entry from the programm command line
