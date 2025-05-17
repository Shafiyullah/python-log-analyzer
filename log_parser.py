import os

def analyze_log_file(file_path):
    """
    Analyzes a log file to count total lines and identify error lines.

    Args:
        file_path (str): The path to the log file.

    Returns:
        dict: A dictionary containing the analysis summary:
              'total_lines': Total number of lines in the file.
              'error_count': Number of lines containing error keywords.
              'error_lines': A list of the error lines found.
              'error': An error message if the file cannot be read.
    """
    total_lines = 0
    error_count = 0
    error_lines = []
    error_keywords = ['ERROR', 'Error', 'error', 'EXCEPTION', 'Exception', 'exception', 'Failed', 'failed'] # Keywords to look for

    if not os.path.exists(file_path):
        return {'error': f"File not found: {file_path}"}

    try:
        with open(file_path, 'r') as f:
            for line in f:
                total_lines += 1
                # Check for any of the error keywords (case-insensitive check)
                if any(keyword.lower() in line.lower() for keyword in error_keywords):
                    error_count += 1
                    error_lines.append(line.strip()) # Add stripped line to list
    except Exception as e:
        return {'error': f"Error reading file: {e}"}

    return {
        'total_lines': total_lines,
        'error_count': error_count,
        'error_lines': error_lines,
        'error': None
    }

# Example of how you might use this function directly (optional)
if __name__ == "__main__":
    # You can uncomment this to test the parser directly
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # sample_log_path = os.path.join(current_dir, 'sample.log')
    # analysis_results = analyze_log_file(sample_log_path)
    # if analysis_results.get('error'):
    #     print(f"Error: {analysis_results['error']}")
    # else:
    #     print("Log Analysis Summary:")
    #     print(f"Total lines: {analysis_results['total_lines']}")
    #     print(f"Error lines found: {analysis_results['error_count']}")
    #     print("Error lines:")
    #     for line in analysis_results['error_lines']:
    #         print(f"- {line}")
    pass # Keep this pass if you want to primarily use it with Flask