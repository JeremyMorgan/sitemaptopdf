import xml.etree.ElementTree as ET
import requests
import os
from weasyprint import HTML
from urllib.parse import urlparse

def extract_urls_from_sitemap(sitemap_path, output_path):
    """
    Extracts URLs from an XML sitemap and saves them to a text file.

    Parameters:
    sitemap_path (str): The path to the XML sitemap file.
    output_path (str): The path to the output text file where the URLs will be saved.

    Returns:
    None

    The function parses the XML sitemap file located at `sitemap_path`, extracts all URLs from the
    `<loc>` tags, and writes them to a text file located at `output_path`. The URLs are written
    one per line. After writing the URLs, the function prints a message indicating the number of
    URLs extracted and the output file path.
    """
    # Parse the XML file    
    tree = ET.parse(sitemap_path)
    root = tree.getroot()

    # Extract URLs
    urls = []
    for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        urls.append(url.text.strip())

    # Write URLs to text file
    with open(output_path, 'w') as f:
        for url in urls:
            f.write(f"{url}\n")

    print(f"Extracted {len(urls)} URLs and saved to {output_path}")

def urls_to_pdfs(input_file, output_folder):
    """
    Converts a list of URLs to PDF files and saves them in a specified folder.

    This function reads URLs from a text file, converts each URL's content to a PDF,
    and saves the PDF in the specified output folder. The PDF filename is derived
    from the last part of the URL path.

    Parameters:
    input_file (str): Path to the text file containing URLs, one per line.
    output_folder (str): Path to the folder where the generated PDFs will be saved.

    Returns:
    None

    The function prints status messages for each successful conversion and any errors encountered.
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Read URLs from the input file
    with open(input_file, 'r') as f:
        urls = f.read().splitlines()

    # Process each URL
    for url in urls:
        try:
            # Extract the last folder name from the URL
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.rstrip('/').split('/')
            last_folder = path_parts[-1] if path_parts else 'index'

            # Generate a filename for the PDF
            filename = f"{last_folder}.pdf"
            pdf_path = os.path.join(output_folder, filename)

            # Convert HTML to PDF using WeasyPrint
            HTML(url=url).write_pdf(pdf_path)

            print(f"Converted {url} to {pdf_path}")
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")


def main():
    """
    Main function to execute the URL extraction and PDF conversion process.

    This function sets up the necessary file paths and calls the functions to extract URLs
    from a sitemap and convert those URLs to PDF files. The sitemap extraction is currently
    commented out.

    Parameters:
    None

    Returns:
    None

    The function performs the following steps:
    1. Defines file paths for the sitemap, URL list, and PDF output folder.
    2. Extracts URLs from the sitemap and saves them to a file.
    3. Converts the URLs from the file to PDF documents.
    """
    sitemap_path = 'sitemap.xml'
    urls_file = 'urls.txt'
    pdf_folder = 'pdf_output'

    # Extract URLs from sitemap
    extract_urls_from_sitemap(sitemap_path, urls_file)

    # Convert URLs to PDFs
    urls_to_pdfs(urls_file, pdf_folder)

if __name__ == "__main__":
    main()