from csv import DictWriter

from .analysis import Analysis

class CSVExporter:
    def __init__(self, file, output_path):
        self.file = file
        self.output_path = output_path / f"{self.file.type}s"
        self.output_path.mkdir(exist_ok=True)
        self.code_header = f"{self.file.type} code"
        self.name_header = f"{self.file.type} full title"
        self.summary_path = self.output_path / 'summary.csv'

    def export(self, keywords):
        with self.summary_path.open('w') as summary_file:
            summary_csv = DictWriter(summary_file, fieldnames=[self.code_header, self.name_header, *keywords])
            summary_csv.writeheader()
            for obj in self.file:
                analysis = Analysis(obj)
                analysis.analyse(keywords)
                summary_record = analysis.summary
                total_matches = sum(summary_record.values())
                summary_record[self.code_header] = obj.code
                summary_record[self.name_header] = obj.full_title
                summary_csv.writerow(summary_record)
                if not total_matches:
                    continue
                detail_path = self.output_path / f"{obj.code}.txt"
                with detail_path.open('w') as detail_file:
                    for kw, results in analysis.results.items():
                        if not summary_record[kw]:
                            continue
                        for section, examples in results.items():
                            if not examples:
                                continue
                            msg = f'found keyword "{kw}" {len(examples)} times in "{section}"'
                            print(f"{'='*len(msg)}\n{msg}\n{'='*len(msg)}\n", file=detail_file)
                            print("\n\n".join([f"'{c}'" for c in examples]), "\n", file=detail_file)
