import { useState } from "react";
import type { Category } from "../types/note";

type Props = {
  categories: Category[];
  selected: number[];
  onChange: (values: number[]) => void;
  placeholder?: string;
};

export default function CategoryMultiSelect({
  categories,
  selected,
  onChange,
  placeholder = "Select categories...",
}: Props) {
  const [open, setOpen] = useState(false);

  const toggleCategory = (id: number) => {
    if (selected.includes(id)) {
      onChange(selected.filter((c) => c !== id));
    } else {
      onChange([...selected, id]);
    }
  };

  const selectedCategories = categories.filter((c) =>
    selected.includes(c.id)
  );

  return (
    <div className="relative">
      <div
        onClick={() => setOpen(!open)}
        className="input-field min-h-[42px] flex flex-wrap gap-2 cursor-pointer"
      >
        {selectedCategories.length === 0 && (
          <span className="text-slate-400 text-sm">{placeholder}</span>
        )}

        {selectedCategories.map((cat) => (
          <span
            key={cat.id}
            className="bg-blue-100 text-blue-700 px-2 py-1 rounded-full text-xs font-medium"
          >
            {cat.name}
          </span>
        ))}
      </div>

      {open && (
        <div className="absolute z-10 mt-2 w-full bg-white border rounded-xl shadow-lg max-h-60 overflow-y-auto">
          {categories.map((cat) => {
            const isSelected = selected.includes(cat.id);
            return (
              <div
                key={cat.id}
                onClick={() => toggleCategory(cat.id)}
                className={`px-4 py-2 cursor-pointer text-sm hover:bg-slate-100 ${
                  isSelected ? "bg-blue-50 font-medium" : ""
                }`}
              >
                {cat.name}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
