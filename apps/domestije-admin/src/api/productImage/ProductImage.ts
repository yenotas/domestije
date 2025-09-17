import { Product } from "../product/Product";

export type ProductImage = {
  createdAt: Date;
  id: string;
  imageUrl: string | null;
  product?: Product | null;
  updatedAt: Date;
};
