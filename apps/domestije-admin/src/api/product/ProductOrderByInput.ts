import { SortOrder } from "../../util/SortOrder";

export type ProductOrderByInput = {
  createdAt?: SortOrder;
  descriptionEn?: SortOrder;
  descriptionRs?: SortOrder;
  descriptionRu?: SortOrder;
  id?: SortOrder;
  isActive?: SortOrder;
  price?: SortOrder;
  sku?: SortOrder;
  titleEn?: SortOrder;
  titleRs?: SortOrder;
  titleRu?: SortOrder;
  updatedAt?: SortOrder;
};
