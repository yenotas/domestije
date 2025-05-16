import { ProductWhereUniqueInput } from "../product/ProductWhereUniqueInput";

export type ProductImageCreateInput = {
  imageUrl?: string | null;
  product?: ProductWhereUniqueInput | null;
};
