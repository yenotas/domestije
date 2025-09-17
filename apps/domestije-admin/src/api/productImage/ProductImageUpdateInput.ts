import { ProductWhereUniqueInput } from "../product/ProductWhereUniqueInput";

export type ProductImageUpdateInput = {
  imageUrl?: string | null;
  product?: ProductWhereUniqueInput | null;
};
