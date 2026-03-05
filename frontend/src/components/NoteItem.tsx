import { useState } from "react";
import type { Note } from "../types/note";

type NoteItemProps = {
  note: Note;
  showArchived: boolean;
  onToggleArchive: (id: number) => void;
  onDelete: (id: number) => void;
  onEdit: (id: number, title: string, content: string) => void;
};

export default function NoteItem({
  note,
  showArchived,
  onToggleArchive,
  onDelete,
  onEdit,
}: NoteItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedTitle, setEditedTitle] = useState(note.title);
  const [editedContent, setEditedContent] = useState(note.content);

  const handleSave = async () => {
    if (!editedTitle.trim()) return;

    await onEdit(note.id, editedTitle, editedContent);
    setIsEditing(false);
  };

  return (
    <div className="note-card h-64 flex flex-col">

      {isEditing ? (
        <>
          <input
            className="input-field"
            value={editedTitle}
            onChange={(e) => setEditedTitle(e.target.value)}
          />

          <textarea
            className="input-field flex-1 resize-none"
            value={editedContent}
            onChange={(e) => setEditedContent(e.target.value)}
          />

          <div className="flex gap-2 mt-2">
            <button className="btn-primary" onClick={handleSave}>
              Save
            </button>
            <button
              className="btn-secondary"
              onClick={() => setIsEditing(false)}
            >
              Cancel
            </button>
          </div>
        </>
      ) : (
        <>
          <h3 className="note-title truncate">
            {note.title}
          </h3>

          <div className="note-content flex-1">
            {note.content}
          </div>

          <div className="flex justify-between items-center pt-3 border-t mt-3">
            <button
              className="btn-secondary"
              onClick={() => setIsEditing(true)}
            >
              Edit
            </button>

            <button
              className="btn-secondary"
              onClick={() => onToggleArchive(note.id)}
            >
              {showArchived ? "Unarchive" : "Archive"}
            </button>

            <button
              className="btn-danger"
              onClick={() => onDelete(note.id)}
            >
              Delete
            </button>
          </div>
        </>
      )}
    </div>
  );
}
