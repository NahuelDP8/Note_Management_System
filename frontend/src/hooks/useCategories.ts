import { useEffect, useState } from "react";
import {
  fetchCategories,
  createCategoryRequest,
  type Category,
} from "../api/categories";

export function useCategories() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(false);

  const loadCategories = async () => {
    try {
      setLoading(true);
      const data = await fetchCategories();
      setCategories(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCategories();
  }, []);

  const createCategory = async (name: string) => {
    const newCategory = await createCategoryRequest(name);
    setCategories((prev) => [...prev, newCategory]);
  };

  return {
    categories,
    loading,
    createCategory,
    refresh: loadCategories,
  };
}
