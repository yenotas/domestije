import { Category as TCategory } from "../api/category/Category";

export const CATEGORY_TITLE_FIELD = "titleEn";

export const CategoryTitle = (record: TCategory): string => {
  return record.titleEn?.toString() || String(record.id);
};
