import { SortOrder } from "../../util/SortOrder";

export type CategoryOrderByInput = {
  createdAt?: SortOrder;
  descriptionEn?: SortOrder;
  descriptionRs?: SortOrder;
  descriptionRu?: SortOrder;
  id?: SortOrder;
  parent?: SortOrder;
  promotionId?: SortOrder;
  titleEn?: SortOrder;
  titleRs?: SortOrder;
  titleRu?: SortOrder;
  updatedAt?: SortOrder;
};
