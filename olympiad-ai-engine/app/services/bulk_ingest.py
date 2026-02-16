import os
from app.services.ingest import ingest_pdf


def ingest_all_pdfs(base_path="data/pdfs"):

    for grade_folder in os.listdir(base_path):

        grade_path = os.path.join(base_path, grade_folder)

        if not os.path.isdir(grade_path):
            continue

        # Extract grade number
        grade = int(grade_folder.replace("grade", ""))

        for subject in os.listdir(grade_path):

            subject_path = os.path.join(grade_path, subject)

            if not os.path.isdir(subject_path):
                continue

            for chapter_folder in os.listdir(subject_path):

                chapter_path = os.path.join(subject_path, chapter_folder)

                if not os.path.isdir(chapter_path):
                    continue

                for file in os.listdir(chapter_path):

                    if file.endswith(".pdf"):

                        file_path = os.path.join(chapter_path, file)

                        chapter_name = file.replace(".pdf", "")

                        print(f"Ingesting Grade {grade} | {subject} | {chapter_name}")

                        ingest_pdf(
                            file_path=file_path,
                            grade=grade,
                            subject=subject,
                            chapter_name=chapter_name
                        )

    return {"status": "All PDFs successfully ingested"}
