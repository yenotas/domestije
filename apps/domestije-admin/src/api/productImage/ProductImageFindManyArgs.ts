import { ProductImageWhereInput } from "./ProductImageWhereInput";
import { ProductImageOrderByInput } from "./ProductImageOrderByInput";

export type ProductImageFindManyArgs = {
  where?: ProductImageWhereInput;
  orderBy?: Array<ProductImageOrderByInput>;
  skip?: number;
  take?: number;
};
