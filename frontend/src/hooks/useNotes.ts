import { useEffect, useState } from "react";
import api from "../api/axios";
import type { Note } from "../types/note";

export function useNotes(showArchived: boolean) {
  const [notes, setNotes] = useState<Note[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchNotes = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await api.get(
        `/notes/?archived=${showArchived}`
      );

      setNotes(response.data);
    } catch {
      setError("Failed to fetch notes");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotes();
  }, [showArchived]);

  const createNote = async (title: string, content: string) => {
    const response = await api.post("/notes/", { title, content });
    setNotes(prev => [response.data, ...prev]);
  };

  const updateNote = async (
    id: number,
    title: string,
    content: string
  ) => {
    const response = await api.put(`/notes/${id}`, {
      title,
      content,
    });

    setNotes(prev =>
      prev.map(note =>
        note.id === id ? response.data : note
      )
    );
  };

  const toggleArchive = async (id: number) => {
    const endpoint = showArchived
      ? `/notes/${id}/unarchive`
      : `/notes/${id}/archive`;

    await api.patch(endpoint);

    setNotes(prev =>
      prev.filter(note => note.id !== id)
    );
  };

  const deleteNote = async (id: number) => {
    await api.delete(`/notes/${id}`);

    setNotes(prev =>
      prev.filter(note => note.id !== id)
    );
  };

  return {
    notes,
    loading,
    error,
    createNote,
    updateNote,
    toggleArchive,
    deleteNote,
  };
}
