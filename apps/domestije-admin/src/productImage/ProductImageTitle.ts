import { ProductImage as TProductImage } from "../api/productImage/ProductImage";

export const PRODUCTIMAGE_TITLE_FIELD = "imageUrl";

export const ProductImageTitle = (record: TProductImage): string => {
  return record.imageUrl?.toString() || String(record.id);
};
