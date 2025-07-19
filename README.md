# Static Site Generator

This project is a simple static site generator built in Python as part of the Boot.dev curriculum. It converts Markdown content into HTML pages with basic styling, perfect for personal sites or technical blogs.

**Note:** Nested inline Markdown (such as italics within bold text) is not currently supported.

## Features

- Parses Markdown files to generate HTML pages.
- Organizes content and output using clear directory structure.
- Includes a default CSS theme.
- Automatically copies over images for use in your site.
- Unit tests included for key components.

## Project Structure

    ├── build.sh # Build script for generating site
    ├── content/ # Source Markdown files (input)
    ├── docs/ # Generated HTML output, images, and CSS
    ├── src/ # Python source code and unit tests
    ├── static/ # Static files (images, CSS) to copy to output
    ├── template.html # HTML template for page generation
    ├── test.sh # Script for running all unit tests
    └── README.md

## Getting Started

1. **Clone the repository:**

   ```sh
   git clone https://github.com/DanielJoseph97/my-static-site.git
   cd YOUR-REPOSITORY
   ```
2. Add or edit your Markdown content:

Place new .md files in the content/ directory using subfolders as desired.

3. Build the site:

```sh
./build.sh
```
This will process Markdown files and output the HTML site to the docs/ directory.

## Running Tests
Unit tests are provided to ensure project reliability.
You can run by running the script:
```sh
./test.sh
```
This command automatically discovers and executes all Python unit tests located in src/.

## Contributing
Feel free to fork and experiment! If you add features or find bugs, improvements and suggestions are welcome.

## License
No license specified.

## Acknowledgements
Built with diligence (and many test cases) on [Boot.Dev](https://www.boot.dev/courses/build-ai-agent-python).
