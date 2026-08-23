import os
import sys
import zipfile
import tarfile
import pandas as pd

def generate_simple_md_table(df, max_rows=5):
    """Converts a DataFrame slice into a basic Markdown table string without external dependencies."""
    headers = [str(c) for c in df.columns]
    md_lines = []
    md_lines.append("| " + " | ".join(headers) + " |")
    md_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    
    for _, row in df.head(max_rows).iterrows():
        clean_row = [str(val).replace('\n', ' ').replace('|', '\\|') for val in row]
        md_lines.append("| " + " | ".join(clean_row) + " |")
        
    return "\n".join(md_lines)


# MODE 1: Scan folder and preview contents inside archive files
def mode_1_scan_directory(target_dir, output_filename="file_list_results.txt"):
    """
    Mode 1: Scans the directory, lists files, and previews contents of compressed archives (.zip, .tar).
    Outputs results to a text file.
    """
    output_file_path = os.path.join(target_dir, output_filename)
    print(f"[*] [Mode 1] Scanning directory: {target_dir}")

    with open(output_file_path, "w", encoding="utf-8") as out_file:
        out_file.write(f"=== File Survey Report: {target_dir} ===\n\n")

        for root, dirs, files in os.walk(target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip the output report file itself
                if file == output_filename:
                    continue

                rel_path = os.path.relpath(file_path, target_dir)
                out_file.write(f"[File] {rel_path}\n")

                # Inspect ZIP archive contents
                if file.lower().endswith('.zip'):
                    try:
                        with zipfile.ZipFile(file_path, 'r') as zip_ref:
                            out_file.write("   └── [ZIP Contents]:\n")
                            for item in zip_ref.namelist():
                                out_file.write(f"       ├── {item}\n")
                    except Exception as e:
                        out_file.write(f"   └── [Error reading ZIP: {e}]\n")

                # Inspect TAR archive contents
                elif file.lower().endswith(('.tar', '.tar.gz', '.tgz', '.tar.bz2')):
                    try:
                        with tarfile.open(file_path, 'r') as tar_ref:
                            out_file.write("   └── [TAR Contents]:\n")
                            for member in tar_ref.getmembers():
                                out_file.write(f"       ├── {member.name}\n")
                    except Exception as e:
                        out_file.write(f"   └── [Error reading TAR: {e}]\n")

    print(f"[✔] Scan completed successfully. Output saved to: {output_filename}")


# MODE 2: Extract archives into folders named after the archives
def mode_2_extract_archives(target_dir, output_parent_dir="extracted_files", ignore_macosx=True):
    """
    Mode 2: Extracts compressed archives into dedicated subfolders named after each archive file.
    """
    destination_base = os.path.join(target_dir, output_parent_dir)
    print(f"[*] [Mode 2] Extracting archives in: {target_dir}")
    print(f"[*] Base output destination: {destination_base}\n")

    extracted_count = 0

    for root, dirs, files in os.walk(target_dir):
        # Skip scanning inside the extraction output folder
        if destination_base in root:
            continue

        for file in files:
            file_path = os.path.join(root, file)
            archive_name, _ = os.path.splitext(file)
            
            # Handle tar.gz double extension
            if archive_name.lower().endswith('.tar'):
                archive_name = archive_name[:-4]

            # Dedicated output directory named after the archive file
            archive_out_dir = os.path.join(destination_base, archive_name)

            # Process ZIP archives
            if file.lower().endswith('.zip'):
                print(f"[*] Extracting ZIP: {file} -> {archive_out_dir}")
                os.makedirs(archive_out_dir, exist_ok=True)
                try:
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        for member in zip_ref.infolist():
                            if ignore_macosx and member.filename.startswith('__MACOSX/'):
                                continue
                            zip_ref.extract(member, archive_out_dir)
                    print("    [+] Extracted successfully.")
                    extracted_count += 1
                except Exception as e:
                    print(f"    [-] Extraction failed: {e}")

            # Process TAR archives
            elif file.lower().endswith(('.tar', '.tar.gz', '.tgz', '.tar.bz2')):
                print(f"[*] Extracting TAR: {file} -> {archive_out_dir}")
                os.makedirs(archive_out_dir, exist_ok=True)
                try:
                    with tarfile.open(file_path, 'r') as tar_ref:
                        for member in tar_ref.getmembers():
                            if ignore_macosx and member.name.startswith('__MACOSX/'):
                                continue
                            tar_ref.extract(member, archive_out_dir)
                    print("    [+] Extracted successfully.")
                    extracted_count += 1
                except Exception as e:
                    print(f"    [-] Extraction failed: {e}")

    print(f"\n[✔] Extraction completed. Total archives processed: {extracted_count}")


# MODE 3: Inspect tabular data and output Markdown overview report
def mode_3_data_profiling(target_dir, output_filename="data_overview_report.md"):
    """
    Mode 3: Scans tabular files (.csv, .xlsx, .tsv), profiles their structure,
    missing values, and statistics, and generates a Markdown report.
    """
    print(f"[*] [Mode 3] Generating data profiling report for: {target_dir}")
    
    markdown_output = []
    markdown_output.append("# Data Inspection & Overview Report\n")
    markdown_output.append(f"**Root Directory:** `{target_dir}`\n")
    markdown_output.append("---\n")

    supported_extensions = ('.csv', '.tsv', '.xlsx', '.xls')
    data_files = []

    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.lower().endswith(supported_extensions):
                data_files.append(os.path.join(root, file))

    if not data_files:
        print("[-] No tabular data files found (.csv, .xlsx, etc.).")
        markdown_output.append("No dataset files found.\n")
        return

    print(f"[*] Found {len(data_files)} tabular dataset(s) to analyze.\n")

    for file_path in data_files:
        relative_path = os.path.relpath(file_path, target_dir)
        print(f"[*] Profiling file: {relative_path}")

        markdown_output.append(f"## Dataset: `{relative_path}`\n")

        try:
            if file_path.lower().endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path)

            total_rows, total_cols = df.shape
            duplicate_count = df.duplicated().sum()
            dup_percentage = (duplicate_count / total_rows * 100) if total_rows > 0 else 0.0

            markdown_output.append("### 1. General Overview")
            markdown_output.append(f"- **Total Rows:** `{total_rows:,}`")
            markdown_output.append(f"- **Total Columns:** `{total_cols:,}`")
            markdown_output.append(f"- **Duplicate Rows:** `{duplicate_count:,}` ({dup_percentage:.2f}%)\n")

            markdown_output.append("### 2. Columns Profiling")
            markdown_output.append("| Column Name | Data Type | Non-Null | Missing Count | Missing % | Unique Values | Sample Value |")
            markdown_output.append("| --- | --- | --- | --- | --- | --- | --- |")

            for col in df.columns:
                dtype = str(df[col].dtype)
                non_null_cnt = df[col].notnull().sum()
                missing_cnt = df[col].isnull().sum()
                missing_pct = (missing_cnt / total_rows * 100) if total_rows > 0 else 0.0
                unique_cnt = df[col].nunique(dropna=True)
                
                sample_series = df[col].dropna()
                sample_val = str(sample_series.iloc[0]) if not sample_series.empty else "N/A"
                sample_val_clean = sample_val.replace('\n', ' ').replace('|', '\\|')
                if len(sample_val_clean) > 30:
                    sample_val_clean = sample_val_clean[:27] + "..."

                markdown_output.append(
                    f"| `{col}` | `{dtype}` | {non_null_cnt:,} | {missing_cnt:,} | {missing_pct:.2f}% | {unique_cnt:,} | {sample_val_clean} |"
                )
            markdown_output.append("\n")

            numeric_df = df.select_dtypes(include=['number'])
            if not numeric_df.empty:
                markdown_output.append("### 3. Numerical Summary")
                desc = numeric_df.describe().T[['min', '25%', '50%', '75%', 'max', 'mean', 'std']]
                desc_reset = desc.reset_index().rename(columns={'index': 'Column'})
                markdown_output.append(generate_simple_md_table(desc_reset, max_rows=len(desc_reset)))
                markdown_output.append("\n")

            markdown_output.append("### 4. Data Preview (First 5 Rows)")
            markdown_output.append(generate_simple_md_table(df, max_rows=5))
            markdown_output.append("\n---\n")

            print(f"    [+] Profiling completed ({total_rows} rows x {total_cols} cols).")

        except Exception as err:
            markdown_output.append(f"**Error analyzing file:** `{err}`\n\n---\n")
            print(f"    [-] Failed to process {relative_path}: {err}")

    output_path = os.path.join(target_dir, output_filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(markdown_output))

    print(f"\n[✔] Data profiling complete! Report saved to: {output_filename}")


def main():
    # Determine base directory
    if '__file__' in globals():
        base_dir = os.path.dirname(os.path.abspath(__file__))
    else:
        base_dir = os.getcwd()

    # Parse command line argument mode
    mode = "1" # Default mode
    if len(sys.argv) > 1:
        mode = sys.argv[1].strip()

    print("==================================================")
    print("      UNIFIED FILE & DATA ANALYSIS TOOL           ")
    print("==================================================\n")

    if mode == "1":
        print("[Mode Selected: 1 - Directory Scan & Archive Survey]")
        mode_1_scan_directory(base_dir)

    elif mode == "2":
        print("[Mode Selected: 2 - Extract Archives into Dedicated Subfolders]")
        mode_2_extract_archives(base_dir)

    elif mode == "3":
        print("[Mode Selected: 3 - Tabular Data Profiling & Markdown Report]")
        mode_3_data_profiling(base_dir)

    else:
        print(f"[!] Invalid mode selection: '{mode}'")
        print("\nUsage Options:")
        print("  python a.py       -> Mode 1: Scan directory and preview archive contents (Default)")
        print("  python a.py 1     -> Mode 1: Scan directory and preview archive contents")
        print("  python a.py 2     -> Mode 2: Extract archives into subfolders named after each archive")
        print("  python a.py 3     -> Mode 3: Profile CSV/Excel datasets and output Markdown report")


if __name__ == "__main__":
    main()
