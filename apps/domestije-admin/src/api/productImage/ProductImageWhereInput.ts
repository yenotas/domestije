import { StringFilter } from "../../util/StringFilter";
import { StringNullableFilter } from "../../util/StringNullableFilter";
import { ProductWhereUniqueInput } from "../product/ProductWhereUniqueInput";

export type ProductImageWhereInput = {
  id?: StringFilter;
  imageUrl?: StringNullableFilter;
  product?: ProductWhereUniqueInput;
};
