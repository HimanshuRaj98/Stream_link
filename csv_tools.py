# csv_tools.py
"""
CSVTools - Utility functions for merging, cleaning, sorting,
and generating streaming URLs from CSV files.
"""

import os
import csv
import pandas as pd

class CSVTools:
    def __init__(self, logger=None, status_updater=None):
        """
        :param logger: function for logging messages e.g. print or UI log
        :param status_updater: function for updating UI status labels
        """
        self.log = logger if logger else print
        self.update_status = status_updater if status_updater else lambda msg: None

    def merge_csvs(self, main_file, source_file, columns):
        """Merge unique entries from source to main CSV."""
        if not os.path.exists(main_file) or not os.path.exists(source_file):
            raise FileNotFoundError("Both main and source files must exist.")

        with open(main_file, newline='', encoding='utf-8') as mfile:
            reader = csv.DictReader(mfile)
            main_data = list(reader)
            existing = {(r.get(columns[0], ''), r.get(columns[1], '')) for r in main_data}

        with open(source_file, newline='', encoding='utf-8') as sfile:
            reader = csv.DictReader(sfile)
            new_entries = []
            for row in reader:
                key = (row.get(columns[0], ''), row.get(columns[1], ''))
                if key not in existing and all(row.get(c) for c in columns):
                    new_entries.append({c: row[c] for c in columns})
                    existing.add(key)

        if new_entries:
            with open(main_file, 'a', newline='', encoding='utf-8') as mfile:
                writer = csv.DictWriter(mfile, fieldnames=columns)
                for row in new_entries:
                    writer.writerow(row)
            msg = f"{len(new_entries)} new entries added."
        else:
            msg = "No new unique entries found."

        self.log(msg)
        self.update_status(msg)
        return msg

    def sort_main_csv(self, main_file, columns):
        """Sort main CSV by first column (A-Z)."""
        if not os.path.exists(main_file):
            raise FileNotFoundError("Main file does not exist.")

        with open(main_file, newline='', encoding='utf-8') as mfile:
            reader = csv.DictReader(mfile)
            data = list(reader)
            if not reader.fieldnames or columns[0] not in reader.fieldnames:
                raise ValueError(f"Column '{columns[0]}' not found.")
        
        data.sort(key=lambda x: x.get(columns[0], "").lower())

        with open(main_file, 'w', newline='', encoding='utf-8') as mfile:
            writer = csv.DictWriter(mfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(data)

        msg = f"Main CSV sorted by '{columns[0]}'."
        self.log(msg)
        self.update_status(msg)
        return msg

    def remove_duplicates_by_name(self, main_file, columns):
        """Remove duplicates by first column value."""
        if not os.path.exists(main_file):
            raise FileNotFoundError("Main file does not exist.")

        with open(main_file, newline='', encoding='utf-8') as mfile:
            reader = csv.DictReader(mfile)
            rows = list(reader)

        seen = set()
        unique_rows = []
        for row in rows:
            name_val = row.get(columns[0], '').strip().lower()
            if name_val and name_val not in seen:
                seen.add(name_val)
                unique_rows.append(row)

        with open(main_file, 'w', newline='', encoding='utf-8') as mfile:
            writer = csv.DictWriter(mfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(unique_rows)

        removed = len(rows) - len(unique_rows)
        msg = f"Removed {removed} duplicate entries."
        self.log(msg)
        self.update_status(msg)
        return msg

    def export_cleaned_sorted_csv(self, main_file, save_path, columns):
        """Export cleaned & sorted CSV to a new file."""
        if not os.path.exists(main_file):
            raise FileNotFoundError("Main file does not exist.")

        with open(main_file, newline='', encoding='utf-8') as mfile:
            reader = csv.DictReader(mfile)
            rows = list(reader)

        seen = set()
        cleaned = []
        for row in rows:
            name_val = row.get(columns[0], '').strip().lower()
            if name_val and name_val not in seen:
                seen.add(name_val)
                cleaned.append(row)

        cleaned.sort(key=lambda x: x.get(columns[0], '').lower())

        with open(save_path, 'w', newline='', encoding='utf-8') as newfile:
            writer = csv.DictWriter(newfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(cleaned)

        msg = f"Exported cleaned & sorted data to: {save_path}"
        self.log(msg)
        self.update_status(msg)
        return msg

    def generate_urls_from_csv(self, filepath):
        """Generate URL columns from image links in CSV."""
        def extract_id(url): return url.strip().split("/")[-1]
        def build_thumbs_url(fid): return f"https://img.doppiocdn.com/thumbs/{fid}/{fid}"
        def build_m3u8_url(fid): return f"https://edge-hls.doppiocdn.org/hls/{fid}/master/{fid}_auto.m3u8"

        if not os.path.exists(filepath):
            raise FileNotFoundError("CSV file not found.")

        df = pd.read_csv(filepath)
        if 'image-background src' not in df.columns:
            raise ValueError("Column 'image-background src' not found.")

        df['file_id'] = df['image-background src'].apply(extract_id)
        df['thumbs_url'] = df['file_id'].apply(build_thumbs_url)
        df['m3u8_url'] = df['file_id'].apply(build_m3u8_url)

        df.rename(columns={
            'model-list-item-username': 'name',
            'm3u8_url': 'url'
        }, inplace=True)

        output_path = filepath.rsplit(".", 1)[0] + "_with_urls.csv"
        df.to_csv(output_path, index=False)

        msg = f"URLs generated and saved as: {output_path}"
        self.log(msg)
        self.update_status(msg)
        return output_path
