import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class ReadFileTool:
    """
    A tool for reading the content of a file from a specified base path.

    :param base_path: The base directory path where file operations will be performed.
    """
    def __init__(self, base_path):
        self.base_path = base_path

    def __call__(self, file_path):
        """
        Reads the content of a file.

        :param file_path: The relative path to the file from the base directory.
        :return: The content of the file as a string, or an error message if the file is not found or another error occurs.
        """
        full_path = os.path.join(self.base_path, file_path)
        try:
            with open(full_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return f"File {file_path} not found."
        except Exception as e:
            return str(e)

class WriteFileTool:
    """
    A tool for writing content to a file at a specified base path.
    :param base_path: The base directory path where file operations will be performed.
    """
    def __init__(self, base_path):
        self.base_path = base_path

    def __call__(self, file_path, content, render_as_pdf=False):
        """
        Writes content to a file. If render_as_pdf is True, the content is treated as LaTeX
        formatted text and saved as a PDF.
        :param file_path: The relative path to the file from the base directory.
        :param content: The content to write to the file. If render_as_pdf is True, this should
                        include LaTeX formatted mathematical expressions.
        :param render_as_pdf: A boolean indicating whether to render the content as a PDF.
        :return: A success message if the file is written successfully, or an error message if an error occurs.
        """
        full_path = os.path.join(self.base_path, file_path)
        try:
            if render_as_pdf:
                with PdfPages(full_path) as pdf:
                    plt.figure(figsize=(8, 6))
                    plt.text(0.5, 0.5, content, fontsize=12, ha='center', va='center')
                    plt.axis('off')
                    pdf.savefig()
                    plt.close()
                return f"PDF {file_path} written successfully with rendered content."
            else:
                with open(full_path, 'w') as file:
                    file.write(content)
                return f"File {file_path} written successfully."
        except Exception as e:
            return str(e)

class ListFilesTool:
    """
    A tool for listing all files in a specified directory at a base path.

    :param base_path: The base directory path where file operations will be performed.
    """
    def __init__(self, base_path):
        self.base_path = base_path

    def __call__(self, directory_path=""):
        """
        Lists all files in the specified directory.

        :param directory_path: The relative path to the directory from the base directory.
        :return: A list of file names in the directory, or an error message if the directory is not found or another error occurs.
        """
        full_path = os.path.join(self.base_path, directory_path)
        try:
            return os.listdir(full_path)
        except FileNotFoundError:
            return f"Directory {directory_path} not found."
        except Exception as e:
            return str(e)