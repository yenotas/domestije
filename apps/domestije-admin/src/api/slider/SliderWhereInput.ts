import { CategoryWhereUniqueInput } from "../category/CategoryWhereUniqueInput";
import { StringFilter } from "../../util/StringFilter";
import { StringNullableFilter } from "../../util/StringNullableFilter";
import { ProductWhereUniqueInput } from "../product/ProductWhereUniqueInput";

export type SliderWhereInput = {
  category?: CategoryWhereUniqueInput;
  id?: StringFilter;
  imageUrl?: StringNullableFilter;
  linkType?: "Product" | "Category" | "External";
  product?: ProductWhereUniqueInput;
  subtitleEn?: StringNullableFilter;
  subtitleRs?: StringNullableFilter;
  subtitleRu?: StringNullableFilter;
  titleEn?: StringNullableFilter;
  titleRs?: StringNullableFilter;
  titleRu?: StringNullableFilter;
  videoUrl?: StringNullableFilter;
};
