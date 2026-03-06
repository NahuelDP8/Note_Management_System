import api from "./axios";

export interface Category {
  id: number;
  name: string;
}

export const fetchCategories = async (): Promise<Category[]> => {
  const response = await api.get<Category[]>("/categories");
  return response.data;
};

export const createCategoryRequest = async (
  name: string
): Promise<Category> => {
  const response = await api.post<Category>("/categories", { name });
  return response.data;
};
