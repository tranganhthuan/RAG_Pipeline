from httpx import Client
from configs.config import BACKEND_SERVER_URL
from server.services.convert import convert_service


def convert_file(name, job_id):
    convert_service.convert_file(name)
    convert_service.add_document(name.replace(".pdf", ".md"))
    client = Client()
    client.post(f"{BACKEND_SERVER_URL}/api/response_convert", json={"job_id": job_id})

if __name__ == "__main__":
    convert_file("paper.pdf", "convert-95e3aee3-a560-4295-8cda-b867b212893t")
