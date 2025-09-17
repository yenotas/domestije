import { StringNullableFilter } from "../../util/StringNullableFilter";
import { StringFilter } from "../../util/StringFilter";
import { ProductListRelationFilter } from "../product/ProductListRelationFilter";
import { PromotionWhereUniqueInput } from "../promotion/PromotionWhereUniqueInput";
import { SliderListRelationFilter } from "../slider/SliderListRelationFilter";

export type CategoryWhereInput = {
  descriptionEn?: StringNullableFilter;
  descriptionRs?: StringNullableFilter;
  descriptionRu?: StringNullableFilter;
  id?: StringFilter;
  parent?: StringNullableFilter;
  products?: ProductListRelationFilter;
  promotion?: PromotionWhereUniqueInput;
  sliders?: SliderListRelationFilter;
  titleEn?: StringNullableFilter;
  titleRs?: StringNullableFilter;
  titleRu?: StringNullableFilter;
};
