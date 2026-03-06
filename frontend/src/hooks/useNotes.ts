import { useEffect, useState } from "react";
import type { Note } from "../types/note";
import {
  fetchNotes,
  createNoteRequest,
  updateNoteRequest,
  archiveNoteRequest,
  unarchiveNoteRequest,
  deleteNoteRequest,
} from "../api/notes";

export function useNotes(
  showArchived: boolean,
  categoryIds?: number[] | null
){
  const [notes, setNotes] = useState<Note[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadNotes = async () => {
    try {
      setLoading(true);
      setError(null);

      const data = await fetchNotes(showArchived, categoryIds);
      setNotes(data);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch notes");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
  loadNotes();
}, [showArchived, categoryIds]);


  const createNote = async (
    title: string,
    content: string,
    categoryIds: number[]
  ) => {
    try {
      const newNote = await createNoteRequest(title, content, categoryIds);
      setNotes((prev) => [newNote, ...prev]);
    } catch (err) {
      console.error(err);
      setError("Failed to create note");
    }
  };


  const updateNote = async (
    id: number,
    title: string,
    content: string,
    categoryIds: number[]
  ) => {
    try {
      const updated = await updateNoteRequest(id, {
        title,
        content,
        category_ids: categoryIds,
      });

      setNotes((prev) =>
        prev.map((note) =>
          note.id === id ? updated : note
        )
      );
    } catch (err) {
      console.error(err);
      setError("Failed to update note");
    }
  };

  const toggleArchive = async (id: number) => {
    try {
      if (showArchived) {
        await unarchiveNoteRequest(id);
      } else {
        await archiveNoteRequest(id);
      }

      setNotes((prev) =>
        prev.filter((note) => note.id !== id)
      );
    } catch (err) {
      console.error(err);
      setError("Failed to archive note");
    }
  };

  const deleteNote = async (id: number) => {
    try {
      await deleteNoteRequest(id);

      setNotes((prev) =>
        prev.filter((note) => note.id !== id)
      );
    } catch (err) {
      console.error(err);
      setError("Failed to delete note");
    }
  };

  return {
    notes,
    loading,
    error,
    createNote,
    updateNote,
    toggleArchive,
    deleteNote,
    refresh: loadNotes,
  };
}
