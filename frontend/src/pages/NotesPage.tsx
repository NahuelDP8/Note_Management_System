import { useState } from "react";
import { useAuth } from "../auth/AuthContext";
import { useNavigate } from "react-router-dom";
import NoteItem from "../components/NoteItem";
import ConfirmModal from "../components/ConfirmModal";
import CategoryMultiSelect from "../components/CategoryMultiSelect";
import { useNotes } from "../hooks/useNotes";
import { useCategories } from "../hooks/useCategories";

export default function NotesPage() {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const { categories } = useCategories();

  const [showArchived, setShowArchived] = useState(false);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [noteToDelete, setNoteToDelete] = useState<number | null>(null);

  const [selectedCategoriesFilter, setSelectedCategoriesFilter] = useState<number[]>([]);
  const [selectedCategories, setSelectedCategories] = useState<number[]>([]);

  const {
    notes,
    loading,
    error,
    createNote,
    toggleArchive,
    deleteNote,
    updateNote
  } = useNotes(showArchived, selectedCategoriesFilter);

  const handleCreate = async () => {
    if (!title.trim()) return;

    await createNote(title, content, selectedCategories);

    setTitle("");
    setContent("");
    setSelectedCategories([]);
  };

  const confirmDelete = async () => {
    if (noteToDelete === null) return;
    await deleteNote(noteToDelete);
    setNoteToDelete(null);
  };

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-slate-100 py-10 px-4">
      <div className="app-container space-y-8">

        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Create Note</h2>

          <input
            className="input-field"
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />

          <textarea
            className="input-field h-24 resize-none"
            placeholder="Content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
          />

          <CategoryMultiSelect
            categories={categories}
            selected={selectedCategories}
            onChange={setSelectedCategories}
            placeholder="Select categories..."
          />

          <button
            onClick={handleCreate}
            className="btn-primary mt-3"
            disabled={loading}
          >
            Create
          </button>
        </div>

        <div className="card">

          <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6 gap-4">
            <h1 className="text-2xl font-bold">
              {showArchived ? "Archived Notes" : "Active Notes"}
            </h1>

            <div className="flex gap-3">
              <button
                className="btn-secondary"
                onClick={() => setShowArchived((prev) => !prev)}
              >
                {showArchived ? "Show Active" : "Show Archived"}
              </button>

              <button
                className="btn-danger"
                onClick={handleLogout}
              >
                Logout
              </button>
            </div>
          </div>

          <CategoryMultiSelect
            categories={categories}
            selected={selectedCategoriesFilter}
            onChange={setSelectedCategoriesFilter}
            placeholder="Filter by categories..."
          />

          {loading && <p className="text-slate-500 mt-4">Loading...</p>}
          {error && <p className="text-red-500 mt-4">{error}</p>}

          {!loading && notes.length === 0 && (
            <p className="text-slate-400 text-sm mt-4">
              No notes found.
            </p>
          )}

          <div className="notes-grid mt-6">
            {notes.map((note) => (
              <NoteItem
                key={note.id}
                note={note}
                categories={categories}
                showArchived={showArchived}
                onToggleArchive={toggleArchive}
                onDelete={(id) => setNoteToDelete(id)}
                onEdit={updateNote}
              />
            ))}
          </div>
        </div>

        <ConfirmModal
          isOpen={noteToDelete !== null}
          message="Are you sure you want to delete this note?"
          onConfirm={confirmDelete}
          onCancel={() => setNoteToDelete(null)}
        />

      </div>
    </div>
  );
}
