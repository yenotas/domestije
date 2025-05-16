import { SortOrder } from "../../util/SortOrder";

export type ProductImageOrderByInput = {
  createdAt?: SortOrder;
  id?: SortOrder;
  imageUrl?: SortOrder;
  productId?: SortOrder;
  updatedAt?: SortOrder;
};
