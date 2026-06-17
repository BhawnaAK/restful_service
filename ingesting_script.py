from functions import ingest_pdf

if __name__ == "__main__":
    benefits_policy_pdf_path = r"C:\Users\GenaiblrpioUsr44\Desktop\RAG_LANGGRAPH\data\benefits_policy.pdf"
    ingest_pdf(benefits_policy_pdf_path, r".\vectorDBs\benefits_policy")
    print("Benefits policy PDF Ingested")


    travel_policy_pdf_path = r"C:\Users\GenaiblrpioUsr44\Desktop\RAG_LANGGRAPH\data\travel_policy.pdf"
    ingest_pdf(travel_policy_pdf_path, r".\vectorDBs\travel_policy")
    print("Travel policy PDF Ingested")


    employee_handbook_pdf_path = r"C:\Users\GenaiblrpioUsr44\Desktop\RAG_LANGGRAPH\data\employee_handbook.pdf"
    ingest_pdf(benefits_policy_pdf_path, r".\vectorDBs\employee_handbook")
    print("Employee Handbook PDF Ingested")