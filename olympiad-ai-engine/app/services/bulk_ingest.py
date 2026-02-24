import os
from app.services.ingest import ingest_pdf

def ingest_all_pdfs(base_path="data/pdfs"):

    for grade_folder in os.listdir(base_path):

        grade_path = os.path.join(base_path, grade_folder)

        if not os.path.isdir(grade_path):
            continue

        grade = int(grade_folder.replace("grade", ""))

        for subject_folder in os.listdir(grade_path):

            subject_path = os.path.join(grade_path, subject_folder)

            if not os.path.isdir(subject_path):
                continue

            subject = subject_folder.lower()

            for file in os.listdir(subject_path):

                if file.endswith(".pdf"):

                    file_path = os.path.join(subject_path, file)

                    chapter_name = (
                        file.replace(".pdf", "")
                            .split("-", 1)[-1]
                            .strip()
                            .lower()
                    )

                    print(f"Ingesting Grade {grade} | {subject} | {chapter_name}")

                    ingest_pdf(
                        file_path=file_path,
                        grade=grade,
                        subject=subject,
                        chapter_name=chapter_name
                    )

    return {"status": "All PDFs successfully ingested"}