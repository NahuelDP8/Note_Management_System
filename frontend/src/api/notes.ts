import api from "./axios";
import type { Note } from "../types/note";

export const fetchNotes = async (
  archived: boolean,
  categoryIds?: number[] | null
): Promise<Note[]> => {
  const response = await api.get<Note[]>("/notes", {
    params: {
      archived,
      category_ids:
        categoryIds && categoryIds.length > 0
          ? categoryIds.join(",")
          : undefined,
    },
  });

  return response.data;
};



export const createNoteRequest = async (
  title: string,
  content: string,
  category_ids: number[]
): Promise<Note> => {
  const response = await api.post<Note>("/notes", {
    title,
    content,
    category_ids,
  });
  return response.data;
};


export const updateNoteRequest = async (
  id: number,
  data: {
    title?: string;
    content?: string;
    category_ids?: number[];
  }
): Promise<Note> => {
  const response = await api.put<Note>(`/notes/${id}`, data);
  return response.data;
};


export const archiveNoteRequest = async (
  id: number
): Promise<void> => {
  await api.patch(`/notes/${id}/archive`);
};

export const unarchiveNoteRequest = async (
  id: number
): Promise<void> => {
  await api.patch(`/notes/${id}/unarchive`);
};

export const deleteNoteRequest = async (
  id: number
): Promise<void> => {
  await api.delete(`/notes/${id}`);
};
