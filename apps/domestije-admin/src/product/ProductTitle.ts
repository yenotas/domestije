import { Product as TProduct } from "../api/product/Product";

export const PRODUCT_TITLE_FIELD = "titleEn";

export const ProductTitle = (record: TProduct): string => {
  return record.titleEn?.toString() || String(record.id);
};
