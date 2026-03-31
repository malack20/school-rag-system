import api from "./api";

export async function listDocuments() {
  const { data } = await api.get("/api/documents/");
  return data;
}

export async function uploadDocument(formData) {
  const { data } = await api.post("/api/documents/upload", formData);
  return data;
}

export async function reindex() {
  const { data } = await api.post("/api/documents/reindex");
  return data;
}

export async function analyzeDocument(id) {
  const { data } = await api.post(`/api/documents/${id}/analyze`, null, { timeout: 20000 });
  return data;
}
